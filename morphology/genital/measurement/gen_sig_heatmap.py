import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kruskal
import matplotlib.cm as cm
from matplotlib.colors import Normalize

# Load data
df = pd.read_csv('measure_genital.csv')

# Compute multiple ratios
df['fl_ph'] = df['flagellum'] / df['phallus']
df['fl_ep1'] = df['flagellum'] / df['epiphallus1']
df['fl_ep'] = df['flagellum'] / df['epiphallus']
df['fl_ep1+ph'] = df['flagellum'] / (df['epiphallus1'] + df['phallus'])
df['fl_ep+ph'] = df['flagellum'] / (df['epiphallus'] + df['phallus'])
df['ep1_ep'] = df['epiphallus1'] / df['epiphallus']
df['ep+ph'] = df['epiphallus'] + df['phallus']

# Get all species groups (sorted alphabetically)
groups = sorted(df['species'].unique())

# Function to compute the p-value matrix
def compute_p_matrix(df, ratio_col):
    p_matrix = pd.DataFrame(np.ones((len(groups), len(groups))),
                            index=groups, columns=groups)
    for i, g1 in enumerate(groups):
        for j, g2 in enumerate(groups):
            if i < j:
                vals1 = df[df['species'] == g1][ratio_col]
                vals2 = df[df['species'] == g2][ratio_col]
                stat, p = kruskal(vals1, vals2, nan_policy='omit')
                p_matrix.loc[g1, g2] = p
                p_matrix.loc[g2, g1] = p
    return p_matrix

# Function to convert p-values to significance markers
def p_to_sig(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return ''

# List of ratios to analyze
ratios = ['flagellum', 'phallus', 'epiphallus1', 'epiphallus2', 'epiphallus', 'ep+ph',
          'fl_ph', 'fl_ep1', 'fl_ep', 'fl_ep1+ph', 'fl_ep+ph', 'ep1_ep']

# Create subplots with 4 rows and 3 columns
fig, axes = plt.subplots(4, 3, figsize=(20, 20))
axes = axes.flatten()

# Loop through each ratio and plot a heatmap (without individual color bars)
for i, ratio in enumerate(ratios):
    p_matrix = compute_p_matrix(df, ratio)
    sig_matrix = p_matrix.map(p_to_sig)
    ax = axes[i]
    sns.heatmap(p_matrix, annot=sig_matrix, fmt='', cmap='viridis_r',
                cbar=False, vmin=0, vmax=0.05, ax=ax)
    ax.set_title(f"Significance for '{ratio}'")
    
# Show y-axis labels only for the first column of subplots
for i, ax in enumerate(axes):
    if i not in [0, 3, 6, 9]:
        ax.tick_params(labelleft=False)
    else:
        ax.set_yticklabels(ax.get_yticklabels(), fontstyle='italic')

# Show x-axis labels only for the bottom row of subplots and set italic font
for i, ax in enumerate(axes):
    if i < 9:
        ax.tick_params(labelbottom=False)
    else:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontstyle='italic')

# Adjust subplot layout, reserving space on the right for a unified color bar
plt.tight_layout(rect=[0, 0, 0.95, 1])

# Create a unified color bar
norm = Normalize(vmin=0, vmax=0.05)
sm = cm.ScalarMappable(cmap="viridis_r", norm=norm)
sm.set_array([])

# Add a unified color bar to the right side of the figure
cbar = fig.colorbar(sm, ax=axes, orientation='vertical', fraction=0.05, pad=0.04)
cbar.set_label('p-value')

# Save as an SVG file
plt.savefig('sig_heatmap.svg', format='svg')
plt.show()

