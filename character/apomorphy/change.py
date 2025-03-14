import sys

def parse_tnt(file_path):
    """ parse tnt file and return a mapping """
    mapping = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    index = 0
    for line in lines[3:]:  # skip the first 3 lines
        first_word = line.strip().split()[0]  # read the first word
        if first_word == ';':  # end to read
            break
        if first_word not in mapping:  # avoid duplicate
            mapping[first_word] = str(index)
            index += 1
    
    return mapping

def replace_in_file(file_path, mapping):
    """ replace the original words with the numbers in the file """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for original, number in mapping.items():
        content = content.replace(original, number)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    if len(sys.argv) < 3:
        print("Usage: change.py <tnt_file> <target_tree_file>")
        sys.exit(1)
    
    tnt_file = sys.argv[1]
    target_file = sys.argv[2]
    
    mapping = parse_tnt(tnt_file)
    replace_in_file(target_file, mapping)
    print("Replacement complete.")

if __name__ == "__main__":
    main()
