import re
from urllib.parse import quote_plus

from BCBio import GFF


class GffParser():

    def __init__(self, beauris_annot, re_protein="r\1-P\2", re_protein_capture=r"^(.*?)-R([A-Z]+)$", is_public=False, slug=""):
        self.re_protein = re_protein
        self.re_protein_capture = re_protein_capture
        self.annotation = beauris_annot
        self.is_public = is_public
        self.slug = slug

    def _generate_protein(self, mrna_id):
        protein_id = re.sub(self.re_protein_capture, self.re_protein, mrna_id)
        return protein_id

    def parse(self):
        annot_version = self.annotation.version
        assembly_version = self.annotation.assembly.version
        assembly_slug = self.annotation.assembly.slug(short=True)
        genome = self.annotation.assembly.organism.pretty_name()
        gff_file = self.annotation.get_derived_path('fixed_gff')
        data = {}

        # Parse GFF, store info in dict
        for scaff in GFF.parse(gff_file):
            for topfeat in scaff.features:
                # Only check mRNA for now
                # TODO: get gene attributes also?
                if topfeat.type != 'gene':
                    continue
                for mrna in topfeat.sub_features:
                    mrna_id = quote_plus(mrna.qualifiers['ID'][0], safe=":/ ")
                    gene_id = quote_plus(mrna.qualifiers['Parent'][0], safe=":/ ")
                    protein_id = self._generate_protein(mrna_id)
                    data[protein_id] = {
                        "organism": genome,
                        "assembly": assembly_version,
                        "annotation": annot_version,
                        "gene_id": gene_id,
                        "interpro_terms": set(),
                        "diamond_terms": set(),
                        "diamond_ids": set(),
                        "interpro_ids": set(),
                        "go_ids": set(),
                        "go_terms": set(),
                        "eggnog_og_terms": set(),
                        "public": self.is_public,
                        "organism_slug": self.slug,
                        "assembly_slug": assembly_slug
                    }

        return data
