import logging
import os

from beauris.organism import Organism

from .basedeployer import BaseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class DockerComposeDeployer(BaseDeployer):

    service_name = 'dockercompose'

    def __init__(self, config, server, entity):

        self.supported_entity_types = (Organism)

        BaseDeployer.__init__(self, config, server, entity)

    def write_data(self):

        with open(os.path.join(self.deploy_base_path, "docker-compose.yml"), 'w') as f:
            f.write(self._render_template(self._get_ansible_template('docker-compose.yml.j2')))

    def start(self, update_existing=[]):
        log.info("Starting interface")
        self._run_playbook("playbook_deploy.yml")

        for exi in update_existing:
            log.info("Force reload of '{}'".format(exi))
            extravars = {
                "service_name": "{}_{}".format(self.stack_name, exi)
            }
            self._run_playbook("playbook_update.yml", extravars)

    def shutdown(self):
        log.info("Shutting down interface")
        self._run_playbook("playbook_shutdown.yml")
