import logging
import os
import re

from .managed_entity import ManagedEntity
from .managed_file import InputFile


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class ExpressionData(ManagedEntity):

    def __init__(self, config, yml_data, annotation):

        self.annotation = annotation

        ManagedEntity.__init__(self, config, default_services=annotation.deploy_services, yml_data=yml_data)

        self.name = self.yml_data['name']
        self.unit = self.yml_data['unit'] if 'unit' in self.yml_data else 'TPM'
        self.replicates = self.yml_data['replicates'] if 'replicates' in self.yml_data else []

        self.safe_name = re.sub(r'[^a-zA-Z0-9-]', '_', self.name)

        self.version = "0"  # No version for this kind of data

        self.entity_name = 'expression_data'

        self.input_files = {
            'table': InputFile.from_yml(self.yml_data["table"], name='fasta', version=self.version)
        }

        self.tasks = self.config.get_tasks(self)

        self.load_tasks_derived_files()

    def get_children(self):

        return []

    def get_organism(self):

        return self.annotation.get_organism()

    def get_parent(self):

        return self.annotation

    def slug(self, short=False):

        if short:
            return "{}_exp{}".format(self.annotation.slug(short), self.sanitize(self.safe_name))
        else:
            return "{}/expression_{}".format(self.annotation.slug(short), self.sanitize(self.safe_name))

    def pretty_name(self, with_parent=True):

        if with_parent:
            return "{} expression data {}".format(self.annotation.pretty_name(), self.name)
        else:
            return "Expression data {}".format(self.name)

    def get_work_dir(self):

        return os.path.join(self.annotation.get_work_dir(), "expression_{}".format(self.sanitize(self.safe_name)))

    def get_locked_yml(self):

        locked_yml = self.yml_data

        locked_yml['table'] = self.input_files['table'].to_yml()

        if len(self.derived_files):
            locked_yml['derived'] = []

            for id, der in self.derived_files.items():
                locked_yml['derived'].append(der.to_yml())

        return locked_yml

    def get_metadata(self, inherit=True):

        metadata = {'expression_data_id': self.safe_name}

        if inherit:
            metadata.update(self.annotation.get_metadata())

        metadata.update(self.get_basic_metadata())

        return metadata

    def load_locked_data(self, locked_yml, future=False):

        ManagedEntity.load_locked_data(self, locked_yml, future)

        if 'table' in locked_yml:
            self.input_files['table'].merge_with_locked(locked_yml['table'], future)

    def find_matching_yml_in_list(self, yml):
        """
        Find a yml subelement from a list matching the current object
        """

        for ysub in yml:
            if ysub["name"] == self.name:
                return ysub

        return {}
