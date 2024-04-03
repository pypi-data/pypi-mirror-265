import logging
import os
import shutil
import tarfile
import tempfile

from beauris.organism import Organism

from .basedeployer import BaseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class ElasticsearchDeployer(BaseDeployer):

    service_name = 'elasticsearch'

    def __init__(self, config, server, entity):

        self.supported_entity_types = (Organism)

        BaseDeployer.__init__(self, config, server, entity)

    def write_data(self):

        es_folder = self._get_data_dir()
        es_arch_path = self.entity.get_derived_path('build_elasticsearch')

        self._do_write_es_data(es_folder, es_arch_path)

    def _do_write_es_data(self, es_folder, es_arch_path, restricted=False):

        os.makedirs(es_folder, exist_ok=True)

        data_folder = os.path.join(es_folder, 'data')
        data_exists = os.path.exists(data_folder)

        # Extracting to temp dir to keep the previous version online during extraction
        extract_folder = tempfile.mkdtemp(dir=es_folder)
        # Permission to let ES run
        os.chmod(extract_folder, 0o755)

        # Unpack archive to folder
        log.info("Extracting elasticsearch data from {} to temp dir {}".format(es_arch_path, extract_folder))
        # Remove first level ("data" folder)
        with tarfile.open(es_arch_path, 'r:bz2') as intarf:
            for member in intarf.getmembers():
                if member.name == "data":
                    continue
                member.name = member.name.replace("data/", "")
                # Skip lock file.
                # NB: Might be a better idea to properly shutdown ES when generating data?
                if member.name == "node.lock":
                    continue
                intarf.extract(member, extract_folder)

        old_data_dir = data_folder + "_old"
        if data_exists:
            # We move first
            log.info("Moving old elasticsearch data dir to {}".format(old_data_dir))
            if os.path.isdir(old_data_dir):
                # This should not happen, but might be residual data after a previous crash
                log.info("{} exists, removing before".format(old_data_dir))
                shutil.rmtree(old_data_dir)
            shutil.move(data_folder, old_data_dir)

        log.info("Moving newly extracted elasticsarch data dir from {} to {}".format(extract_folder, data_folder))
        shutil.move(extract_folder, data_folder)

        if data_exists:
            # Delete after
            log.info("Finished, removing old elasticsearch data dir {}".format(old_data_dir))
            shutil.rmtree(old_data_dir)

    def check_services_to_reload(self):

        services_to_reload = []

        # No reloading in staging, we down & up
        if self.server == "staging":
            return []

        dirc = os.path.join(self._get_data_dir(), 'data')
        if os.path.exists(dirc):
            services_to_reload.append('elasticsearch')

        dirc = os.path.join(self._get_data_dir(restricted=True), 'data')
        if os.path.exists(dirc):
            services_to_reload.append('elasticsearch')

        return services_to_reload
