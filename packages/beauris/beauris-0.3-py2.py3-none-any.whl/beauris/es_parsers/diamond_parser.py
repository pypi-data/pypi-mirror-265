import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class DiamondParser():

    def __init__(self, beauris_annot, protein_dict):
        self.annotation = beauris_annot
        self.protein_dict = protein_dict

    def parse(self):
        if 'func_annot_bipaa' in self.annotation.tasks:
            diamond_file = self.annotation.get_derived_path('diamond')
        elif 'func_annot_orson' in self.annotation.tasks:
            diamond_file = self.annotation.get_derived_path('diamond_xml')
        else:
            return self.protein_dict

        tree = ET.ElementTree(file=diamond_file)
        for iteration in tree.iter(tag="Iteration"):
            self._manage_iteration(iteration)

        return self.protein_dict

    def _manage_iteration(self, iteration):
        protein_id = None
        hit_ids = set()
        hit_desc = set()

        for child in iteration:
            if child.tag == 'Iteration_query-def':
                protein_id = child.text
            elif child.tag == 'Iteration_hits':
                for hit in child:
                    if hit.tag == "Hit":
                        for subchild in hit:
                            if subchild.tag == "Hit_id":
                                hit_ids.add(subchild.text)
                            elif subchild.tag == "Hit_def":
                                hit_desc.add(subchild.text)
                            elif subchild.tag == "Hit_accession":
                                hit_ids.add(subchild.text)
        if not protein_id:
            logger.warn("Missing protein ID in xml, skipping iteration")
            return
        if protein_id not in self.protein_dict:
            logger.warn("{} - linked mRNA not in GFF file, skipping".format(protein_id))
            return
        self.protein_dict[protein_id]['diamond_ids'].update(hit_ids)
        self.protein_dict[protein_id]['diamond_terms'].update(hit_desc)
