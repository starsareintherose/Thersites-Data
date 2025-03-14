# Kruskal-Wallis Phylogeny

This step uses the phylogenetic topology and morphological data to test which lineage's morphological character is significant or not using the Kruskal-Wallis test.

## Usage

### Running the script

To execute the pipeline, simply run:

```bash
bash run.sh
```

Alternatively, you can manually run the Python script with specific arguments:

```bash
python script.py -t tree.nwk -c data.csv --svg1 output_with_labels.svg --svg2 output_without_labels.svg --table pvalues_table.csv
```

### Arguments

| Argument         | Description |
|-----------------|-------------|
| `-t`, `--tree`  | Path to the Newick format tree file. |
| `-c`, `--csv`   | Path to the CSV file containing morphological data. Must include a `seq` column matching tree tips. |
| `--svg1`        | Output SVG file for the tree with node labels (default: `tree_with_labels.svg`). |
| `--svg2`        | Output SVG file for the tree without node labels (default: `tree_without_labels.svg`). |
| `--table`       | Output CSV file for Kruskal-Wallis test p-values (default: `pvalues_table.csv`). |

## Input Data Format

### Tree File (`tree.nwk`)

The input tree file must be in Newick format, for example:

```
((A,B),(C,D));
```

### CSV Data File (`data.csv`)

The CSV file should contain morphological data associated with each leaf (taxon) in the tree. Example:

| seq  | Width | Height | phallus | epiphallus1 | epiphallus2 | flagellum |
|------|-------|--------|---------|-------------|-------------|-----------|
| A    | 1.2   | 2.5    | 0.8     | 1.1         | NaN         | 0.9       |
| B    | 1.5   | 2.7    | 0.9     | 1.3         | 1.0         | 1.1       |
| C    | 1.3   | 2.4    | NaN     | 1.0         | 1.2         | 0.8       |
| D    | 1.4   | 2.6    | 0.7     | NaN         | 1.3         | 1.0       |

- The `seq` column must match leaf names in the tree.
- Missing values should be represented as `NaN`.

## Output Files

### `pvalues_table.csv`

This file contains the Kruskal-Wallis test p-values for each node and each morphological variable:

| node_id  | Width | Height | phallus | epiphallus1 | epiphallus2 | flagellum |
|----------|-------|--------|---------|-------------|-------------|-----------|
| Node1    | 0.02  | 0.15   | NaN     | 0.01        | 0.04        | 0.30      |
| Node2    | 0.05  | 0.25   | 0.10    | 0.03        | 0.02        | 0.20      |

- A p-value < 0.05 suggests significant morphological differentiation at that node.
- `NaN` indicates that the test was not performed due to missing or insufficient data.

### `tree_with_labels.svg`

An SVG visualization of the tree where internal nodes are labeled with node IDs and heatmaps represent p-values.

### `tree_without_labels.svg`

Similar to the labeled tree but without node labels, focusing only on heatmaps.

