#!/usr/bin/env python

import argparse
import logging
import os
import sys

from beauris import MR_Bot

from pykwalify.core import Core
from pykwalify.errors import SchemaError

import yaml

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str, help="Organism yml file")

    args = parser.parse_args()

    errors = 0

    mr_bot = MR_Bot()

    with open(args.infile, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError:
            log.error("Invalid Beauris config yaml file : {}".format(args.infile))
            mr_bot.write_message("Invalid Beauris config yaml file : {}".format(args.infile))
            raise

    schema_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../validation/template')
    c = Core(source_file=args.infile, schema_files=[os.path.join(schema_path, 'schema.yaml')], extensions=[os.path.join(schema_path, 'ext.py')])
    try:
        c.validate(raise_exception=True)
    except SchemaError as e:
        mess = "Error validating yml file:\n{}".format(e.msg)
        mr_bot.write_message(mess)
        raise e

    error_logs = []

    if 'extra_files' in data:
        xtra_names = []
        for xtra in data['extra_files']:
            if xtra['name'] in xtra:
                org_name = data['genus'] + data['species']
                error = "Found a duplicate extra_file name for organism {}: {}".format(org_name, xtra['name'])
                log.error(error)
                error_logs.append(error)
                errors += 1
            xtra_names.append(xtra['name'])

    if 'assemblies' in data:
        ass_versions = []
        for ass in data['assemblies']:
            if ass['version'] in ass_versions:
                error = "Found a duplicate assembly version: {}".format(ass['version'])
                log.error(error)
                error_logs.append(error)
                errors += 1
            ass_versions.append(ass['version'])

            if 'annotations' in ass:
                annot_versions = []
                for annot in ass['annotations']:
                    if annot['version'] in annot_versions:
                        error = "Found a duplicate annotation version for assembly {}: {}".format(ass['version'], annot['version'])
                        log.error(error)
                        error_logs.append(error)
                        errors += 1
                    annot_versions.append(annot['version'])

                    if 'expression_data' in annot:
                        xp_names = []
                        for xp in annot['expression_data']:
                            if xp['name'] in xp_names:
                                error = "Found a duplicate expression_data name for annotation {}: {}".format(annot['version'], xp['name'])
                                log.error(error)
                                error_logs.append(error)
                                errors += 1
                            xp_names.append(xp['name'])

            if 'tracks' in ass:
                track_names = []
                for track in ass['tracks']:
                    if track['name'] in track_names:
                        error = "Found a duplicate track name for assembly {}: {}".format(ass['version'], track['name'])
                        log.error(error)
                        error_logs.append(error)
                        errors += 1
                    track_names.append(track['name'])

            if 'extra_files' in ass:
                xtra_names = []
                for xtra in ass['extra_files']:
                    if xtra['name'] in xtra:
                        error = "Found a duplicate extra_file name for assembly {}: {}".format(ass['version'], xtra['name'])
                        log.error(error)
                        error_logs.append(error)
                        errors += 1
                    xtra_names.append(xtra['name'])

    if errors > 0:
        log.error("There were some errors in the {} organism config file".format(args.infile))
        error_msg = "Error while linting file:\n" + "\n".join(error_logs)
        mr_bot.write_message(error_msg)
        sys.exit(1)
