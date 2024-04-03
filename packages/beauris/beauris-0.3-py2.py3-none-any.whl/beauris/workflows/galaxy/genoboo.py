#!/usr/bin/env python
import argparse
import logging
import sys

from beauris import Beauris


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def get_func_annot_files(file_uploads, annot):
    has_annot = False
    blast_db = None
    # Need diamond (xml), interproscan (tsv), and eggnog (tsv)
    if 'func_annot_bipaa' in annot.tasks:
        has_annot = True
        blast_db = annot.derived_files['diamond'].get_tool_version()
        file_uploads['interpro_{}'.format(annot.version)] = {'type': 'tsv', 'path': annot.get_derived_path('interproscan'), 'name': 'interpro_{}'.format(annot.version)}
        file_uploads['diamond_{}'.format(annot.version)] = {'type': 'blastxml', 'path': annot.get_derived_path('diamond'), 'name': 'diamond_{}'.format(annot.version)}
        file_uploads['eggnog_{}'.format(annot.version)] = {'type': 'tsv', 'path': annot.get_derived_path('eggnog'), 'name': 'eggnog_{}'.format(annot.version)}
    elif 'func_annot_orson' in annot.tasks:
        has_annot = True
        blast_db = annot.derived_files['diamond_xml'].get_tool_version()
        file_uploads['interpro_{}'.format(annot.version)] = {'type': 'tsv', 'path': annot.get_derived_path('interproscan_tsv'), 'name': 'interpro_{}'.format(annot.version)}
        file_uploads['diamond_{}'.format(annot.version)] = {'type': 'blastxml', 'path': annot.get_derived_path('diamond_xml'), 'name': 'diamond_{}'.format(annot.version)}
        file_uploads['eggnog_{}'.format(annot.version)] = {'type': 'tsv', 'path': annot.get_derived_path('eggnog_annotations'), 'name': 'eggnog_{}'.format(annot.version)}
    return file_uploads, has_annot, blast_db


