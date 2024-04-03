import logging
import os
import shutil
import tarfile
import tempfile

from beauris.organism import Organism

from .basedeployer import BaseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class GenobooDeployer(BaseDeployer):

    service_name = 'genoboo'

    def __init__(self, config, server, entity):

        self.supported_entity_types = (Organism)

        BaseDeployer.__init__(self, config, server, entity)

    def write_data(self):

        genoboo_folder = self._get_data_dir()
        genoboo_arch_path = self.entity.get_derived_path('build_genoboo')

        self.deploy_variables['genoboo_expression_unit'] = self._genoboo_get_expression_unit(self.entity)

        if os.path.exists(genoboo_arch_path):
            self._do_setup_genoboo(genoboo_arch_path, genoboo_folder)

        if self.entity.has_mixed_data():
            genoboo_folder = self._get_data_dir(restricted=True)
            genoboo_arch_path = self.entity.get_derived_path('build_genoboo_restricted')

            if os.path.exists(genoboo_arch_path):
                self._do_setup_genoboo(genoboo_arch_path, genoboo_folder, restricted=True)

    def _do_setup_genoboo(self, derived_path, dst_folder, restricted=False):

        os.makedirs(dst_folder, exist_ok=True)

        data_folder = os.path.join(dst_folder, 'mongo_db')
        data_exists = os.path.exists(data_folder)

        # Extracting to temp dir to let the previous version online during extraction
        extract_folder = tempfile.mkdtemp(dir=dst_folder)

        # Unpack archive to folder
        log.info("Extracting genoboo data from {} to temp dir {}".format(derived_path, extract_folder))
        # Change containing folder name to 'data'
        with tarfile.open(derived_path, 'r:bz2') as intarf:
            for member in intarf.getmembers():
                member.name = os.path.join('data', os.path.basename(member.name))
                intarf.extract(member, extract_folder)

        # Create 'log' folder now to set permissions
        os.makedirs(os.path.join(extract_folder, 'log'), exist_ok=True)

        os.chmod(extract_folder, 0o755)

        old_data_dir = data_folder + "_old"
        if data_exists:
            # We move first
            log.info("Moving old genoboo data dir to {}".format(old_data_dir))
            if os.path.isdir(old_data_dir):
                # This should not happen, but might be residual data after a previous crash
                log.info("{} exists, removing before".format(old_data_dir))
                shutil.rmtree(old_data_dir)
            shutil.move(data_folder, old_data_dir)

        log.info("Moving newly extracted genoboo data dir from {} to {}".format(extract_folder, data_folder))
        shutil.move(extract_folder, data_folder)

        # Write config file
        genoboo_conf_file = os.path.join(self.deploy_base_path, "genoboo.json")
        if restricted:
            genoboo_conf_file = os.path.join(self.deploy_base_path, "genoboo_restricted.json")
        with open(genoboo_conf_file, 'w') as f:
            f.write(self._render_template(self._get_ansible_template('genoboo.json.j2'), with_vars={"restricted": restricted}))

    def _genoboo_get_expression_unit(self, org):
        units = set()
        for ass in org.assemblies:
            for annot in ass.annotations:
                for exp in annot.expressions:
                    units.add(exp.unit)

        if len(units) > 1:
            raise RuntimeError("Multiple expression units found: {}".format(units))

        if len(units) == 1:
            return units.pop()
        return 'TPM'

    def check_services_to_reload(self):

        # No reloading in staging, we down & up
        if self.server == "staging":
            return []

        services_to_reload = []

        dirc = os.path.join(self._get_data_dir(), 'mongo_db')
        if os.path.exists(dirc):
            services_to_reload.append('genoboo')

        dirc = os.path.join(self._get_data_dir(restricted=True), 'mongo_db')
        if os.path.exists(dirc):
            services_to_reload.append('genoboo-restricted')

        return services_to_reload

    def to_cleanup(self):
        to_cleanup = []

        dirc = os.path.join(self._get_data_dir(), 'mongo_db')
        if os.path.exists(dirc):
            to_cleanup.append(os.path.join(self._get_data_dir(), 'mongo_db_old'))

        dirc = os.path.join(self._get_data_dir(restricted=True), 'mongo_db')
        if os.path.exists(dirc):
            to_cleanup.append(os.path.join(self._get_data_dir(restricted=True), 'mongo_db_old'))

        return to_cleanup
