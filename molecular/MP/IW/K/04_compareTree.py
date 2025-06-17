from ete3 import Tree
from collections import defaultdict

def trees_equal(newick1, newick2):
    t1 = Tree(newick1, format=1)
    t2 = Tree(newick2, format=1)
    rf, *_ = t1.robinson_foulds(t2)
    return rf == 0

def compress_line_numbers(numbers):
    numbers = sorted(numbers)
    result = []
    start = numbers[0]
    end = numbers[0]

    for n in numbers[1:]:
        if n == end + 1:
            end = n
        else:
            if start == end:
                result.append(f"{start}")
            else:
                result.append(f"{start}–{end}")
            start = end = n

    if start == end:
        result.append(f"{start}")
    else:
        result.append(f"{start}–{end}")

    return ', '.join(result)

with open("00allK.nex") as f:
    lines = [line.strip() for line in f if line.strip()]

types = []  # one line one tree
type_index_map = defaultdict(list)

for idx, tree_str in enumerate(lines):
    line_no = idx + 1
    matched = False
    for i, (rep_tree, line_numbers) in enumerate(types):
        if trees_equal(tree_str, rep_tree):
            types[i][1].append(line_no)
            matched = True
            break
    if not matched:
        types.append((tree_str, [line_no]))

# output the results
for i, (_, line_numbers) in enumerate(types, 1):
    lines_str = compress_line_numbers(line_numbers)
    print(f"Type {i}: K {lines_str}")
