#!/usr/bin/env python3
import sys
import csv

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        lines = f.readlines()

    if len(lines) < 3:
        print("the input file is not in the expected format")
        sys.exit(1)

    # the first three lines are title, header, and taxa lines
    title_line = lines[0].strip()              # e.g., "Relative warp scores (S') matrix"
    header_info = lines[1].strip()             # e.g., "1 5L 12 0"
    taxa_line = lines[2].strip()               # taxa lines

    taxa = taxa_line.split()  # get the taxa names
    # extract the number of values per taxon
    try:
        numbers_per_taxon = int(header_info.split()[2])
    except Exception as e:
        print("the input file is not in the expected format")
        sys.exit(1)

    # collect all the data tokens
    data_tokens = []
    for line in lines[3:]:
        tokens = line.strip().split()
        data_tokens.extend(tokens)

    # check if the number of values in the input file is as expected
    expected_count = len(taxa) * numbers_per_taxon
    if len(data_tokens) != expected_count:
        print(f"Error: the number of values in the input file is not as expected, expected {expected_count}, got {len(data_tokens)}")
        sys.exit(1)

    # build the header for the CSV file
    header = ['id'] + [f"SV{i+1}" for i in range(numbers_per_taxon)]

    # read the data tokens and write to the output CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for i, taxon in enumerate(taxa):
            start = i * numbers_per_taxon
            end = start + numbers_per_taxon
            row_data = data_tokens[start:end]
            writer.writerow([taxon] + row_data)

    print(f"converted {input_file} to {output_file}")

if __name__ == '__main__':
    main()

