#!/usr/bin/env python

import argparse
import logging
import sys

from beauris import Beauris, MR_Bot

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def run_deploy_task(task_id, org, job_args, bo, server):
    runner = bo.get_runner('local', org, task_id, server=server)
    cmd = ["python", "-m", "beauris.workflows.local." + task_id] + job_args
    exit_code, stdout, stderr = runner.run_or_resume_job(cmd=cmd)
    return exit_code


def main():
    """
    Setup deployment files
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=str)
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()

    if not bo.config.raw['deploy']['deploy_interface']:
        log.info("Missing deployment params in beauris.yml, skipping docker setup")
        sys.exit(0)

    org = bo.load_organism(args.infile)

    non_standard_deploys = ['apollo']
    deploy_tasks = []
    existing = []
    to_cleanup = []

    log.info("Services to deploy:")
    for serv in org.get_deploy_services(args.server):
        if serv not in non_standard_deploys:
            log.info("  - {}".format(serv))
            deploy_tasks.append("deploy_{}".format(serv))

            tdeployer = bo.get_deployer(serv, args.server, org)
            existing += tdeployer.check_services_to_reload()
            to_cleanup += tdeployer.to_cleanup()

    if not deploy_tasks:
        log.info("No docker service to deploy.")
        sys.exit(0)

    exit_code_all = 0

    job_args = [args.server, args.infile]

    deployer_dock = bo.get_deployer('dockercompose', args.server, org)

    if args.server == "staging":
        log.info("Staging mode, shutting down running UIs")
        deployer_dock.shutdown()
    elif args.server == "production":
        log.info("Production mode, shutting down staging UIs")
        deployer_staging = bo.get_deployer('dockercompose', "staging", org)
        deployer_staging.shutdown()

    log.info("Setting up genome homepage")
    deployer = bo.get_deployer('genomehomepage', args.server, org)
    deployer.write_data()

    log.info("Setting up base docker-compose file")
    deployer_dock.write_data()

    for dep_task in deploy_tasks:
        exit_code_all += run_deploy_task(dep_task, org, job_args, bo, args.server)

    log.info("Starting up application")
    deployer_dock.start(update_existing=existing)

    if to_cleanup:
        deployer_dock.cleanup(to_cleanup)

    if exit_code_all != 0:
        log.error('Some interface setup job failed with exit code {} for {}, see log above.'.format(exit_code_all, org.slug()))
    else:
        mr_bot = MR_Bot()
        # Use interface deployer to get urls
        log_messages = deployer.get_notifications()
        if log_messages:
            mr_bot.write_message("\n\n".join(log_messages))
            log.info('All interface setup jobs succeeded for {}.'.format(org.slug()))

    sys.exit(min(exit_code_all, 255))


if __name__ == '__main__':
    main()
