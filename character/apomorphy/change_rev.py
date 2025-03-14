import sys
import re

def parse_tnt(file_path):
    """ parse tnt file and return a mapping from index to word """
    mapping = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    index = 0
    for line in lines[3:]:  # skip the first 3 lines
        first_word = line.strip().split()[0]  # read the first word
        if first_word == ';':  # end to read
            break
        if str(index) not in mapping:  # avoid duplicate
            mapping[str(index)] = first_word
            index += 1
    
    return mapping

def replace_in_file(file_path, mapping):
    """ replace the number in file with the corresponding word """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # use regular expression to match the number
    pattern = re.compile(r'\b(' + '|'.join(re.escape(num) for num in sorted(mapping.keys(), key=int, reverse=True)) + r')\b')
    
    # replace the number with the corresponding word
    content = pattern.sub(lambda match: mapping[match.group(0)], content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    if len(sys.argv) < 3:
        print("Usage: change_rev.py <tnt_file> <target_tree_file>")
        sys.exit(1)
    
    tnt_file = sys.argv[1]
    target_file = sys.argv[2]
    
    mapping = parse_tnt(tnt_file)
    replace_in_file(target_file, mapping)
    print("Replacement complete.")

if __name__ == "__main__":
    main()
