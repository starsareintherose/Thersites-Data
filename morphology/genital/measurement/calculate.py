import numpy as np
import pandas as pd

# read csv
df = pd.read_csv('measure_genital.csv')

# replace empty string with NaN
df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

# drop rows with NaN in columns 'phallus', 'epiphallus1', 'epiphallus2', 'flagellum'
cols = ['phallus', 'epiphallus1', 'epiphallus2', 'flagellum']
df.dropna(subset=cols, inplace=True)

# delete rows with 0 in columns 'phallus', 'epiphallus1', 'epiphallus2', 'flagellum'
for col in cols:
    df = df[df[col] != 0]

# calculate min, max, mean, std of each group
grouped = df.groupby('species').agg({
    'phallus': ['min', 'max', 'mean', 'std'],
    'epiphallus1': ['min', 'max', 'mean', 'std'],
    'epiphallus2': ['min', 'max', 'mean', 'std'],
    'flagellum': ['min', 'max', 'mean', 'std']
})

# print grouped
print(grouped)

# save to csv
grouped.to_csv('grouped_data.csv')
