import logging

from ..task import Task, TaskOutput

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class AssemblyTasks():

    entity_name = 'assembly'

    @staticmethod
    def get_tasks():

        return {
            'fasta_check': FastaCheckTask,
            'jbrowse': JBrowseTask,
            'fatotwobit': FaToTwoBitTask,
            'blastdb_assembly': BlastAssemblyTask,
            'apollo': ApolloTask,
            'apollo_perms': ApolloPermsTask,
            'deploy_jbrowse': DeployJbrowseTask,
        }


class FastaCheckTask(Task):

    pass


class JBrowseTask(Task):

    # If restricted_to changed on some track, need to regenerate
    params = {
        'check_perms': True
    }

    def run_only_for_services(self):

        return [
            ('jbrowse', self.entity),
            ('apollo', self.entity),
        ]

    def get_derived_outputs(self):

        if not self.check_required_by_services():
            log.info('Loading tasks plan: JBrowse is not derived for {}'.format(self.entity.slug()))
            return []

        deps = [self.entity.input_files['fasta']]
        for ann in self.entity.annotations:
            deps.append(ann.input_files['gff'])
        for track in self.entity.tracks:
            deps.append(track.input_files['track_file'])

        tool_version = '1.16.11'

        return [
            TaskOutput(name='jbrowse', ftype='jbrowse', path='jbrowse.tar.gz', tool_version=tool_version, publish=False, access_mode_from_children=True, depends_on=deps),
        ]


class FaToTwoBitTask(Task):

    def get_derived_outputs(self):

        deps = [self.entity.input_files['fasta']]

        tool_version = '357'

        return [
            TaskOutput(name='2bit', ftype='2bit', path='genome.2bit', tool_version=tool_version, publish=False, depends_on=deps),
        ]


class BlastAssemblyTask(Task):

    params = {
        'specs_id': 'blastdb'
    }

    blastdb_exts = ['nhr', 'nin', 'nog', 'nsd', 'nsi', 'nsq']

    def get_derived_outputs(self):

        outputs = []

        tool_version = '2.6.0'

        deps = [self.entity.input_files['fasta']]

        for ext in self.blastdb_exts:
            outputs.append(TaskOutput(name="blastdb_{}".format(ext), ftype=ext, path="assembly.{}".format(ext), tool_version=tool_version, publish=False, depends_on=deps))

        return outputs


class ApolloTask(Task):

    # If restricted_to changed, jbrowse contextual menu may change => redeploy
    params = {
        'check_perms': True
    }


class ApolloPermsTask(Task):

    params = {
        'check_perms': True
    }


class DeployJbrowseTask(Task):

    # If restricted_to changed, jbrowse contextual menu may change => redeploy
    params = {
        'check_perms': True,
        'always_run': True
    }
