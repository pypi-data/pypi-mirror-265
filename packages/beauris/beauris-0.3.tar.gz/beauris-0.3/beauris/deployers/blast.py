import logging
import os
import shutil

from beauris.blastbank import BankWriter
from beauris.organism import Organism

from .basedeployer import BaseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class BlastDeployer(BaseDeployer):

    service_name = 'blast'

    def __init__(self, config, server, entity):

        self.supported_entity_types = (Organism)

        BaseDeployer.__init__(self, config, server, entity)

    def write_data(self):

        shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workflows", "ansible", "docker_files", "postgres-blast-entrypoint.sh"), self.deploy_base_path)

        if self.server == "production":
            # Need to create this or it will break when swarm creates the dockers
            docker_data_path = self._get_data_dir("docker_data/blast_db")
            os.makedirs(docker_data_path, exist_ok=True)

        blast_base_path = self._get_data_dir("blast")
        blast_files_path = self._get_data_dir("blast_files")

        self._do_write_banks(blast_base_path, blast_files_path)

        if self.entity.has_mixed_data():
            if self.server == "production":
                # Need to create this or it will break when swarm creates the dockers
                docker_data_path = self._get_data_dir("docker_data/blast_db_restricted")
                os.makedirs(docker_data_path, exist_ok=True)
            blast_base_path = self._get_data_dir("blast", restricted=True)
            blast_files_path = self._get_data_dir("blast_files", restricted=True)
            self._do_write_banks(blast_base_path, blast_files_path, restricted=True)

    def _do_write_banks(self, data_dir, files_dir, restricted=False):

        if self.entity.has_mixed_data() and not restricted:
            purged_ent = self.entity.copy_and_purge_restricted_data()
        else:
            purged_ent = self.entity

        banks = purged_ent.get_blast_banks()

        writer = BankWriter(banks, data_dir, files_dir, self.server, restricted)
        writer.write_bank_yml()
        writer.write_links_yml()

    def check_services_to_reload(self):

        services_to_reload = []

        # No reloading in staging, we down & up
        if self.server == "staging":
            return []

        dirc = self._get_data_dir("blast")
        if os.path.exists(dirc) and os.path.exists(os.path.join(dirc, "banks.yml")):
            services_to_reload.append('blast')

        dirc = self._get_data_dir("blast", restricted=True)
        if os.path.exists(dirc) and os.path.exists(os.path.join(dirc, "banks.yml")):
            services_to_reload.append('blast-restricted')

        return services_to_reload
