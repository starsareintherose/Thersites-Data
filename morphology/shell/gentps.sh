#!/bin/bash

tpsfn=$1

readarray -t filename < <(ls *.tif)
readarray -t idnum < <(ls *.tif | sed "s@.tif@@g")
ln_fn=${#filename[@]}
for (( i=0; i<$ln_fn; i++)); do
	echo "LM=0" >> $tpsfn
	echo "IMAGE=${filename[$i]}" >> $tpsfn
	echo "ID=${idnum[$i]}" >> $tpsfn
done
