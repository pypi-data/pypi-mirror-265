import logging
import os
import shutil

from beauris.organism import Organism

import yaml

from .basedeployer import BaseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


# Tidy up the yaml dump (indent lists starts)
class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


class AutheliaDeployer(BaseDeployer):

    service_name = 'authelia'

    def __init__(self, config, server, entity):

        self.supported_entity_types = (Organism)

        BaseDeployer.__init__(self, config, server, entity)

    def write_data(self, apply=True):
        # only authelia for now
        has_changed = self._manage_authelia_conf()
        if apply:
            if has_changed:
                log.info("Authelia conf has changed, reloading docker")
                extravars = {
                    "service_name": self.config.deploy[self.server]['options'].get("authelia_service", "")
                }
                self._run_playbook("playbook_update.yml", extravars)
            else:
                log.info("No changes in authelia configuration")

    def _manage_authelia_conf(self):
        conf_path = self.config.deploy[self.server]['options']['authelia_conf']

        with open(conf_path, "r") as f:
            yml_str = f.read()
            try:
                yml_data = yaml.safe_load(yml_str)
            except yaml.YAMLError:
                log.error("Invalid authelia conf file : {}".format(conf_path))
                return False

        original_rules = yml_data['access_control']['rules']

        restriction = self.entity.get_restricted_tos()
        mixed = self.entity.has_mixed_data()

        if restriction:
            restriction = restriction[0]  # We only support 1 group per organism (for now)
            if mixed:
                rules = self.get_rules(original_rules, None, self.netloc, self.url_prefix, self.sub_url)
                rules = self.get_rules(rules, restriction, self.netloc_restricted, self.url_prefix_restricted, self.sub_url)
            else:
                rules = self.get_rules(original_rules, restriction, self.netloc, self.url_prefix, self.sub_url)
        else:
            rules = self.get_rules(original_rules, None, self.netloc, self.url_prefix, self.sub_url)

        # We might still have some old "restricted" rules from before, make sure get rid of them
        if not self.entity.has_mixed_data():
            rules = self.remove_mixed_rules(rules, self.netloc_restricted, self.url_prefix_restricted, self.sub_url)

        # Check if we need to update the file
        comp_orig = sorted([str(x) for x in original_rules])
        comp_new = sorted([str(x) for x in rules])
        has_changed = comp_orig != comp_new

        if has_changed:
            # Make a copy beforehand..
            shutil.copyfile(conf_path, conf_path + ".backup")
            yml_data['access_control']['rules'] = rules
            # Write to a temp file & rename it to avoid issues
            with open(conf_path + ".temp", 'w') as f:
                f.write(yaml.dump(yml_data, Dumper=Dumper, default_flow_style=False, sort_keys=False))
            os.replace(conf_path + ".temp", conf_path)

        # Merge authelia conf files if needed
        if 'authelia_conf_merge_with' in self.config.deploy[self.server]['options'] and 'authelia_conf_merge_to' in self.config.deploy[self.server]['options']:
            merge_with = self.config.deploy[self.server]['options']['authelia_conf_merge_with']
            merge_to = self.config.deploy[self.server]['options']['authelia_conf_merge_to']

            rules_str = yaml.dump({'access_control': {'rules': rules}}, Dumper=Dumper, default_flow_style=False, sort_keys=False)
            rules_str = rules_str.split("\n", 2)[2]  # Keep only the list of rules, properly indented

            with open(merge_with, 'r') as not_merged:
                with open(merge_to, 'w') as merged:
                    not_merged_str = not_merged.read()
                    merged_str = not_merged_str.replace('# __BEAURIS_RULES__', rules_str)  # TODO document this
                    merged.write(merged_str)

        return has_changed

    def get_rules(self, original_rules, restricted_to, netloc, url_prefix, sub_url):
        rules = []
        existing_deny = existing_allow = None
        for rule in original_rules:
            # Keep internal rules
            if 'networks' in rule:
                rules.append(rule)
            elif rule['domain'] == netloc and any([self.match_rule(url_prefix, sub_url, ressource) for ressource in rule.get('resources', [])]):
                # Remove rules if no restrictions now
                if not restricted_to:
                    continue
                if rule['policy'] == "deny":
                    existing_deny = rule
                elif rule.get('subject', "") == "group:{}".format(restricted_to):
                    existing_allow = rule
            else:
                rules.append(rule)

        if restricted_to:
            if existing_allow is None:
                rules.append({
                    'domain': netloc,
                    'resources': ["^{}/{}/.*$".format(url_prefix, sub_url)],
                    'policy': 'one_factor',
                    'subject': "group:{}".format(restricted_to)
                })
            else:
                rules.append(existing_allow)

            if existing_deny is None:
                rules.append({
                    'domain': netloc,
                    'resources': ["^{}/{}/.*$".format(url_prefix, sub_url)],
                    'policy': 'deny'
                })
            else:
                rules.append(existing_deny)

        return rules

    def remove_mixed_rules(self, original_rules, netloc, url_prefix, sub_url):
        rules = []
        for rule in original_rules:
            # Keep internal rules
            if 'networks' in rule:
                rules.append(rule)
            elif rule['domain'] == netloc and any([self.match_rule(url_prefix, sub_url, ressource) for ressource in rule.get('resources', [])]):
                # Remove rules if no restrictions now
                continue
            else:
                rules.append(rule)

        return rules

    def match_rule(self, url_prefix, sub_url, rule):
        # We need to check the full rule, and not just 'blocks', because 'sp' rules will match 'sp_restricted' otherwise
        created_rule = "^{}/{}/.*$".format(url_prefix, sub_url)
        return rule == created_rule