def run_genoboo_job(org, access_mode="public"):

    task_id = "build_genoboo"
    runner = bo.get_runner('galaxy', org, task_id, access_mode=access_mode)

    config_task = runner.get_job_specs(task_id)

    # Get config values
    # Not really a great solution, but envsubst + regex is not a good mix
    re_protein = config_task.get("re_protein", "$1-P$2").replace(r"\$", "$")
    re_protein_capture = config_task.get("re_protein_capture", "^(.*?)-R([A-Z]+)$")
    blast_algorithm = config_task.get("blast_algorithm", "blastp")
    blast_matrix = config_task.get("blast_matrix", "blosum62")

    exit_code_all = 0

    tools_params = {
        "existing": None
    }

    num_ass = 0
    # Use a precise tool version if possible
    # tool = "Genoboo"
    tool = "toolshed.g2.bx.psu.edu/repos/gga/genenotebook_genenotebook_build/genenotebook_build/0.4.13+galaxy0"
    file_uploads = {}

    # Should loop on assemblies later
    # For now, only take the last assembly
    for ass in org.assemblies:

        num_annot = 0

        file_uploads['ass_{}'.format(ass.slug(short=True))] = {'type': 'fasta', 'path': ass.get_input_path('fasta'), 'name': ass.slug(short=True)}

        base_key_genome = "genomes_{}|".format(num_ass)
        ass_dict = {
            base_key_genome + "name": ass.pretty_name(),
            base_key_genome + "public": True,
            base_key_genome + "genome": {
                "batch": False,
                "values": [
                    {
                        "id": "##UPLOADED_DATASET_ID__ass_{}##".format(ass.slug(short=True)),
                        "src": "hda",
                    }
                ]
            }
        }
        tools_params.update(ass_dict)
        num_ass += 1

        # Should loop on annotations later
        for annot in ass.annotations:

            base_key_annot = "{}annots_{}|".format(base_key_genome, num_annot)

            file_uploads['annot_{}'.format(annot.version)] = {'type': 'gff3', 'path': annot.get_derived_path('fixed_gff'), 'name': annot.version}
            # Get func annotation files
            # Need diamond (xml), interproscan (tsv), and eggnog (tsv)
            file_uploads, has_func_annot, blast_db = get_func_annot_files(file_uploads, annot)

            annot_dict = {
                base_key_annot + "prot_naming|method": "regex",
                base_key_annot + "annot": annot.version,
                base_key_annot + "prot_naming|re_protein": re_protein,
                base_key_annot + "prot_naming|re_protein_capture": re_protein_capture,
                base_key_annot + "annotation": {
                    "batch": False,
                    "values": [
                        {
                            "id": "##UPLOADED_DATASET_ID__annot_{}##".format(annot.version),
                            "src": "hda",
                        }
                    ]
                }
            }
            if has_func_annot:
                annot_dict.update({
                    base_key_annot + "blast_cond|blast_choice": "diamond",
                    base_key_annot + "blast_cond|algorithm": blast_algorithm,
                    base_key_annot + "blast_cond|database": blast_db,
                    base_key_annot + "blast_cond|matrix": blast_matrix,
                    base_key_annot + "blast_cond|diamond": {
                        "batch": False,
                        "values": [
                            {
                                "id": "##UPLOADED_DATASET_ID__diamond_{}##".format(annot.version),
                                "src": "hda",
                            }
                        ]
                    },
                    base_key_annot + "eggnog": {
                        "batch": False,
                        "values": [
                            {
                                "id": "##UPLOADED_DATASET_ID__eggnog_{}##".format(annot.version),
                                "src": "hda",
                            }
                        ]
                    },
                    base_key_annot + "interproscan": {
                        "batch": False,
                        "values": [
                            {
                                "id": "##UPLOADED_DATASET_ID__interpro_{}##".format(annot.version),
                                "src": "hda",
                            }
                        ]
                    }
                })

            exp_n = 0
            for exp in annot.expressions:
                file_uploads['expression_{}'.format(exp.safe_name)] = {'type': 'tsv', 'path': exp.get_input_path('table'), 'name': 'expression_{}'.format(exp.safe_name)}

                base_key_exp = base_key_annot + "expression_{}|".format(exp_n)
                annot_dict.update({
                    base_key_exp + "public": True,
                    base_key_exp + "counts": {
                        "batch": False,
                        "values": [
                            {
                                "id": "##UPLOADED_DATASET_ID__expression_{}##".format(exp.safe_name),  # TODO check uniqueness of safe_name
                                "src": "hda",
                            }
                        ]
                    },
                })
                replica_n = 0
                for replica in exp.replicates:
                    base_key_repl = base_key_exp + "expression_replicas_{}|".format(replica_n)
                    annot_dict.update({
                        base_key_repl + "replica_names": replica['name'],
                        base_key_repl + "replicas": ",".join([str(x) for x in replica['cols']]),
                    })
                    replica_n += 1
                exp_n += 1

            tools_params.update(annot_dict)
            num_annot += 1

    dest_rename = {
        'gnb_db': 'genoboo.tar.bz2'
    }

    exit_code, out, err = runner.run_or_resume_job(tool=tool, params=tools_params, uploads=file_uploads, dest_rename=dest_rename, check_output=False)

    exit_code_all += exit_code

    return exit_code_all


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    if not org.assemblies:
        log.error('At least one assembly is required for Genoboo')
        sys.exit(0)

    if all([not ass.annotations for ass in org.assemblies]):
        log.error('At least one annotation is required for Genoboo')
        sys.exit(0)

    task_id = "build_genoboo"
    exit_code_all = 0

    if not org.has_mixed_data():
        exit_code = run_genoboo_job(org)
        exit_code_all += exit_code
    else:
        purged_org = org.copy_and_purge_restricted_data()

        if org:
            exit_code = run_genoboo_job(purged_org)
            exit_code_all += exit_code
        else:
            log.info("No data to deploy (nothing left after purging)")

        exit_code = run_genoboo_job(org, "restricted")
        exit_code_all += exit_code

    # Check expected output: will take care of finding if restricted output is expected
    task_id = "build_genoboo"
    runner = bo.get_runner('galaxy', org, task_id)
    if runner.task.has_run and exit_code_all == 0:
        exit_code_all += runner.task.check_expected_outputs()

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))
