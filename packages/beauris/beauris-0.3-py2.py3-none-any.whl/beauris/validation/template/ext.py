# -*- coding: utf-8 -*-

import logging
import os
import re

from pykwalify.errors import SchemaError

import requests

log = logging.getLogger(__name__)


def is_file(value, rule_obj, path):
    if not path.startswith("/"):
        raise SchemaError("Path {} is not an absolute path".format(value))
    if os.path.isfile(value):
        return True
    elif os.path.isdir(value):
        raise SchemaError("Path {} is a directly".format(value))
    else:
        _validate_path_exists(value)
    raise SchemaError("Path {} is not a file".format(value))


def is_dir(value, rule_obj, path):
    if os.path.isdir(value):
        return True

    raise SchemaError("Path {} is not a directory".format(value))


def is_valid_name(value, rule_obj, path):
    # Only accept alphanumericals & - & _
    if re.match(r'^[A-Za-z0-9_-]+$', value):
        return True
    raise SchemaError("Name {} is not a valid internal name".format(value))


def ext_onto_organism(value, rule_obj, path):
    log.debug("value: %s", value)
    log.debug("rule_obj: %s", rule_obj)
    log.debug("path: %s", path)
    # TODO: Better management when EBI is down
    return True
    # return _validate_ontological_term(value, "NCBITAXON")


def _validate_path_exists(file_path, symlink=False):
    current_path = "/"
    for subpath in file_path.split("/"):
        current_path = os.path.join(current_path, subpath)
        if not os.path.exists(current_path):
            if current_path == file_path:
                if not os.path.islink(file_path):
                    if symlink:
                        raise SchemaError("Error with link {}. Linked file {} does not exists.".format(symlink, file_path))
                    else:
                        raise SchemaError("Path {} is not a file".format(file_path))
                continue
            if symlink:
                raise SchemaError("Error with link {}. In linked file {}: directory {} does not exist, or permissions on containing folder are wrong.".format(symlink, file_path, current_path))
            else:
                raise SchemaError("File {} not found: directory {} does not exist, or permissions on containing folder are wrong.".format(file_path, current_path))
    # Do the same for link target
    if os.path.islink(file_path):
        _validate_path_exists(os.readlink(file_path), symlink=file_path)


def _validate_ontological_term(term, ontology, root_term_iri=""):
    base_path = "http://www.ebi.ac.uk/ols/api/search"
    body = {
        "q": term,
        "ontology": ontology.lower(),
        "type": "class",
        "exact": True,
        "queryFields": ["label", "synonym"]
    }
    if root_term_iri:
        body["childrenOf"] = root_term_iri
    r = requests.get(base_path, params=body)
    res = r.json()

    log.info(res["response"])
    if not res["response"]["numFound"] == 1:
        return 'Term {} not found in ontology {}'.format(term, ontology)
    return True
