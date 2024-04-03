#!/usr/bin/env python
import argparse
import logging
import os
import sys

from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    # We need to check for both staging and production
    if 'elasticsearch' not in org.get_deploy_services("staging") and 'elasticsearch' not in org.get_deploy_services("production"):
        log.info('Elasticsearch is not required for {}'.format(org.slug()))
        sys.exit(0)

    if not (org.assemblies and any([ass.annotations for ass in org.assemblies])):
        log.error('At least one assembly and one annotation is required for Elasticsearch')
        sys.exit(0)

    task_id = "build_elasticsearch"
    runner = bo.get_runner('local', org, task_id)
    script_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./"))

    exit_code = 0
    log.info("Running build elasticsearch for {}".format(org.pretty_name()))

    # Run in a subprocess to capture stdout/stderr + exit code
    cmd = ["python", "{}/run_build_elasticsearch.py".format(script_dir), args.infile]
    exit_code, out, err = runner.run_or_resume_job(cmd=cmd)

    if runner.task.has_run and exit_code == 0:
        exit_code += runner.task.check_expected_outputs()

    if exit_code != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code, 255))
