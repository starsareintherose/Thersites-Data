import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import scipy.stats as stats
from scipy.stats import gaussian_kde

# Load data and exclude NA values in key columns 
df = pd.read_csv('measure_genital.csv')

# Compute ep+ph
df['ep+ph'] = df['epiphallus'] + df['phallus']
df['fl_ph'] = df['flagellum'] / df['phallus']
df['fl_ep1'] = df['flagellum'] / df['epiphallus1']
df['fl_ep'] = df['flagellum'] / df['epiphallus']
df['fl_ep1+ph'] = df['flagellum'] / (df['epiphallus1'] + df['phallus'])
df['fl_ep+ph'] = df['flagellum'] / (df['epiphallus'] + df['phallus'])
df['ep1_ep'] = df['epiphallus1'] / df['epiphallus']

# Predefined species color mapping
species_colors = {
    'novaehollandiae': '#ff888a',
    'mitchellae': '#48b9ff',
    'darlingtoni': '#75ff66',
    'richmondiana': '#ede100',
    'sp1': '#0057b7',
    'sp2': '#b3b3b3'
}

# Specify variables to plot and their titles
columns = ['flagellum', 'phallus', 'epiphallus1', 'epiphallus2', 'epiphallus', 'ep+ph', 
           'fl_ph', 'fl_ep1', 'fl_ep', 'fl_ep1+ph', 'fl_ep+ph', 'ep1_ep']
titles = ['Flagellum', 'Phallus', 'Epiphallus 1', 'Epiphallus 2', 'Epiphallus', 'Epiphallus + Phallus', 
          'Flagellum / Phallus', 'Flagellum / Epiphallus 1', 'Flagellum / Epiphallus', 
          'Flagellum / (Epiphallus 1 + Phallus)', 'Flagellum / (Epiphallus + Phallus)', 
          'Epiphallus 1 / Epiphallus']

# Create a figure with a 4x3 grid (12 subplots)
fig = plt.figure(figsize=(15, 20))
gs = GridSpec(4, 3, figure=fig)
axes = []
for i in range(4):
    for j in range(3):
        ax = fig.add_subplot(gs[i, j])
        axes.append(ax)

# Plot histograms for each variable, stacking bars by species
for i, col in enumerate(columns):
    ax = axes[i]
    # Exclude NA values in the specified variable and species column
    data = df.dropna(subset=[col, 'species'])
    data = data[np.isfinite(data[col])]
    sns.histplot(
        data=data,
        x=col,
        hue='species',
        bins=40,
        stat='count',
        palette=species_colors,
        multiple='stack',
        edgecolor='none',
        linewidth=0,
        ax=ax
    )

    # Compute KDE and scale it to match histogram counts
    x_vals = np.linspace(data[col].min(), data[col].max(), 100)
    kde = gaussian_kde(data[col])
    # Multiply KDE by sample size and bin width to match histogram scale
    bin_width = (data[col].max() - data[col].min()) / 40  
    kde_values = kde(x_vals) * len(data) * bin_width
    # Plot the KDE curve
    axes[i].plot(x_vals, kde_values, color='#7c7c7c', alpha=0.7, linewidth=3)
    ax.set_title(titles[i])
    ax.set_xlabel('')
    if i != 0:
        ax.legend('')
        
plt.tight_layout()
plt.savefig("distr_gen_species_stacked.svg", format="svg")
plt.show()

# Normality test: Shapiro-Wilk test, performed after excluding NA values
output_lines = []
output_lines.append("Overall normality test results:")

for col in columns:
    # Perform Shapiro-Wilk test after removing NA values
    stat, p = stats.shapiro(df[col].dropna())
    output_lines.append(f"{col}: statistic={stat:.3f}, p-value={p:.3f}")

output_lines.append("\nNormality test results by species:")
for species in species_colors.keys():
    output_lines.append(f"\nSpecies: {species}")
    subset = df[df['species'] == species]
    for col in columns:
        stat, p = stats.shapiro(subset[col].dropna())
        output_lines.append(f"  {col}: statistic={stat:.3f}, p-value={p:.3f}")

# Print results to console
for line in output_lines:
    print(line)

# Save results to a file
with open("normality_test_results.txt", "w") as f:
    for line in output_lines:
        f.write(line + "\n")

