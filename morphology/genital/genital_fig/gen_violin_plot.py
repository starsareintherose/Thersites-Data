import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# read data
df = pd.read_csv('measure_genital.csv')

# custom color palette
group_colors = {
    'darlingtoni': '#75ff66',
    'mitchellae': '#48b9ff',
    'novaehollandiae': '#ff888a',
    'richmondiana': '#ede100',
    'sp1': '#0057b7',
    'sp2': '#b3b3b3',
}
sns.set_palette(list(group_colors.values()))

# confirm all categories have colors
categories = df['species'].unique()
missing_colors = set(categories) - set(group_colors.keys())
if missing_colors:
    print(f"Warning: Missing colors for categories: {missing_colors}")

# map species to colors
df['color'] = df['species'].map(group_colors)

# calculate ratios
df['fl_ph'] = df['flagellum'] / df['phallus']
df['fl_ep1'] = df['flagellum'] / df['epiphallus1']
df['fl_ep'] = df['flagellum'] / df['epiphallus']
df['fl_ep1+ph'] = df['flagellum'] / (df['epiphallus1'] + df['phallus'])
df['fl_ep+ph'] = df['flagellum'] / (df['epiphallus'] + df['phallus'])
df['ep1_ep'] = df['epiphallus1'] / df['epiphallus']

# define plot information
plot_info = [
    ('fl_ph', 'violin map of flagellum/phallus'),
    ('fl_ep1', 'violin map of flagellum/epiphallus1'),
    ('fl_ep', 'violin map of flagellum/epiphallus'),
    ('fl_ep1+ph', 'violin map of flagellum/(phallus+epiphallus1)'),
    ('fl_ep+ph', 'violin map of flagellum/(phallus+epiphallus)'),
    ('ep1_ep', 'violin map of epiphallus1/epiphallus'),
]

# create 2 x 3 subplots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
axes = axes.flatten()  # convert axes to 1D array

# draw violin subplots
for i, (col, title) in enumerate(plot_info):
    ax = axes[i]
    sns.violinplot(x='species',
                   y=col,
                   data=df,
                   inner="point",
                   palette=group_colors,
                   saturation=1,
                   linecolor='grey',
                   ax=ax)
    ax.set_title(title)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    # to avoid duplicated legend
    if i != 0:
        leg = ax.get_legend()
        if leg is not None:
            leg.remove()
    else:
        ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig('combined_violin_plots.svg', format='svg')
plt.show()

