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

    if 'build_genoboo' not in org.derived_files.keys() and 'build_genoboo_restricted' not in org.derived_files.keys():
        log.info("No Genoboo to deploy, skipping")
        sys.exit(0)

    log.info("Setting up genoboo")

    runner = bo.get_runner('local', org, 'deploy_genoboo', server=args.server)

    deps = []
    if 'build_genoboo' in org.derived_files:
        deps.append(org.derived_files['build_genoboo'])
    if 'build_genoboo_restricted' in org.derived_files:
        deps.append(org.derived_files['build_genoboo_restricted'])
    runner.task.depends_on = deps

    if runner.task.needs_to_run() and not runner.task.disable_run():

        deployer = bo.get_deployer('genoboo', args.server, org)
        deployer.write_data()


if __name__ == '__main__':
    main()
