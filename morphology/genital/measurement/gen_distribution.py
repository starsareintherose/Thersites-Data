import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# read data
df = pd.read_csv('measure_genital.csv')

# create figure and grid
fig = plt.figure(figsize=(15, 12))
gs = GridSpec(2, 3, figure=fig, height_ratios=[1, 1])  # 两行三列

# configure columns and titles
columns = ['epiphallus1', 'epiphallus2', 'epiphallus', 'phallus', 'flagellum']
titles = ['Epiphallus 1', 'Epiphallus 2', 'Epiphallus', 'Phallus', 'Flagellum']

# create axes
axes = []

# first line
for i in range(3):
    ax = fig.add_subplot(gs[0, i])  # first line three subplots
    axes.append(ax)

# second line
for i in range(2):
    ax = fig.add_subplot(gs[1, i + 1])  # second line two subplots
    axes.append(ax)

# draw every subplot
for i, col in enumerate(columns):
    # orphan: kde_kws={'color': '#FFD700', 'alpha': 1, 'linewidth': 3} 
    sns.histplot(df[col], kde=False, stat='density', color='#0057B7', alpha=1, bins=40, ax=axes[i])
    sns.kdeplot(
        data=df,
        x=col,
        ax=axes[i],
        color='#FFD700',
        alpha=1,
        linewidth=3
    )

# adjust layout and save
plt.tight_layout()
plt.savefig("distr_gen.svg", format="svg")
plt.show()

