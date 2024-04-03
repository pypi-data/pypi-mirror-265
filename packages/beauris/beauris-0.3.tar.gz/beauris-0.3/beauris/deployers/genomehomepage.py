import logging
import os
import shutil

from beauris.organism import Organism

from .basedeployer import BaseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class GenomeHomepageDeployer(BaseDeployer):

    service_name = 'genomehomepage'

    def __init__(self, config, server, entity):

        self.supported_entity_types = (Organism)

        BaseDeployer.__init__(self, config, server, entity)

    def write_data(self):

        self.do_write_site()

        if self.entity.has_mixed_data():
            self.do_write_site(restricted=True)

    def do_write_site(self, restricted=False):

        sdir = 'site'
        if restricted:
            sdir += "_restricted"
        os.makedirs(os.path.join(self.deploy_base_path, sdir), exist_ok=True)

        if self.entity.has_mixed_data() and not restricted:
            purged_ent = self.entity.copy_and_purge_restricted_data()
        else:
            purged_ent = self.entity

        with_vars = {"org": purged_ent}

        if restricted:
            with_vars['base_url'] = self.base_url_restricted
            with_vars['url_prefix'] = self.url_prefix_restricted
            with_vars['base_url_public'] = self.base_url
            with_vars['url_prefix_public'] = self.url_prefix

        with_vars['has_mixed_data'] = self.entity.has_mixed_data()
        with_vars['is_restricted'] = restricted

        with open(os.path.join(self.deploy_base_path, sdir, "index.html"), 'w') as f:
            f.write(self._render_template(self._get_ansible_template('web/index.html.j2'), with_vars=with_vars))

        # Prepare search web page
        if self.deploy_variables['deploy_elasticsearch']:
            try:
                template_path = self._get_ansible_template('web/search.html.j2', check_exists=True)
                dst = os.path.join(self.deploy_base_path, sdir, "search.html")
                with open(dst, 'w') as f:
                    f.write(self._render_template(template_path, with_vars=with_vars))
            except RuntimeError:
                pass

        assets_dir = self._get_ansible_template('web/assets', False)
        if os.path.exists(assets_dir):
            # dirs_exist_ok only works in python >= 3.8
            shutil.copytree(assets_dir, os.path.join(self.deploy_base_path, sdir, "assets"), dirs_exist_ok=True)

        if self.entity.picture_file:
            shutil.copy(self.entity.picture_file, os.path.join(self.deploy_base_path, sdir, "assets", 'images', 'organism' + self.entity.picture_ext))

    def get_notifications(self):
        log_messages = []

        log_messages.append("All interface setup jobs succeeded for {}".format(self.entity.slug()))
        log_messages.append("Interface will be available at: {}{}/{}/".format(self.base_url, self.url_prefix, self.sub_url))
        if self.entity.has_mixed_data():
            log_messages.append("Restricted interface will be available at: {}{}/{}/".format(self.base_url_restricted, self.url_prefix_restricted, self.sub_url))

        return log_messages
