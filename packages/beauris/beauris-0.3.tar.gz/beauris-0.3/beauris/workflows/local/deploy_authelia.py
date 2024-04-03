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

    deployer = bo.get_deployer('authelia', args.server, org)

    log.info("Setting up access permissions")
    deployer.write_data()


if __name__ == '__main__':
    main()
