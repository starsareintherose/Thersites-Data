import os
import pandas as pd
import sys

def convert_csv_to_custom_format(input_file):
    # read CSV file
    df = pd.read_csv(input_file)

    # trim the extension name
    file_name = os.path.basename(input_file)
    base_name = os.path.splitext(file_name)[0]

    # count the line number
    num_rows = len(df)

    # store in array
    result = []
    
    # add LM
    result.append(f"LM={num_rows}")  
    
    # transfer csv rows to points
    for index, row in df.iterrows():
        x_value = row.iloc[0]
        y_value = row.iloc[1]
        result.append(f"{x_value:.5f} {y_value:.5f}")

    # add fake images and id
    result.append(f"IMAGE={base_name}.tif")
    result.append(f"ID={base_name}")

    return result

def process_all_csv_in_folder(folder_path, output_file):
    # open file append data
    with open(output_file, 'w') as f:
        # get all csv in folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):  # only process csv
                input_file = os.path.join(folder_path, file_name)
                print(f"Processing {input_file}...")  # output processing file, make debug easier
                converted_data = convert_csv_to_custom_format(input_file)
                
                # write
                for line in converted_data:
                    f.write(line + "\n")
                f.write("\n")  # give a blank line

    print(f"All CSV files have been processed and saved to {output_file}")

if __name__ == "__main__":
    # arg
    if len(sys.argv) < 2:
        print("Usage: python csv_to_tps.py <input_folder> [output_file]")
        sys.exit(1)

    # input folder as arg1
    folder_path = sys.argv[1]

    # output file as  arg2, default is output.tps
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.tps'

    # main function
    process_all_csv_in_folder(folder_path, output_file)

