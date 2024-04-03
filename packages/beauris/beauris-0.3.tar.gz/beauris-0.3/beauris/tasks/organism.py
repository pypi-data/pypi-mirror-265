import logging

from ..task import Task, TaskOutput

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class OrganismTasks():

    entity_name = 'organism'

    @staticmethod
    def get_tasks():

        return {
            'build_genoboo': BuildGenobooTask,
            'build_elasticsearch': BuildElasticsearchTask,

            'deploy_authelia': DeployAutheliaTask,
            'deploy_download': DeployDownloadTask,
            'deploy_blast': DeployBlastTask,
            'deploy_jbrowse': DeployJBrowseTask,
            'deploy_genoboo': DeployGenobooTask,
            'deploy_elasticsearch': DeployElasticsearchTask
        }


class DeployAutheliaTask(Task):

    params = {
        'always_run': True
    }


class DeployDownloadTask(Task):

    params = {
        'always_run': True
    }


class DeployBlastTask(Task):

    params = {
        'always_run': True
    }


class DeployJBrowseTask(Task):

    params = {
        'always_run': True
    }


class DeployGenobooTask(Task):

    params = {
        'always_run': True
    }


class DeployElasticsearchTask(Task):

    params = {
        'always_run': True
    }


class BuildGenobooTask(Task):

    params = {
        'check_perms': True
    }

    def run_only_for_services(self):

        return [
            ('genoboo', self.entity.assemblies)
        ]

    def get_func_annot_files(self, annot):
        data = []
        # Need diamond (xml), interproscan (tsv), and eggnog (tsv)
        if 'func_annot_bipaa' in annot.tasks:
            data.append(annot.derived_files['interproscan'])
            data.append(annot.derived_files['diamond'])
            data.append(annot.derived_files['eggnog'])
        elif 'func_annot_orson' in annot.tasks:
            data.append(annot.derived_files['interproscan_tsv'])
            data.append(annot.derived_files['diamond_xml'])
            data.append(annot.derived_files['eggnog_annotations'])
        return data

    def get_derived_outputs(self):

        if not self.entity.assemblies or not self.check_required_by_services():
            log.info('Loading tasks plan: Genoboo is not derived for {}'.format(self.entity.slug()))
            return []

        deps = []
        if self.entity.assemblies:
            for ass in self.entity.assemblies:
                deps.append(ass.input_files['fasta'])
                for annot in ass.annotations:
                    deps.append(annot.input_files['gff'])
                    deps += self.get_func_annot_files(annot)
                    for exp in annot.expressions:
                        deps.append(exp.input_files['table'])

        tool_version = '0.4.13'

        return [
            TaskOutput(name='build_genoboo', ftype='genoboo', path='genoboo.tar.bz2', tool_version=tool_version, publish=False, access_mode_from_children=True, depends_on=deps),
        ]


class BuildElasticsearchTask(Task):

    params = {
        'check_perms': True
    }

    def run_only_for_services(self):

        return [
            ('elasticsearch', self.entity.assemblies)
        ]

    def get_func_annot_files(self, annot):
        data = []
        # Need diamond (xml), interproscan (tsv), and eggnog (tsv)
        if 'func_annot_bipaa' in annot.tasks:
            data.append(annot.derived_files['interproscan'])
            data.append(annot.derived_files['diamond'])
            data.append(annot.derived_files['eggnog'])
        elif 'func_annot_orson' in annot.tasks:
            data.append(annot.derived_files['interproscan_tsv'])
            data.append(annot.derived_files['diamond_xml'])
            data.append(annot.derived_files['eggnog_annotations'])
        return data

    def get_derived_outputs(self):

        if not self.entity.assemblies or not any([ass.annotations for ass in self.entity.assemblies]) or not self.check_required_by_services():
            log.info('Loading tasks plan: Elasticsearch is not derived for {}'.format(self.entity.slug()))
            return []

        deps = []
        if self.entity.assemblies:
            for ass in self.entity.assemblies:
                deps.append(ass.input_files['fasta'])
                for annot in ass.annotations:
                    deps.append(annot.input_files['gff'])
                    deps += self.get_func_annot_files(annot)
                    for exp in annot.expressions:
                        deps.append(exp.input_files['table'])

        tool_version = '8.7.0'

        return [
            TaskOutput(name='build_elasticsearch', ftype='es', path='es.tar.bz2', tool_version=tool_version, publish=False, depends_on=deps),
        ]
