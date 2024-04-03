import csv
import logging
import os

from goatools import obo_parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class EggnogParser():

    def __init__(self, beauris_annot, protein_dict, go_file=""):
        self.annotation = beauris_annot
        self.go_file = go_file
        self.protein_dict = protein_dict

    def _get_go_terms(self, goterms):
        terms = []
        for term in goterms.split(','):
            if term not in self.go:
                logger.warn("{} is not in GO, skipping".format(term))
                continue
            terms.append(self.go[term].name)
        return terms

    def parse(self):
        if 'func_annot_bipaa' in self.annotation.tasks:
            eggnog_file = self.annotation.get_derived_path('eggnog')
        elif 'func_annot_orson' in self.annotation.tasks:
            eggnog_file = self.annotation.get_derived_path('eggnog_annotations')
        else:
            logger.warn("No eggnog file generated. Skipping")
            return self.protein_dict

        has_go = False

        if self.go_file and os.path.isfile(self.go_file):
            has_go = True
            self.go = obo_parser.GODag(self.go_file, optional_attrs={'consider', 'replaced_by'}, load_obsolete=True, prt=None)
        else:
            logger.warn("Go file missing. Will not store Go descriptions")

        with open(eggnog_file, 'r') as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if row[0].startswith("#"):
                    continue
                protein_id = row[0]
                eggnog_og_terms = row[7]
                go_ids = row[9]

                if protein_id not in self.protein_dict:
                    logger.warn("{} - linked mRNA not in GFF file, skipping".format(protein_id))
                    continue

                if eggnog_og_terms != "-":
                    self.protein_dict[protein_id]['eggnog_og_terms'].add(eggnog_og_terms)
                if go_ids != "-":
                    self.protein_dict[protein_id]['go_ids'].update(go_ids.split(","))
                    if has_go:
                        self.protein_dict[protein_id]['go_terms'].update(self._get_go_terms(go_ids))

        return self.protein_dict
