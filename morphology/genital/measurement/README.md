# Genital Length Measurement

Measurements were taken using FIJI.

## FIJI

`File` -> `Open` -> Select the image

Right click `*Straight*` -> Select `*Segmented Line*`

`Analyze` -> `Measure` -> Get the `Length`

## Python

```bash
for pyscript in gen_distribution.py gen_scatter_plot.py gen_violin_plot.py; do
    python3 $pyscript
done
```

