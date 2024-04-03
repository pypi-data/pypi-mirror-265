#!/bin/bash

ln -sf "$1" input.bam
ln -sf "$2" input.bai
ln -sf "$3" genome.fa

bedtools genomecov -split -ibam input.bam -bg > output.bg

sort -k1,1 -k2,2n output.bg > output.bg.sorted

samtools faidx genome.fa -o genome.fa.fai

bedGraphToBigWig output.bg.sorted genome.fa.fai "$4"
