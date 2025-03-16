import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np
from scipy.stats import rankdata, norm, shapiro, levene, kruskal
import matplotlib.ticker as mtick 
import matplotlib.colors as mcolors

# Read data
df = pd.read_csv('measure_genital.csv')

# Define a custom color palette
group_colors = {
    'novaehollandiae': '#ff888a',
    'mitchellae': '#48b9ff',
    'darlingtoni': '#75ff66',
    'richmondiana': '#ede100',
    'sp1': '#0057b7',
    'sp2': '#b3b3b3',
}
sns.set_palette(list(group_colors.values()))

# Check if all species have assigned colors
categories = df['species'].unique()
missing_colors = set(categories) - set(group_colors.keys())
if missing_colors:
    print(f"Warning: Missing colors for categories: {missing_colors}")

# Map species to colors
df['color'] = df['species'].map(group_colors)

# Compute ratios
df['fl_ph'] = df['flagellum'] / df['phallus']
df['fl_ep1'] = df['flagellum'] / df['epiphallus1']
df['fl_ep'] = df['flagellum'] / df['epiphallus']
df['fl_ep1+ph'] = df['flagellum'] / (df['epiphallus1'] + df['phallus'])
df['fl_ep+ph'] = df['flagellum'] / (df['epiphallus'] + df['phallus'])
df['ep1_ep'] = df['epiphallus1'] / df['epiphallus']
df['ep+ph'] = df['epiphallus'] + df['phallus']

# Define plot information, each tuple contains column name and plot title
plot_info = [
    ('flagellum', 'Violin Plot of flagellum'),
    ('phallus', 'Violin Plot of phallus'),
    ('epiphallus1', 'Violin Plot of epiphallus1'),
    ('epiphallus2', 'Violin Plot of epiphallus2'),
    ('epiphallus', 'Violin Plot of epiphallus'),
    ('ep+ph', 'Violin Plot of epiphallus+phallus'),
    ('fl_ph', 'Violin Plot of flagellum/phallus'),
    ('fl_ep1', 'Violin Plot of flagellum/epiphallus1'),
    ('fl_ep', 'Violin Plot of flagellum/epiphallus'),
    ('fl_ep1+ph', 'Violin Plot of flagellum/(phallus+epiphallus1)'),
    ('fl_ep+ph', 'Violin Plot of flagellum/(phallus+epiphallus)'),
    ('ep1_ep', 'Violin Plot of epiphallus1/epiphallus'),
]

# -------------------------
# Implement Dunn's test p-value matrix using SciPy (non-parametric post hoc comparison)
def dunn_test_pmatrix(df, col, group_col):
    groups = df[group_col].unique()
    groups = list(groups)
    # Sort groups by mean value
    groups_sorted = sorted(groups, key=lambda g: np.mean(df.loc[df[group_col]==g, col].dropna().values))
    
    # Extract non-missing data and compute overall ranking
    df_nonan = df.dropna(subset=[col]).reset_index(drop=True)
    overall_values = df_nonan[col].values
    overall_ranks = rankdata(overall_values)
    
    # Compute sample size and mean rank for each group (using df_nonan indices)
    group_info = {}
    for g in groups_sorted:
        group_data = df_nonan[df_nonan[group_col] == g]
        n = len(group_data)
        mean_rank = np.mean(overall_ranks[group_data.index])
        group_info[g] = {'n': n, 'mean_rank': mean_rank}
    
    N = len(df_nonan)
    # Construct p-value matrix
    p_matrix = np.ones((len(groups_sorted), len(groups_sorted)))
    for i, g1 in enumerate(groups_sorted):
        for j, g2 in enumerate(groups_sorted):
            if i < j:
                diff = abs(group_info[g1]['mean_rank'] - group_info[g2]['mean_rank'])
                se = np.sqrt((N*(N+1)/12.0) * (1/group_info[g1]['n'] + 1/group_info[g2]['n']))
                z = diff / se
                p_val = 2 * (1 - norm.cdf(z))
                p_matrix[i, j] = p_val
                p_matrix[j, i] = p_val
    return groups_sorted, p_matrix

# Group species based on Dunn's test p-value matrix and assign letters
def dunn_letter_assignment(df, col, group_col, alpha=0.05):
    groups_sorted, p_matrix = dunn_test_pmatrix(df, col, group_col)
    letter_groups = []  # Store groups of species
    group_letters = {}
    for grp in groups_sorted:
        assigned = False
        for i, letter_group in enumerate(letter_groups):
            can_assign = True
            for other in letter_group:
                idx_grp = groups_sorted.index(grp)
                idx_other = groups_sorted.index(other)
                if p_matrix[idx_grp, idx_other] < alpha:
                    can_assign = False
                    break
            if can_assign:
                letter_group.append(grp)
                group_letters[grp] = chr(ord('a') + i)
                assigned = True
                break
        if not assigned:
            new_letter = chr(ord('a') + len(letter_groups))
            letter_groups.append([grp])
            group_letters[grp] = new_letter
    return group_letters


# Create a 4 x 3 subplot layout
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(18, 20))
axes = axes.flatten()

# Specify the display order of species (to keep it consistent across plots)
order = list(group_colors.keys())

for i, (col, title) in enumerate(plot_info):
    ax = axes[i]
    # Create violin plot
    sns.violinplot(
        x='species',
        y=col,
        data=df,
        order=order,
        hue='species',
        palette=group_colors,
        legend=False,
        saturation=1,
        linecolor='none',
        ax=ax)
    sns.stripplot(
        x='species',
        y=col,
        data=df,
        order=order,
        color='grey',     # Set point color to grey
        edgecolor=None,   # No border
        size=3,           # Point size (adjust as needed)
        jitter=True,      # Add jitter to avoid overlapping points
        ax=ax
    )
    ax.set_title(title, fontsize=15)
    ax.set_ylabel('')
    ax.set_xlabel('')
    if i < 9:
        ax.tick_params(labelbottom=False)
    else:
        ticks = ax.get_xticks()
        ax.xaxis.set_major_locator(mtick.FixedLocator(ticks))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontstyle='italic', fontsize=15)
    
    # Format y-axis to two decimal places
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
    for label in ax.get_yticklabels():
        label.set_fontsize(15)
    
    # Use Dunn's test to get group letters
    dunn_groups = dunn_letter_assignment(df, col, 'species', alpha=0.05)
    
    # Add group letters above violin plots
    for j, species in enumerate(order):
        if species not in df['species'].unique():
            continue
        y_max = df.loc[df['species'] == species, col].max()
        offset = (df[col].max() - df[col].min()) * 0.05
        t = ax.text(j, y_max + offset, dunn_groups.get(species, ''),
                    ha='center', va='bottom', color='white', fontsize=20)
        t.set_path_effects([
            path_effects.Stroke(linewidth=4, foreground='black'),
            path_effects.Normal()
        ])
    
plt.tight_layout()
plt.savefig('combined_violin_plots_kw_dunn.svg', format='svg')
plt.show()

