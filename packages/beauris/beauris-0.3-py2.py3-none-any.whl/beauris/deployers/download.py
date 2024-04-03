import logging
import os
import shutil
import tempfile

from beauris.organism import Organism

from .basedeployer import BaseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class DownloadDeployer(BaseDeployer):

    service_name = 'download'

    def __init__(self, config, server, entity):

        self.supported_entity_types = (Organism)

        BaseDeployer.__init__(self, config, server, entity)

    def write_data(self):

        if self.config.raw['data_locker']['method'] == "dir":
            data_base_path = os.path.join(self.deploy_base_path, "src_data")
            self._setup_download_links(data_base_path)

            if self.entity.has_mixed_data():
                data_base_path += "_restricted"
                self._setup_download_links(data_base_path, restricted=True)
        else:
            raise NotImplementedError()

        self.do_nginx_conf()
        if self.entity.has_mixed_data():
            self.do_nginx_conf(restricted=True)

    def do_nginx_conf(self, restricted=False):
        # Prepare nginx config
        ndir = 'nginx'
        if restricted:
            ndir += "_restricted"
        nginx_path = os.path.join(self.deploy_base_path, ndir, 'conf')
        os.makedirs(nginx_path, exist_ok=True)

        with open(os.path.join(nginx_path, "default.conf"), 'w') as f:
            f.write(self._render_template(self._get_ansible_template('default.conf.j2')))

    def _setup_download_links(self, data_base_path, restricted=False):

        if self.entity.has_mixed_data() and not restricted:
            purged_ent = self.entity.copy_and_purge_restricted_data()
        else:
            purged_ent = self.entity

        files = purged_ent.get_files_to_publish()

        # Delete any old download content
        if os.path.exists(data_base_path):
            for filename in os.listdir(data_base_path):
                file_path = os.path.join(data_base_path, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

        for file, entity in files:
            src_path = file.get_usable_path()
            dest_path = file.get_publish_path(entity.get_work_dir(), data_base_path, entity)

            link_dir = os.path.dirname(dest_path)
            os.makedirs(link_dir, exist_ok=True)
            if os.path.islink(dest_path):
                if not os.readlink(dest_path) == src_path:
                    # Update link
                    temp_link_name = tempfile.mktemp(dir=link_dir)
                    os.symlink(src_path, temp_link_name)
                    os.replace(temp_link_name, dest_path)
            else:
                os.symlink(src_path, dest_path)
