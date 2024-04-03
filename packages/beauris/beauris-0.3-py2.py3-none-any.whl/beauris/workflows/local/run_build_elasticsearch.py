#!/usr/bin/env python
import argparse
import logging
import sys
import tarfile
import time

from beauris import Beauris
from beauris.es_parsers import DiamondParser, EggnogParser, GffParser, InterproParser

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def unpack_gene(gene):
    data = {}
    for key, value in gene.items():
        data[key] = list(value) if isinstance(value, set) else value
    return data


def data_generator(data):
    for gene in data.values():
        yield {
            "_index": "genes",
            "_source": unpack_gene(gene)
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    # Maybe we could manage it better?
    mapping = {
        "properties": {
            "gene_id": {"type": "text", "analyzer": "standard"},
            "organism": {"type": "text", "analyzer": "standard"},
            "organism_slug": {"enabled": False},
            "assembly": {"enabled": False},
            "assembly_slug": {"enabled": False},
            "annotation": {"type": "text", "analyzer": "keyword"},
            "eggnog_og_terms": {"type": "text", "analyzer": "standard"},
            "go_ids": {"type": "text", "analyzer": "standard"},
            "go_terms": {"type": "text", "analyzer": "standard"},
            "interpro_ids": {"type": "text", "analyzer": "standard"},
            "interpro_terms": {"type": "text", "analyzer": "standard"},
            "diamond_ids": {"type": "text", "analyzer": "standard"},
            "diamond_terms": {"type": "text", "analyzer": "standard"},
            "public": {"type": "boolean"}
        }
    }

    # We need to check for both staging and production
    if 'elasticsearch' not in org.get_deploy_services("staging") and 'elasticsearch' not in org.get_deploy_services("production"):
        log.info('Elasticsearch is not required for {}'.format(org.slug()))
        sys.exit(0)

    if not (org.assemblies and any([ass.annotations for ass in org.assemblies])):
        log.error('At least one assembly and one annotation is required for Elasticsearch')
        sys.exit(0)

    task_id = "build_elasticsearch"
    runner = bo.get_runner('local', org, task_id)
    config_task = runner.get_job_specs(task_id)

    re_protein = config_task.get("re_protein", r'\1-P\2')
    re_protein_capture = config_task.get("re_protein_capture", r"^(.*?)-R([A-Z]+)$")
    go_file = config_task.get("goterms_file")
    to_index = config_task.get("to_index", [])

    es_url = "http://localhost:9200"
    es = Elasticsearch(es_url)

    # Try to delete the indice beforehand, just in case it's a multiple organisms job
    es.indices.delete(index="genes", ignore_unavailable=True)

    es.indices.create(index="genes", mappings=mapping)

    # Check if org is public
    slug = org.slug()

    for ass in org.assemblies:
        for annot in ass.annotations:
            is_public = not bool(annot.restricted_to)
            data = GffParser(annot, re_protein=re_protein, re_protein_capture=re_protein_capture, is_public=is_public, slug=slug).parse()
            log.info("Number of genes indexed: " + str(len(data)))
            if 'interpro' in to_index:
                log.info("Parsing interproscan")
                data = InterproParser(annot, data).parse()
            if 'diamond' in to_index:
                log.info("Parsing diamond")
                data = DiamondParser(annot, data).parse()
            if 'eggnog' in to_index:
                log.info("Parsing Eggnog")
                data = EggnogParser(annot, data, go_file).parse()

            bulk(es, data_generator(data), refresh='wait_for')

    data_path = "/usr/share/elasticsearch/data/"
    archive_path = org.get_derived_path('build_elasticsearch')

    # Wait a bit before creating the archive
    time.sleep(20)

    with tarfile.open(archive_path, 'w:bz2') as outtarf:
        outtarf.add(data_path, arcname="data")
