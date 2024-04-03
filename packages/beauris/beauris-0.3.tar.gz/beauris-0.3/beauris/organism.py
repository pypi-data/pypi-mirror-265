import logging
import os

import gitlab

import yaml

from .assembly import Assembly
from .extra_file import ExtraFile
from .managed_entity import ManagedEntity
from .proteome import Proteome
from .transcriptome import Transcriptome


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Organism(ManagedEntity):

    def __init__(self, config, yml_path, test_data=False, locked_dir=None, future_locked_dir=None, default_services=[]):

        self.yml_path = yml_path

        with open(yml_path, "r") as f:
            yml_str = f.read()
            if test_data:
                # This is a trick to ease tests
                yml_str = yml_str.replace('$TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../test-data')))
            try:
                self.yml_data = yaml.safe_load(yml_str)
            except yaml.YAMLError:
                log.error("Invalid organism yaml file : {}".format(yml_path))
                raise

        ManagedEntity.__init__(self, config, yml_path=yml_path, locked_dir=locked_dir, future_locked_dir=future_locked_dir, default_services=default_services, yml_data=self.yml_data)

        self.entity_name = 'organism'

        self.ci_prefix = None

        if 'computer_name' in self.yml_data:
            self.computer_name = self.yml_data['computer_name']
            self.computer_name_short = self.yml_data['computer_name']
        else:
            # TODO better computer_name guessing with strains
            self.computer_name = "{}_{}".format(self.yml_data['genus'], self.yml_data['species']).lower()
            self.computer_name_short = "{}{}".format(self.yml_data['genus'][:1], self.yml_data['species']).lower()
            if 'strain' in self.yml_data:
                self.computer_name = "{}_{}".format(self.computer_name, self.yml_data['strain']).lower()
            if 'sex' in self.yml_data and self.yml_data['sex'] != 'unknown':
                self.computer_name = "{}_{}".format(self.computer_name, self.yml_data['sex']).lower()

        self.genus = self.yml_data['genus']
        self.species = self.yml_data['species']
        self.strain = self.yml_data.get('strain', '')
        self.sex = self.yml_data.get('sex', '')

        self.common_name = self.yml_data.get('common_name', '')

        self.xrefs = {}
        if 'xrefs' in self.yml_data:
            self.xrefs = self.yml_data['xrefs']

        pic_path = self.config.raw.get("picture_files", "")
        default_pic_file = None
        if pic_path:
            root_custom = os.path.dirname(self.config.config_file_path)
            default_pic_file = os.path.join(root_custom, pic_path, self.computer_name)

        self.picture_file = None
        self.picture_ext = None
        if 'picture_file' in self.yml_data:
            self.picture_file = self.yml_data.get("picture", {}).get("file", "")
        elif default_pic_file and os.path.exists(default_pic_file + '.png'):
            self.picture_file = default_pic_file + '.png'
        elif default_pic_file and os.path.exists(default_pic_file + '.jpg'):
            self.picture_file = default_pic_file + '.jpg'

        if self.picture_file:
            self.picture_ext = os.path.splitext(self.picture_file)[1]

        self.picture_author = self.config.raw.get("picture", {}).get("author", None)
        self.picture_source_url = self.config.raw.get("picture", {}).get("source_url", None)

        self.task_options = self.load_task_options(self.yml_data)
        self.parse_services(self.yml_data)

        self.tasks = self.config.get_tasks(self)

        self.assemblies = self._load_assemblies()

        self.transcriptomes = self._load_transcriptomes()

        self.proteomes = self._load_proteomes()

        self.extra_files = self._load_extra_files()

        self.load_tasks_derived_files()

        self.load_locked_yml(test_data)

        self.load_locked_yml(test_data, future=True)

        if len(self.get_restricted_tos()) > 1:
            raise RuntimeError("Multiple different 'restricted_to' rules in a single organism are not supported (found {})".format(self.get_restricted_tos()))

    def get_children(self):

        return self.assemblies + self.transcriptomes + self.proteomes + self.extra_files

    def get_organism(self):

        return self

    def get_assembly(self, version):

        for ass in self.assemblies:
            if ass.version == version:
                return ass

        return None

    def slug(self, short=False):

        if short:
            return self.computer_name_short
        else:
            return self.computer_name

    def pretty_name(self, with_parent=True):

        if self.common_name:
            return self.common_name

        name_clean = "{} {}".format(self.genus, self.species).lower().capitalize()
        if self.strain:
            name_clean += " {}".format(self.strain)
        if self.sex:
            name_clean += " {}".format(self.sex)

        return name_clean

    def _load_assemblies(self):
        assemblies = []
        for ass in self.yml_data.get("assemblies", []):
            assemblies.append(Assembly(self.config, ass, self))

        return assemblies

    def _load_transcriptomes(self):
        transcriptomes = []
        for trans in self.yml_data.get("transcriptomes", []):
            transcriptomes.append(Transcriptome(self.config, trans, self))

        return transcriptomes

    def _load_proteomes(self):
        proteomes = []
        for trans in self.yml_data.get("proteomes", []):
            proteomes.append(Proteome(self.config, trans, self))

        return proteomes

    def _load_extra_files(self):
        extra_files = []
        for trans in self.yml_data.get("extra_files", []):
            extra_files.append(ExtraFile(self.config, trans, self))

        return extra_files

    def get_ci_prefix(self):

        # Use cached value when possible
        if self.ci_prefix is not None:
            return self.ci_prefix

        needed_env_vars = [
            'CI_PROJECT_ID',
            'CI_SERVER_URL',
            'GITLAB_BOT_TOKEN',
            'CI_COMMIT_BRANCH',
            'CI_DEFAULT_BRANCH',
        ]

        prefix = ""

        if os.getenv('CI_MERGE_REQUEST_IID'):
            prefix = "{}-".format(os.getenv('CI_MERGE_REQUEST_IID'))
        elif all(item in os.environ for item in needed_env_vars) and os.getenv('CI_COMMIT_BRANCH') == os.getenv('CI_DEFAULT_BRANCH'):
            # Not in a merge request, but maybe this commit comes from a merged one on default branch

            gl_url = os.getenv('CI_SERVER_URL')
            gl = gitlab.Gitlab(url=gl_url, private_token=os.getenv('GITLAB_BOT_TOKEN'))

            project = gl.projects.get(os.getenv('CI_PROJECT_ID'), lazy=True)
            commit = project.commits.get(os.getenv('CI_COMMIT_SHORT_SHA'))
            mrs = commit.merge_requests()

            if len(mrs) == 1 and 'iid' in mrs[0]:
                prefix = "{}-".format(mrs[0]['iid'])

        self.ci_prefix = prefix

        return prefix

    def get_work_dir(self, prefix=None):

        if prefix:
            dirname = prefix
        else:
            dirname = self.get_ci_prefix()

        dirname += self.computer_name

        return os.path.join(self.config.root_work_dir, dirname)

    def get_locked_yml(self):

        locked_yml = self.yml_data

        if len(self.derived_files):
            locked_yml['derived'] = []

            for id, der in self.derived_files.items():
                locked_yml['derived'].append(der.to_yml())

        locked_yml['assemblies'] = []

        if self.assemblies:
            for ass in self.assemblies:
                locked_yml['assemblies'].append(ass.get_locked_yml())

        if self.transcriptomes:
            locked_yml['transcriptomes'] = []

            for trans in self.transcriptomes:
                locked_yml['transcriptomes'].append(trans.get_locked_yml())

        if self.proteomes:
            locked_yml['proteomes'] = []

            for trans in self.proteomes:
                locked_yml['proteomes'].append(trans.get_locked_yml())

        if self.extra_files:
            locked_yml['extra_files'] = []

            for trans in self.extra_files:
                locked_yml['extra_files'].append(trans.get_locked_yml())

        return locked_yml

    def get_metadata(self, inherit=True):

        return {
            'computer_name': self.computer_name,
            'genus': self.genus,
            'species': self.species,
            'strain': self.strain,
            'restricted_to': self.restricted_to,
        }

    def load_locked_yml(self, test_data=False, future=False):

        if future:
            ymlpath = self.future_locked_yml_path
        else:
            ymlpath = self.locked_yml_path

        if not os.path.isfile(ymlpath):
            log.info("No {}locked data found in '{}'".format("future " if future else "", ymlpath))
            return

        log.info("Loading locked data from {}".format(ymlpath))

        with open(ymlpath, "r") as f:
            yml_str = f.read()
            if test_data:
                # This is a trick to ease tests
                yml_str = yml_str.replace('$TEST_DATA_DIR', os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../test-data')))
            try:
                locked_yml_data = yaml.safe_load(yml_str)
            except yaml.YAMLError:
                log.error("Invalid {}locked yaml file : {}".format("future " if future else "", ymlpath))
                raise

        return self.load_locked_data(locked_yml_data, future)

    def load_locked_data(self, locked_yml, future=False):

        ManagedEntity.load_locked_data(self, locked_yml, future)

        for ass in self.assemblies:
            ass.load_locked_data(ass.find_matching_yml_in_list(locked_yml.get("assemblies", [])), future)

        for trans in self.transcriptomes:
            trans.load_locked_data(trans.find_matching_yml_in_list(locked_yml.get("transcriptomes", [])), future)

        for trans in self.proteomes:
            trans.load_locked_data(trans.find_matching_yml_in_list(locked_yml.get("proteomes", [])), future)

        for trans in self.extra_files:
            trans.load_locked_data(trans.find_matching_yml_in_list(locked_yml.get("extra_files", [])), future)

    def purge_restricted_data(self):

        kept_ass = []
        for ass in self.assemblies:
            if ass.restricted_to is None:
                ass.purge_restricted_data()
                kept_ass.append(ass)

        self.assemblies = kept_ass

        kept_trans = []
        for trans in self.transcriptomes:
            if trans.restricted_to is None:
                trans.purge_restricted_data()
                kept_trans.append(trans)

        self.transcriptomes = kept_trans

        kept_prot = []
        for prot in self.proteomes:
            if prot.restricted_to is None:
                prot.purge_restricted_data()
                kept_prot.append(prot)

        self.proteomes = kept_prot

        kept_extra = []
        for xtra in self.extra_files:
            if xtra.restricted_to is None:
                xtra.purge_restricted_data()
                kept_extra.append(xtra)

        self.extra_files = kept_extra

    def get_deploy_services(self, server):

        servs = ManagedEntity.get_deploy_services(self, server)

        # TODO #109 refactor this stuff, we should probably have a Service class and proper management of Task/Service and Service/Service dependencies
        if 'genoboo' in servs and all('genoboo' not in x.get_deploy_services(server) for x in self.get_children()):
            servs.remove('genoboo')

        if 'elasticsearch' in servs and all('elasticsearch' not in x.get_deploy_services(server) for x in self.get_children()):
            servs.remove('elasticsearch')

        if 'jbrowse' in servs and all('jbrowse' not in x.get_deploy_services(server) for x in self.get_children()):
            servs.remove('jbrowse')

        if 'apollo' in servs and all('apollo' not in x.get_deploy_services(server) for x in self.get_children()):
            servs.remove('apollo')

        if 'blast' in servs and all('blast' not in x.get_deploy_services(server) for x in self.get_children()):
            servs.remove('blast')

        if 'download' in servs and all('download' not in x.get_deploy_services(server) for x in self.get_children()):
            servs.remove('download')

        # So ugly, sorry sorry sorry, #109
        if set(servs) == set(['authelia', 'apollo']):
            # No docker service? => no need for authelia
            servs.remove('authelia')

        return servs
