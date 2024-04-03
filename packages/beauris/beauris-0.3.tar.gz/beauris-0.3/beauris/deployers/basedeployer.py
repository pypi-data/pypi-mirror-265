import logging
import os
import shutil
import sys
from copy import deepcopy
from urllib.parse import urlsplit

import ansible_runner

from beauris.assembly import Assembly
from beauris.organism import Organism

from jinja2 import Template

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class BaseDeployer():

    def __init__(self, config, server, entity):

        self.config = config
        self.server = server

        if not self.service_name:
            raise RuntimeError("Invalid deployer, missing a service_name attribute")

        if not self.supported_entity_types:
            raise RuntimeError("Invalid deployer, missing a supported_entity_types attribute")

        self.entity = entity

        if not isinstance(self.entity, self.supported_entity_types):
            raise RuntimeError("Can't deploy a {} service with a {} entity".format(self.service_name, entity.__class__.__name__))

        if isinstance(self.entity, Organism):
            self.deploy_base_path = os.path.join(self.config.deploy[server]["target_dir"], self.entity.genus, self.entity.species, self.entity.strain)
        elif isinstance(self.entity, Assembly):
            self.deploy_base_path = os.path.join(self.config.deploy[server]["target_dir"], self.entity.organism.genus, self.entity.organism.species, self.entity.organism.strain)
        else:

            # TODO need to be a bit cleaner when we'll deploy other things than organism
            raise RuntimeError("Can't initialize deploy_base_path with a {} entity".format(self.entity.__class__.__name__))

        # Prepare folder
        os.makedirs(self.deploy_base_path, exist_ok=True)

        self.init_variables()

    def write_data(self):

        raise NotImplementedError()

    def _get_data_dir(self, service_name=None, restricted=False):

        if not service_name:
            data_dir = os.path.join(self.deploy_base_path, 'docker_data', self.service_name)
        else:
            data_dir = os.path.join(self.deploy_base_path, service_name)

        if restricted:
            data_dir += "_restricted"

        return data_dir

    def _get_ansible_template(self, path, check_exists=True):

        custom_path = self.config.raw['ansible'][self.server].get("custom_templates", "")

        if custom_path:

            root_custom = os.path.dirname(self.config.config_file_path)
            custom_path = os.path.join(root_custom, custom_path, path)

            if os.path.exists(custom_path):
                return custom_path

        default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workflows", "ansible", "templates", path)

        if check_exists and not os.path.exists(default_path):
            raise RuntimeError("Could not find file {}".format(default_path))

        return default_path

    def _render_template(self, template_file, with_vars={}):
        with open(template_file) as f:
            template = Template(f.read())

        dvars = deepcopy(self.deploy_variables)
        dvars.update(with_vars)
        return template.render(dvars)

    def _run_playbook(self, playbook, extravars={}):
        data = self._get_ansible_data(playbook)

        data['extravars'].update(extravars)

        r = ansible_runner.run(**data)

        log.info("Running playbook {}".format(playbook))
        log.info("{}: {}".format(r.status, r.rc))
        log.info("Final status:")
        log.info(r.stats)

        # Cleanup, since ansible store the ssh key and env var in files in the env folder
        shutil.rmtree(os.path.join(data["private_data_dir"], "env"))

        if r.rc != 0:
            log.error("Ansible playbook execution failed, exiting")
            sys.exit(r.rc)

    def _get_ansible_data(self, playbook):

        inventory = {"docker_swarm_host": {"hosts": self.config.raw['ansible'][self.server]["host"]}}
        extravars = {
            "deploy_dir": self.deploy_base_path,
            "stack_name": self.stack_name,
        }
        envvars = {}

        # Add external env variables
        for key, value in self.config.raw['ansible'][self.server].get("envvars", {}).items():
            envvars[key] = value

        for key, value in self.config.raw['ansible'][self.server].get("extravars", {}).items():
            extravars[key] = value

        private_ssh_key = os.getenv("ANSIBLE_SSH_KEY") + "\n"

        return {
            "private_data_dir": os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workflows", "ansible", "ansible_data"),
            "inventory": inventory,
            "playbook": playbook,
            "ssh_key": private_ssh_key,
            "extravars": extravars,
            "envvars": envvars,
        }

    def init_variables(self):

        self.base_url = self.config.deploy[self.server]["base_url"].rstrip("/")
        # TODO default for url_prefix should be ""
        self.url_prefix = self.config.deploy[self.server]["url_prefix"].rstrip("/")
        self.netloc = urlsplit(self.base_url).netloc

        # Url for restricted data
        self.base_url_restricted = self.config.deploy[self.server]["base_url_restricted"].rstrip("/")
        # TODO default for url_prefix should be ""
        self.url_prefix_restricted = self.config.deploy[self.server]["url_prefix_restricted"].rstrip("/")
        self.netloc_restricted = urlsplit(self.base_url_restricted).netloc

        self.stack_name = self.entity.slug()  # TODO this is ugly to set this here (might not be an organism), but otoh we might need it for non-organisms
        self.sub_url = self.stack_name
        if self.server == "staging":
            self.stack_name += "_staging"
            if self.config.deploy[self.server].get("append_staging"):
                self.sub_url += "_staging"

        blast_theme = self.config.deploy[self.server]["options"].get("blast_theme", "")  # TODO this is ugly to set this here (might not be an organism), but otoh we might need it for non-organisms

        apollo_url = ""  # TODO this is ugly to set this here (might not be an organism), but otoh we might need it for non-organisms

        if 'apollo' in self.config.raw:
            apollo_url = self.config.get_service_url('apollo', self.server)

        self.deploy_variables = {
            "stack_name": self.stack_name,
            "locker_folder": os.path.join(self.config.raw['data_locker']['options']['target_dir'], "") if self.config.raw['data_locker']['method'] == "dir" else "",
            "root_work_dir": self.config.root_work_dir,
            "netloc": self.netloc,
            "netloc_restricted": self.netloc_restricted,
            "sub_url": self.sub_url,
            "stage": self.server,
            "base_url": self.base_url,
            "url_prefix": self.url_prefix,
            "base_url_restricted": self.base_url_restricted,
            "url_prefix_restricted": self.url_prefix_restricted,
            "blast_job_folder": os.path.join(self.config.deploy[self.server]["options"].get("blast_job_dir", "")),
            "blast_theme": os.path.join(blast_theme, "") if blast_theme else "",
            "use_apollo": 'apollo' in self.entity.get_deploy_services(self.server),
            "apollo_url": apollo_url,
            "deploy_blast": 'blast' in self.entity.get_deploy_services(self.server),
            "deploy_download": 'download' in self.entity.get_deploy_services(self.server),
            "deploy_jbrowse": 'jbrowse' in self.entity.get_deploy_services(self.server),
            "deploy_authelia": 'authelia' in self.entity.get_deploy_services(self.server),
            "deploy_genoboo": 'genoboo' in self.entity.get_deploy_services(self.server),
            "deploy_elasticsearch": "elasticsearch" in self.entity.get_deploy_services(self.server),
            "org": self.entity,
            "extra_ref_data_dirs": self.config.deploy[self.server]['options'].get("extra_ref_data_dirs", []),
            "genoboo_expression_unit": "TPM"
        }

    def check_services_to_reload(self):

        return []

    def to_cleanup(self):

        return []

    def cleanup(self, to_cleanup):

        for old_data_dir in to_cleanup:
            if os.path.exists(old_data_dir):
                log.info("Cleaning old data dir {}".format(old_data_dir))
                shutil.rmtree(old_data_dir)

    def get_notifications(self):
        return []
