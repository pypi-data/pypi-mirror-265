#!/usr/bin/env python

# Set permissions on an organism on a remote Apollo server

import argparse
import logging
import os
import sys

from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str)
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)
    task_id = "apollo_perms"

    script_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./"))

    exit_code_all = 0

    if 'apollo' not in org.get_deploy_services(args.server):
        log.info('Skipping Apollo permissions update')
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

        log.info("Updating permissions in Apollo for {}".format(common_name))

        # Manage permissions
        runner = bo.get_runner('local', ass, task_id)

        # Mixed data at assembly level? add only the restricted version and give the stricted permissions
        # TODO make this configurable for other user cases?
        jb_dataset = 'jbrowse'
        if ass.has_mixed_data():
            jb_dataset = 'jbrowse_restricted'

        deps = [ass.derived_files[jb_dataset]]
        runner.task.depends_on = deps

        rests = ass.get_restricted_tos()
        if len(rests) > 0:
            current_group = ass.get_restricted_tos()[0]
        else:
            current_group = ass.restricted_to

        # TODO This is not super generic, probably need to refactor it at some point
        if ass.restricted_to_apollo:
            current_group = ass.restricted_to_apollo

        default_group = bo.config.raw['apollo'][args.server].get('public_group')
        cmd = ["python", "{}/run_apollo_perms.py".format(script_dir)]
        if current_group:
            cmd += ["--restricted={}".format(current_group)]
        elif default_group:
            cmd += ["--restricted={}".format(default_group)]
        else:
            # We don't actually know the behaviour of Apollo with no groups
            raise NotImplementedError()
        cmd += [common_name, bo.config.raw['apollo'][args.server]['url'], bo.config.raw['apollo'][args.server]['user'], bo.config.raw['apollo'][args.server]['password']]
        # Force to run if anything has changed since last run (or lock, if no last run)
        exit_code, out, err = runner.run_or_resume_job(cmd=cmd, since='last_run')

        exit_code_all += exit_code

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))
