import pandas as pd
import matplotlib.pyplot as plt

# read data
df = pd.read_csv('measure_shell.csv')

# custom color mapping
group_colors = {
    'darlingtoni': '#75ff66',
    'mitchellae': '#48b9ff',
    'novaehollandiae': '#ff888a',
    'richmondiana': '#ede100',
    'sp1': '#0057b7',
    'sp2': '#b3b3b3',
}

# check missing colors
categories = df['name'].unique()
missing_colors = set(categories) - set(group_colors.keys())
if missing_colors:
    print(f"Warning: Missing colors for categories: {missing_colors}")

# map color to each category
df['color'] = df['name'].map(group_colors)

# plot scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(df['Width'], df['Height'], c=df['color'], alpha=1, marker='o')

# add legend for each group
for name, color in group_colors.items():
    plt.scatter([], [], color=color, label=name, marker='o')  # empty scatter plot for legend
plt.legend(title='name')

# add lines
x_values = df['Width']
plt.plot(x_values, 0.8 * x_values, color='black', linestyle='--', label='y=0.8x')
plt.plot(x_values, 0.7 * x_values, color='grey', linestyle='--', label='y=0.7x')

# add labels
plt.xlabel('Width(cm)')
plt.ylabel('Height(cm)')
plt.title('Scatter Plot of Shell Width and Height')

# add legend for lines and categories
plt.legend(title='Categories and Lines')

# save figure
plt.savefig('shell_width_height.svg', format='svg')

# show plot
plt.show()

