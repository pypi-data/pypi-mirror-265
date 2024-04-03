#!/usr/bin/env python

# Send an organism archive to a remote Apollo server

import argparse
import logging
import sys
import time

from apollo import ApolloInstance

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def check_organism(wa, slug):
    return wa.organisms.show_organism(slug)


def update_group(wa, cname, gname, perms):
    tries = 0
    not_yet_done = True
    type = 'add' if perms else 'remove'

    while tries < 3 and not_yet_done:
        not_yet_done = False
        try:
            wa.groups.update_organism_permissions(gname, args.cname,
                                                  administrate=False, write=perms, read=perms,
                                                  export=perms)
            return
        except KeyError:
            # You can get a sporadic error from apollo, just retry a bit later
            not_yet_done = True
            time.sleep(10)

        tries += 1
    # Failed after 3 time, raise error
    log.error("Error while updating organism {}: couldn't {} group {}".format(cname, type, gname))


def manage_groups(wa, cname, new_group_name=""):
    expected_permissions = ['WRITE', 'EXPORT', 'READ']

    for group in wa.groups.get_groups():
        if new_group_name and group['name'] == new_group_name:
            if not any([(org['organism'] == cname and org['permissions'] == expected_permissions) for org in group['organismPermissions']]):
                update_group(wa, cname, group['name'], True)
        else:
            if any([(org['organism'] == cname and org.get('permissions')) for org in group['organismPermissions']]):
                update_group(wa, cname, group['name'], False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--restricted', type=str, help="Group for restricting access")
    parser.add_argument('cname', type=str, help="Common name")
    parser.add_argument('url', type=str, help="Apollo server URL")
    parser.add_argument('user', type=str, help="Apollo server user")
    parser.add_argument('password', type=str, help="Apollo server password")
    args = parser.parse_args()

    wa = ApolloInstance(args.url, args.user, args.password)

    new_group_name = ""
    if args.restricted:
        groups = wa.groups.get_groups(name=args.restricted)
        if not groups:
            log.error("Error: Group {} does not exists".format(args.restricted))
            sys.exit(1)
        new_group_name = groups[0]['name']

    manage_groups(wa, args.cname, new_group_name)

    # Raise an error if there were some logged
    if 40 in log._cache and log._cache[40]:
        sys.exit(1)
