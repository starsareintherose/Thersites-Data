# Molecular Analysis

## SNP Analysis

Obtain the SNP csv file from the DArT company, then run the R script, it will generate fasta file.

```bash
Rscript Thersites.R
```

## Model selection

```bash
modeltest-ng -i gl_output_rmq.fasta -d nt -T raxml -o G16 -c 16 
```

## Maximum Likelihood Phylogenetic Analysis

```bash
raxml-ng --all --msa gl_output_rmq.fasta --model HKY+I+G16 --bs-trees 1000 --threads 40
```

## Bayesian Phylogenetic Analysis

```bash
nohup mpirun -np 4 mb -i mimi.nex &
```

## Maxmimum Parsimony Phylogenetic Analysis

```bash
# run tnt
script_file=/usr/share/tnt/tnt_script/guoyi.run
input_file=mimi.tnt
tnt run $script_file $input_file dna eiw 12 str 5 EIW,
tnt run $script_file $input_file dna iw 12 str 5 IW,
tnt run $script_file $input_file dna ew 0 str 5 EW,

# convert tnt output to figtree format
for type in EIW EW IW
do
tnt2figtree $type.resample.tre $type.resample.figtree
done
```
