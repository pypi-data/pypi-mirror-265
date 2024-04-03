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

    if 'build_elasticsearch' not in org.derived_files.keys():
        log.info("No Elasticsearch to deploy, skipping")
        sys.exit(0)

    deployer = bo.get_deployer('elasticsearch', args.server, org)

    log.info("Setting up elasticsearch")

    runner = bo.get_runner('local', org, 'deploy_elasticsearch', server=args.server)
    deps = [org.derived_files['build_elasticsearch']]
    runner.task.depends_on = deps

    if runner.task.needs_to_run() and not runner.task.disable_run():
        deployer.write_data()


if __name__ == '__main__':
    main()
