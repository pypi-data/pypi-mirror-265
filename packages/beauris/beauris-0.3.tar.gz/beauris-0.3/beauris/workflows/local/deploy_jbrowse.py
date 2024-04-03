#!/usr/bin/env python

import argparse
import logging
import sys


from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str)
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()

    if not bo.config.raw['deploy']['deploy_interface']:
        log.info("Skipping docker setup")
        sys.exit(0)

    org = bo.load_organism(args.infile)

    log.info("Setting up jbrowse")

    some_ass_deployed = False

    for ass in org.assemblies:

        if 'jbrowse' not in ass.derived_files.keys() and 'jbrowse_restricted' not in ass.derived_files.keys():
            log.info("No JBrowse to deploy for {}, skipping".format(ass.slug(short=True)))
            continue

        runner = bo.get_runner('local', ass, 'deploy_jbrowse', server=args.server)

        deps = []
        if 'jbrowse' in ass.derived_files:
            deps.append(ass.derived_files['jbrowse'])
        if 'jbrowse_restricted' in ass.derived_files:
            deps.append(ass.derived_files['jbrowse_restricted'])
        runner.task.depends_on = deps

        if runner.task.needs_to_run() and not runner.task.disable_run():
            deployer = bo.get_deployer('jbrowse', args.server, ass)
            deployer.write_data()
            some_ass_deployed = True

    if some_ass_deployed:
        deployer = bo.get_deployer('jbrowse', args.server, org)
        deployer.write_data()


if __name__ == '__main__':
    main()
