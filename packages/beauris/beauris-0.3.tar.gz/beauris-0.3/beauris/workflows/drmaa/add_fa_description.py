import argparse
import logging
import re

from Bio import SeqIO

import pandas

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def add_description_in_fa(infile, outfile, annotfile):

    Annot = pandas.read_csv(annotfile, sep='\t', skiprows=4)[['#query', 'Description', 'Preferred_name']]
    with open(infile, 'r') as Fasta, open(outfile, 'w') as newFasta:
        fasta = SeqIO.parse(Fasta, 'fasta')
        for fasta_seq in fasta:
            if (Annot['#query'].eq(fasta_seq.id)).any():
                if len(Annot.loc[Annot['#query'] == fasta_seq.id].values[0][1]) > 100:
                    # Description is more than 100 char
                    fasta_seq.description = fasta_seq.description + '|em_Preferred_name=' + Annot.loc[Annot['#query'] == fasta_seq.id].values[0][2] + '|em_Description=' + re.sub(
                        "[\n>]", ' ',
                        Annot.loc[Annot['#query'] == fasta_seq.id].values[0][1][:100]) + ' (truncated)'
                else:
                    fasta_seq.description = fasta_seq.description + '|em_Preferred_name=' + Annot.loc[Annot['#query'] == fasta_seq.id].values[0][2] + '|em_Description=' + re.sub(
                        "[\n>]", ' ',
                        Annot.loc[Annot['#query'] == fasta_seq.id].values[0][1])
                    SeqIO.write(fasta_seq, newFasta, 'fasta')
            SeqIO.write(fasta_seq, newFasta, 'fasta')


def main():
    """
       Annotate a fasta file with a given eggnog annotation
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str, help="fasta file")
    parser.add_argument("--outfile", type=str, help="enriched fasta file with the eggnog annotation")
    parser.add_argument('--annotfile', type=str, help="annotation eggnog")
    args = parser.parse_args()

    log.info("Annotate {} with the given annotation {}".format(args.infile, args.annotfile))
    add_description_in_fa(args.infile, args.outfile, args.annotfile)


if __name__ == '__main__':
    main()
