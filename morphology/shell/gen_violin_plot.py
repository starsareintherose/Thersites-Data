import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np
from scipy.stats import rankdata, norm, shapiro, levene, kruskal
import matplotlib.ticker as mtick 
import matplotlib.colors as mcolors

# Read the dataset
df = pd.read_csv('measure_shell.csv')

# Define a custom color palette for species
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
categories = df['name'].unique()
missing_colors = set(categories) - set(group_colors.keys())
if missing_colors:
    print(f"Warning: Missing colors for categories: {missing_colors}")

# Map species to their corresponding colors
df['color'] = df['name'].map(group_colors)

# Compute the height-to-width ratio
df['Height_Width'] = df['Height'] / df['Width']

# Define plot settings: each tuple contains the column name and plot title
plot_info = [
    ('Height', 'Violin Plot of Height'),
    ('Width', 'Violin Plot of Width'),
    ('Height_Width', 'Violin Plot of Height/Width Ratio'),
]

# -------------------------
# Function to compute Dunn’s test p-value matrix (non-parametric post hoc comparison)
def dunn_test_pmatrix(df, col, group_col):
    groups = df[group_col].unique()
    groups = list(groups)
    # Sort groups based on mean values
    groups_sorted = sorted(groups, key=lambda g: np.mean(df.loc[df[group_col]==g, col].dropna().values))
    
    # Extract all non-missing data and compute global ranks
    df_nonan = df.dropna(subset=[col]).reset_index(drop=True)
    overall_values = df_nonan[col].values
    overall_ranks = rankdata(overall_values)
    
    # Compute sample size and mean rank for each group
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

# Function to assign group letters based on Dunn’s test results
def dunn_letter_assignment(df, col, group_col, alpha=0.05):
    groups_sorted, p_matrix = dunn_test_pmatrix(df, col, group_col)
    letter_groups = []  # Stores assigned groups
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


# Create a 1 x 3 grid of subplots
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 6))
axes = axes.flatten()

# Define species order for consistency across plots
order = list(group_colors.keys())

for i, (col, title) in enumerate(plot_info):
    ax = axes[i]
    # Plot violin plot
    sns.violinplot(
        x='name',
        y=col,
        data=df,
        order=order,
        hue='name',
        palette=group_colors,
        legend=False,
        saturation=1,
        linecolor='none',
        ax=ax)
    # Overlay strip plot
    sns.stripplot(
        x='name',
        y=col,
        data=df,
        order=order,
        color='grey',     # Set point fill color to grey
        edgecolor=None,   # No border
        size=3,           # Point size
        jitter=True,      # Add jitter to prevent overlapping
        ax=ax
    )
    ax.set_title(title, fontsize=15)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ticks = ax.get_xticks()
    ax.xaxis.set_major_locator(mtick.FixedLocator(ticks))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontstyle='italic', fontsize=15)
    
    # Format y-axis labels to 2 decimal places
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
    for label in ax.get_yticklabels():
        label.set_fontsize(15)
    
    # Get group letters from Dunn's test
    dunn_groups = dunn_letter_assignment(df, col, 'name', alpha=0.05)
    
    # Add group letters above violin plots
    for j, species in enumerate(order):
        if species not in df['name'].unique():
            continue
        y_max = df.loc[df['name'] == species, col].max()
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

