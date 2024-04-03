import json
import logging
import os
import shutil
import tarfile
import tempfile

from beauris.assembly import Assembly
from beauris.organism import Organism

from .basedeployer import BaseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class JbrowseDeployer(BaseDeployer):

    service_name = 'jbrowse'

    def __init__(self, config, server, entity):

        self.supported_entity_types = (Assembly, Organism)

        BaseDeployer.__init__(self, config, server, entity)

    def write_data(self):

        jbrowse_folder = self._get_data_dir()

        if isinstance(self.entity, Assembly):

            if (not self.entity.organism.has_mixed_data()) \
               or (self.entity.organism.has_mixed_data() and not self.entity.is_restricted()):
                self.write_ass_data(jbrowse_folder)

            if self.entity.organism.has_mixed_data():
                jbrowse_folder = self._get_data_dir(restricted=True)
                self.write_ass_data(jbrowse_folder, restricted=True)

        elif isinstance(self.entity, Organism):
            self.write_org_data(jbrowse_folder)

            if self.entity.has_mixed_data():
                jbrowse_folder = self._get_data_dir(restricted=True)
                self.write_org_data(jbrowse_folder, restricted=True)
        else:
            raise NotImplementedError()

    def replace_service_url_placeholder(self, tracklist_file, restricted):

        with open(tracklist_file, "r") as tli:
            tl_content = tli.read()

        for service_name in self.entity.get_deploy_services(self.server):
            placeholder = f"https://__BEAURIS_SERVICE_URL_PLACEHOLDER_{service_name}__"

            good_url = self.entity.config.get_service_url(service_name, self.server, self.entity.organism, restricted)

            tl_content = tl_content.replace(placeholder, good_url)

        with open(tracklist_file, "w") as tlo:
            tlo.write(tl_content)

    def write_ass_data(self, jbrowse_folder, restricted=False):

        os.makedirs(jbrowse_folder, exist_ok=True)

        assembly_jbrowse_folder = os.path.join(jbrowse_folder, self.entity.slug(short=True))
        jbrowse_exists = os.path.exists(assembly_jbrowse_folder)
        if restricted and 'jbrowse_restricted' in self.entity.derived_files:
            # can be jbrowse_restricted or jbrowse depending if assembly itself has mixed_data or not
            jbrowse_arch_path = self.entity.get_derived_path('jbrowse_restricted')
        else:
            jbrowse_arch_path = self.entity.get_derived_path('jbrowse')

        # Extracting to temp dir to let the previous version online during extraction
        extract_folder = tempfile.mkdtemp(dir=jbrowse_folder)

        # Unpack archive to folder
        if self.server == "production":
            log.info("Extracting jbrowse data from {} to temp dir {}".format(jbrowse_arch_path, extract_folder))
            with tarfile.open(jbrowse_arch_path, 'r:gz') as intarf:
                # We need to modify the links to use the proper bam files
                log.info("Editing jbrowse tar.gz on the fly to use correct track file paths")
                tracks_real_path = self.entity.get_track_paths(prefer='locked')

                # First find all fake files that we need to replace by proper symlinks
                trackl = intarf.extractfile(intarf.getmember('trackList.json'))
                trl = json.load(trackl)

                to_swap = self.entity.jbrowse_track_swapping(trl['tracks'], tracks_real_path)

                for member in intarf.getmembers():
                    if member.name in to_swap:
                        os.makedirs(os.path.join(extract_folder, os.path.dirname(member.name)), exist_ok=True)
                        os.symlink(to_swap[member.name], os.path.join(extract_folder, member.name))
                    elif member.isfile() and not member.issym():
                        intarf.extract(member, path=extract_folder)

        elif self.server == "staging":
            log.info("Extracting jbrowse data from {} to temp dir {}".format(jbrowse_arch_path, extract_folder))
            with tarfile.open(jbrowse_arch_path, 'r:gz') as intarf:
                intarf.extractall(path=extract_folder)

        else:
            raise RuntimeError("Unexpected server type {}".format(self.server))

        self.replace_service_url_placeholder(os.path.join(extract_folder, 'trackList.json'), restricted)

        # Write tracks.conf
        with open(os.path.join(extract_folder, "tracks.conf"), "w") as f:
            f.write("[general]\ndataset_id = {}\n".format(self.entity.slug(short=True)))

        os.chmod(extract_folder, 0o755)

        old_data_dir = assembly_jbrowse_folder + "_old"
        if jbrowse_exists:
            # We move first
            log.info("Moving old jbrowse data dir to {}".format(old_data_dir))
            if os.path.isdir(old_data_dir):
                # This should not happen, but might be residual data after a previous crash
                log.info("{} exists, removing before".format(old_data_dir))
                shutil.rmtree(old_data_dir)
            shutil.move(assembly_jbrowse_folder, old_data_dir)

        log.info("Moving newly extracted jbrowse data dir from {} to {}".format(extract_folder, assembly_jbrowse_folder))
        shutil.move(extract_folder, assembly_jbrowse_folder)

        if jbrowse_exists:
            # Delete after
            log.info("Finished, removing old jbrowse data dir {}".format(old_data_dir))
            shutil.rmtree(old_data_dir)

    def write_org_data(self, jbrowse_folder, restricted=False):

        os.makedirs(jbrowse_folder, exist_ok=True)

        if self.entity.has_mixed_data() and not restricted:
            purged_ent = self.entity.copy_and_purge_restricted_data()
        else:
            purged_ent = self.entity

        if purged_ent is None:
            return

        with open(os.path.join(jbrowse_folder, "datasets.conf"), "w") as f:
            for ass in purged_ent.assemblies:
                safe_slug = ass.slug(short=True).replace('.', '_')  # Jbrowse doesn't like dots
                f.write("[datasets.{}]\n".format(safe_slug))
                f.write("url = ?data=data/{}\nname = {}\n".format(ass.slug(short=True), ass.pretty_name()))
