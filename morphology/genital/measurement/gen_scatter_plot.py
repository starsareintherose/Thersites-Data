import pandas as pd
import matplotlib.pyplot as plt

# read csv file
df = pd.read_csv('measure_genital.csv')

# cutomize colors
group_colors = {
    'darlingtoni': '#75ff66',
    'mitchellae': '#48b9ff',
    'novaehollandiae': '#ff888a',
    'richmondiana': '#ede100',
    'sp1': '#0057b7',
    'sp2': '#b3b3b3',
}

# mapping species to colors
df['color'] = df['species'].map(group_colors)

# create plate
fig, axes = plt.subplots(3, 2, figsize=(15, 15))  # 3 lines 2 rows 
axes = axes.flatten()  

# subplot 1: phallus vs. flagellum
axes[0].scatter(df['phallus'], df['flagellum'], c=df['color'], alpha=1, marker='o')
line1, = axes[0].plot(df['phallus'], 0.5 * df['phallus'], color='black', linestyle='-', label='y=0.50x')
line2, = axes[0].plot(df['phallus'], 0.25 * df['phallus'], color='grey', linestyle='-', label='y=0.25x')
axes[0].set_xlabel('phallus (cm)')
axes[0].set_ylabel('flagellum (cm)')
axes[0].set_title('Phallus vs. Flagellum')

# subplot 2: epiphallus1 vs. flagellum
axes[1].scatter(df['epiphallus1'], df['flagellum'], c=df['color'], alpha=1, marker='o')
axes[1].plot(df['epiphallus1'], 0.5 * df['epiphallus1'], color='black', linestyle='-', label='y=0.50x')
axes[1].plot(df['epiphallus1'], 0.25 * df['epiphallus1'], color='grey', linestyle='-', label='y=0.25x')
axes[1].set_xlabel('epiphallus1 (cm)')
axes[1].set_ylabel('flagellum (cm)')
axes[1].set_title('Epiphallus1 vs. Flagellum')

# subplot 3: epiphallus vs. flagellum
axes[2].scatter(df['epiphallus'], df['flagellum'], c=df['color'], alpha=1, marker='o')
axes[2].plot(df['epiphallus'], 0.5 * df['epiphallus'], color='black', linestyle='-', label='y=0.50x')
axes[2].plot(df['epiphallus'], 0.25 * df['epiphallus'], color='grey', linestyle='-', label='y=0.25x')
axes[2].set_xlabel('epiphallus (cm)')
axes[2].set_ylabel('flagellum (cm)')
axes[2].set_title('Epiphallus vs. Flagellum')

# subplot 4: epiphallus1 + phallus vs. flagellum
x1_values = df['epiphallus1'] + df['phallus']
axes[3].scatter(x1_values, df['flagellum'], c=df['color'], alpha=1, marker='o')
axes[3].plot(x1_values, 0.5 * x1_values, color='black', linestyle='-', label='y=0.50x')
axes[3].plot(x1_values, 0.25 * x1_values, color='grey', linestyle='-', label='y=0.25x')
axes[3].set_xlabel('epiphallus1 + phallus (cm)')
axes[3].set_ylabel('flagellum (cm)')
axes[3].set_title('Epiphallus1 + Phallus vs. Flagellum')

# subplot 5: epiphallus + phallus vs. flagellum
x2_values = df['epiphallus'] + df['phallus']
axes[4].scatter(x2_values, df['flagellum'], c=df['color'], alpha=1, marker='o')
axes[4].set_xlabel('epiphallus + phallus (cm)')
axes[4].set_ylabel('flagellum (cm)')
axes[4].set_title('Epiphallus + Phallus vs. Flagellum')

# subplot 6: epiphallus1 vs. epiphallus2
axes[5].scatter(df['epiphallus1'], df['epiphallus2'], c=df['color'], alpha=1, marker='o')
axes[5].set_xlabel('epiphallus1 (cm)')
axes[5].set_ylabel('epiphallus2 (cm)')
axes[5].set_title('Epiphallus1 vs. Epiphallus2')

# merge legend handles
handles_points = [plt.Line2D([0], [0], color=color, marker='o', linestyle='', label=name) 
           for name, color in group_colors.items()]
handles_lines = [line1, line2]
handles_combined = handles_points + handles_lines
axes[0].legend(handles=handles_combined, loc='upper left')

# merge figures
plt.tight_layout()
plt.savefig('genital_scatter_plots.svg', format='svg')
plt.show()

