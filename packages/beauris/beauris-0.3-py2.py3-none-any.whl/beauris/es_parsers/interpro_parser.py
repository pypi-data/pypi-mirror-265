import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class InterproParser():

    def __init__(self, beauris_annot, protein_dict):
        self.annotation = beauris_annot
        self.protein_dict = protein_dict

    def parse(self):
        if 'func_annot_bipaa' in self.annotation.tasks:
            interpro_file = self.annotation.get_derived_path('interproscan')
        elif 'func_annot_orson' in self.annotation.tasks:
            interpro_file = self.annotation.get_derived_path('interproscan_tsv')
        else:
            return self.protein_dict

        with open(interpro_file, 'r') as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if row[0].startswith("#"):
                    continue
                protein_id = row[0]
                sig_id = row[4]
                sig_desc = row[5]
                interpro_id = row[11]
                interpro_desc = row[12]
                if protein_id not in self.protein_dict:
                    logger.warn("{} - linked mRNA not in GFF file, skipping".format(protein_id))
                    continue
                if sig_id != "-":
                    self.protein_dict[protein_id]['interpro_ids'].add(sig_id)
                if sig_desc != "-":
                    self.protein_dict[protein_id]['interpro_terms'].add(sig_desc)
                if interpro_id != "-":
                    self.protein_dict[protein_id]['interpro_ids'].add(interpro_id)
                if interpro_desc != "-":
                    self.protein_dict[protein_id]['interpro_terms'].add(interpro_desc)

        return self.protein_dict
