#!/usr/bin/env python

# Send an organism archive to a remote Apollo server

import argparse
import io
import json
import logging
import os
import sys
import tarfile

from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def fix_track_paths(intarf, output, to_swap, entity, server):

    with tarfile.open(output, 'w:gz') as tarf:
        for member in intarf.getmembers():
            if member.name in to_swap:
                log.info("Replacing archive file {} by symlink to {}".format(member.name, to_swap[member.name]))
                # Creating a new TarInfo object to avoid strange bug when replacing a symlink by a new one
                new_member = tarfile.TarInfo(name=member.name)
                new_member.type = tarfile.SYMTYPE
                new_member.linkname = to_swap[member.name]
                new_member.size = 0
                new_member.mode = member.mode
                new_member.mtime = member.mtime
                tarf.addfile(
                    tarinfo=new_member
                )
            elif member.name == "trackList.json":
                # Edit service urls on the fly
                tl_content = intarf.extractfile(member).read().decode()

                for service_name in entity.get_deploy_services(server):
                    placeholder = f"https://__BEAURIS_SERVICE_URL_PLACEHOLDER_{service_name}__"

                    url_needs_restricted = entity.organism.has_mixed_data() and entity.is_restricted()
                    good_url = entity.config.get_service_url(service_name, server, entity.organism, restricted=url_needs_restricted)

                    tl_content = tl_content.replace(placeholder, good_url)

                tl_content = tl_content.encode('utf8')
                member.size = len(tl_content)
                tarf.addfile(member, io.BytesIO(tl_content))
            elif (member.isdir() or member.isfile()) and not member.issym():
                extracted = intarf.extractfile(member)
                tarf.addfile(member, extracted)
            elif member.issym():
                # symlink not in the to_swap dict => copy as is
                new_member = tarfile.TarInfo(name=member.name)
                new_member.type = tarfile.SYMTYPE
                new_member.linkname = member.linkname
                new_member.size = 0
                new_member.mode = member.mode
                new_member.mtime = member.mtime
                tarf.addfile(
                    tarinfo=new_member
                )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str)
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)
    task_id = "apollo"

    script_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./"))
    genus = org.genus
    species = org.species

    exit_code_all = 0

    if 'apollo' not in org.get_deploy_services(args.server):
        log.info('Skipping Apollo deployment')
        sys.exit(0)

    if 'apollo' not in bo.config.raw or args.server not in bo.config.raw['apollo'] \
       or 'url' not in bo.config.raw['apollo'][args.server] \
       or 'user' not in bo.config.raw['apollo'][args.server] \
       or 'password' not in bo.config.raw['apollo'][args.server]:
        log.error('Invalid Apollo credentials for server {}.'.format(args.server))
        sys.exit(1)

    for ass in org.assemblies:

        common_name = ass.organism.pretty_name()
        common_name += " {}".format(ass.version)

        runner = bo.get_runner('local', ass, task_id)

        # TODO Maybe task depends_on should be defined in beauris.tasks?

        # Mixed data at assembly level? add only the restricted version (we'll do the same in apollo_perms)
        # TODO make this configurable for other user cases?
        jb_dataset = 'jbrowse'
        if ass.has_mixed_data():
            jb_dataset = 'jbrowse_restricted'

        deps = [ass.derived_files[jb_dataset]]
        runner.task.depends_on = deps

        jbrowse_arch_path = ass.get_derived_path(jb_dataset)
        if runner.task.needs_to_run() and not runner.task.disable_run():

            # We need to edit the tar.gz archive because locked paths are only accessible after merging
            log.info("Editing jbrowse tar.gz on the fly to use correct track file paths and contextual menu urls")

            with tarfile.open(ass.get_derived_path(jb_dataset), 'r:gz') as intarf:

                # First find all bam files that we need to replace by proper symlinks
                trackl = intarf.extractfile(intarf.getmember('trackList.json'))
                trl = json.load(trackl)

                to_swap = {}  # In staging mode, no need to swap track paths (but still need to adapt menu urls)
                if args.server == "production":
                    to_swap = ass.jbrowse_track_swapping(trl['tracks'], ass.get_track_paths(prefer='locked'))

                jbrowse_arch_path = "{}/jbrowse/jbrowse_fix_apollo_{}.tar.gz".format(ass.get_work_dir(), args.server)

                fix_track_paths(intarf, jbrowse_arch_path, to_swap, ass, args.server)

        log.info("Running create or update organism in Apollo for {}".format(jbrowse_arch_path))

        # Run in a subprocess to capture stdout/stderr + exit code
        cmd = ["python", "{}/run_apollo.py".format(script_dir), '--update']
        cmd += [jbrowse_arch_path, common_name, genus, species, bo.config.raw['apollo'][args.server]['url'], bo.config.raw['apollo'][args.server]['user'], bo.config.raw['apollo'][args.server]['password']]

        exit_code, out, err = runner.run_or_resume_job(cmd=cmd)

        exit_code_all += exit_code

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))
