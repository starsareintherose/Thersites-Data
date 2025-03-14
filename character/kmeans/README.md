# K means clustering

The script aims to run K means clustering for K values from 2 to 10 and plot the Silhouette Score for each K value. The script will also plot the clusters for the best K value.

## NTS

Use tpsRelw to generate the matrix

Input: `Data` - select the tps file 

Compute: `Consensus` - `Partial warps` - `Relative warps` 

Display: `Relative warps` - `File` - `Save scores`

First, it need to be converted to csv file using `nts2csv.py` script.

Then it can use `lm_nts.py` to run the K means clustering.

## TPS

This has been implemented in `lm_tps.py` script. Compared to `nts2csv.py`, it has been modified to read the TPS file directly and perfrom Generalized Procrustes Analysis.

## Bar plot

The script `barchart.py` can be used to plot the bar chart for the occurence of each species in the clusters.

## Usage

```bash
bash run.sh
```
