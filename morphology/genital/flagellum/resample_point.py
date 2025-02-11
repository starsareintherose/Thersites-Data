import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import sys

def resample_csv(input_file, output_file, target_length=100):
    # read csv
    df = pd.read_csv(input_file)
    
    # give the file name
    print("Columns in CSV file:", df.columns)

    # confirm file name is right
    if 'Distance_(inches)' not in df.columns or 'inches' not in df.columns:
        print("Error: CSV file must contain 'Distance_(inches)' and 'inches' columns")
        sys.exit(1)

    # Convert inches to cm
    df['Distance_(cm)'] = df['Distance_(inches)'] * 2.54
    df['cm'] = df['inches'] * 2.54

    # use linear interpolation
    interp_func = interp1d(df['Distance_(cm)'], df['cm'], kind='linear')

    # create new x values in cm
    new_x = np.linspace(df['Distance_(cm)'].min(), df['Distance_(cm)'].max(), target_length)

    # calculate new y values in cm
    new_y = interp_func(new_x)

    # create new dataframe with cm values
    resampled_df = pd.DataFrame({'Distance_(cm)': new_x, 'cm': new_y})

    # save
    resampled_df.to_csv(output_file, index=False)
    print(f"Resampled data saved to {output_file}")

if __name__ == "__main__":
    # get arg
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.csv', '_converted.csv')
    
    # main function
    resample_csv(input_file, output_file)

