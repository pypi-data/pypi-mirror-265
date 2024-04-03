import argparse
import logging
import re

from BCBio import GFF

import pandas

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gffFile', type=str, help="GFF input file (no functional annotations)")
    parser.add_argument('--outFile', type=str, help="GFF output file (with EggNOG annotations)")
    parser.add_argument('--eggFile', type=str, help="EggNOG file")

    args = parser.parse_args()

    newGFF = open(args.outFile, "w")
    annot = pandas.read_csv(args.eggFile, sep='\t', skiprows=4)[['#query', 'Description', 'Preferred_name']]
    for scaff in GFF.parse(open(args.gffFile)):
        for feat in scaff.features:
            if feat.id in annot['#query'].values.tolist():
                n = list(annot['#query']).index(feat.id)
                # Remove unauthorized characters
                pref_name = re.sub("[\n\t\\%;=&,]", ' ', annot['Preferred_name'][n])
                desc = re.sub("[\n\t\\%;=&,]", ' ', annot['Description'][n])
                feat.qualifiers['em_Preferred_name'] = pref_name
                feat.qualifiers['em_Description'] = desc
        GFF.write([scaff], newGFF)
