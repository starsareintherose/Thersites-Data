import pandas as pd

# read csv
df = pd.read_csv('measure_shell.csv')

# calculate min, max, mean, std of each group
grouped = df.groupby('name').agg({
    'Height': ['min', 'max', 'mean', 'std'],
    'Width': ['min', 'max', 'mean', 'std'],
    'Height_Width_Ratio': ['min', 'max', 'mean', 'std']
})

# print grouped
print(grouped)

# save to csv
grouped.to_csv('grouped_data.csv')
