import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import scipy.stats as stats
from scipy.stats import gaussian_kde

# Read the dataset and exclude NA values in key columns 
# (If a global cleanup is needed, use dropna after reading, but here we handle NA during plotting)
df = pd.read_csv('measure_shell.csv')

# Compute the height-to-width ratio
df['Height_Width'] = df['Height'] / df['Width']

# Predefine colors for different species
species_colors = {
    'novaehollandiae': '#ff888a',
    'mitchellae': '#48b9ff',
    'darlingtoni': '#75ff66',
    'richmondiana': '#ede100',
    'sp1': '#0057b7',
    'sp2': '#b3b3b3'
}

# Specify the variables to be plotted and their corresponding titles
columns = ['Height', 'Width', 'Height_Width']
titles = ['Height', 'Width', 'Height/Width Ratio']

# Create a figure with a 1x3 grid (3 subplots in total)
fig = plt.figure(figsize=(15, 6))
gs = GridSpec(1, 3, figure=fig)
axes = []
for i in range(1):
    for j in range(3):
        ax = fig.add_subplot(gs[i, j])
        axes.append(ax)

# Plot histograms for each variable: bars are stacked by species
for i, col in enumerate(columns):
    ax = axes[i]
    # Remove NA values for the specified variable and species column
    data = df.dropna(subset=[col, 'name'])
    sns.histplot(
        data=data,
        x=col,
        hue='name',
        bins=40,
        stat='count',
        palette=species_colors,
        multiple='stack',
        edgecolor='none',
        linewidth=0,
        ax=ax
    )

    # Compute KDE (Kernel Density Estimation) and convert it to counts (multiply by sample size)
    x_vals = np.linspace(df[col].min(), df[col].max(), 100)
    kde = gaussian_kde(df[col])
    # To ensure KDE represents the total count, multiply by len(df)
    bin_width = (data[col].max() - data[col].min()) / 40  # Compute bin width
    kde_values = kde(x_vals) * len(data) * bin_width
    # Plot the manually computed KDE curve
    axes[i].plot(x_vals, kde_values, color='#7c7c7c', alpha=0.7, linewidth=3)

    ax.set_title(titles[i])
    ax.set_xlabel('')
    if i != 0:
        ax.legend('')  
plt.tight_layout()
plt.savefig("distr_gen_species_stacked.svg", format="svg")
plt.show()

# Normality test: Use the Shapiro-Wilk test, excluding NA values before performing the test
output_lines = []
output_lines.append("Overall normality test results:")

for col in columns:
    # Perform Shapiro-Wilk test after removing NA values
    stat, p = stats.shapiro(df[col].dropna())
    output_lines.append(f"{col}: statistic={stat:.3f}, p-value={p:.3f}")

output_lines.append("\nNormality test results by species:")
for species in species_colors.keys():
    output_lines.append(f"\nSpecies: {species}")
    subset = df[df['name'] == species]
    for col in columns:
        stat, p = stats.shapiro(subset[col].dropna())
        output_lines.append(f"  {col}: statistic={stat:.3f}, p-value={p:.3f}")

# Print results to the console
for line in output_lines:
    print(line)

# Save the results to a text file
with open("normality_test_results.txt", "w") as f:
    for line in output_lines:
        f.write(line + "\n")

