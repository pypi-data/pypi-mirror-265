import logging
import os
import re

from .managed_entity import ManagedEntity
from .managed_file import InputFile


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class ExtraFile(ManagedEntity):

    def __init__(self, config, yml_data, parent):

        self.parent = parent

        ManagedEntity.__init__(self, config, default_services=parent.deploy_services, yml_data=yml_data)

        self.name = self.yml_data['name']

        self.safe_name = re.sub(r'[^a-zA-Z0-9-]', '_', self.name)

        self.version = "0"  # No version for this kind of data

        self.entity_name = 'extra_file'

        self.input_files = {
            'file': InputFile.from_yml(self.yml_data["file"], name='file', version=self.version)
        }

        self.tasks = self.config.get_tasks(self)

        self.load_tasks_derived_files()

        self.blastbanks = []

    def get_children(self):

        return []

    def get_parent(self):

        return self.parent

    def slug(self, short=False):

        if short:
            return "{}_extra{}".format(self.parent.slug(short), self.sanitize(self.safe_name))
        else:
            return "{}/extra_file_{}".format(self.parent.slug(short), self.sanitize(self.safe_name))

    def pretty_name(self, with_parent=True):

        if with_parent:
            return "{} extra file {}".format(self.parent.pretty_name(), self.name)
        else:
            return "Extra file {}".format(self.name)

    def get_work_dir(self):

        return os.path.join(self.parent.get_work_dir(), "extra_file_{}".format(self.sanitize(self.safe_name)))

    def get_locked_yml(self):

        locked_yml = self.yml_data

        locked_yml['file'] = self.input_files['file'].to_yml()

        if len(self.derived_files):
            locked_yml['derived'] = []

            for id, der in self.derived_files.items():
                locked_yml['derived'].append(der.to_yml())

        return locked_yml

    def get_metadata(self, inherit=True):

        metadata = {'extra_file_id': self.safe_name}

        if inherit:
            metadata.update(self.parent.get_metadata())

        metadata.update(self.get_basic_metadata())

        return metadata

    def find_matching_yml_in_list(self, yml):
        """
        Find a yml subelement from a list matching the current object
        """

        for ysub in yml:
            if ysub["name"] == self.name:
                return ysub

        return {}

    def load_locked_data(self, locked_yml, future=False):

        ManagedEntity.load_locked_data(self, locked_yml, future)

        if 'file' in locked_yml:
            self.input_files['file'].merge_with_locked(locked_yml['file'], future)
