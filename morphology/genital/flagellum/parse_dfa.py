import re
import csv
import sys
from collections import defaultdict
import os

if len(sys.argv) != 2:
    print("Usage: python parse_dfa_matrix_en.py inputfile.txt")
    sys.exit(1)

input_file = sys.argv[1]
prefix = os.path.splitext(os.path.basename(input_file))[0]

with open(input_file, "r") as f:
    text = f.read()

blocks = re.split(r"Discriminant Function Analysis", text)[1:]

species = set()
accuracy_dict = defaultdict(dict)
significance_dict = defaultdict(dict)
mahalanobis_dict = defaultdict(dict)
label_dict = defaultdict(dict)

def interpret_combined(mahalanobis_dist_str, t_p_str):
    try:
        mahalanobis_dist = float(mahalanobis_dist_str)
        pro_p = float(pro_p_str.replace("<", ""))
        t_p = float(t_p_str.replace("<", ""))
    except:
        return "Data missing"

    if t_p >= 0.05:
        return "Not significantly different"

    if mahalanobis_dist > 20:
        return f"Significant and large shape difference (p = {t_p}, Procrustes = {mahalanobis_dist})"
    elif mahalanobis_dist > 10:
        return f"Significant and moderate shape difference (p = {t_p}, Procrustes = {mahalanobis_dist})"
    elif mahalanobis_dist > 5:
        return f"Significant but small shape difference (p = {t_p}, Procrustes = {mahalanobis_dist})"
    else:
        return f"Significant but very small shape difference (p = {t_p}, Procrustes = {mahalanobis_dist})"

def label_summary(mahalanobis_dist_str, t_p_str):
    try:
        mahalanobis_dist = float(mahalanobis_dist_str)
        t_p = float(t_p_str.replace("<", ""))
    except:
        return ""

    if t_p >= 0.05:
        return "NS"

    if mahalanobis_dist > 20:
        return "L"
    elif mahalanobis_dist > 10:
        return "M"
    elif mahalanobis_dist > 5:
        return "S"
    else:
        return "SN"

for block in blocks:
    comp = re.search(r"Comparison:\s+(\w+)\s+--\s+(\w+)", block)
    if not comp:
        continue
    sp1, sp2 = comp.groups()
    species.update([sp1, sp2])

    # Cross-validation classification
    cv_match = re.search(
        r"From cross-validation:\s+True\s+Allocated to\s+Group\s+Group 1\s+Group 2\s+Total\s+Group 1\s+(\d+)\s+(\d+)\s+\d+\s+Group 2\s+(\d+)\s+(\d+)",
        block
    )
    if cv_match:
        g1_g1, g1_g2, g2_g1, g2_g2 = map(int, cv_match.groups())
        correct = g1_g1 + g2_g2
        total = g1_g1 + g1_g2 + g2_g1 + g2_g2
        acc = round(correct / total * 100, 2)
        accuracy_dict[sp1][sp2] = acc
        accuracy_dict[sp2][sp1] = acc

    # Extract values
    mahalanobis_match = re.search(r"Mahalanobis distance:\s+([\d.]+)", block)
    mahalanobis_dist = mahalanobis_match.group(1) if mahalanobis_match else ""

    #perm_procrustes_match = re.findall(r"P-values for permutation tests.*?Procrustes distance:\s*([<\d.]+)", block, re.DOTALL)
    perm_tsquare_match = re.findall(r"P-values for permutation tests.*?T-square:\s*([<\d.]+)", block, re.DOTALL)

    #if perm_procrustes_match and perm_tsquare_match:
    if perm_tsquare_match:
        #pro_p = perm_procrustes_match[0]
        t_p = perm_tsquare_match[0]

        mahalanobis_dict[sp1][sp2] = mahalanobis_dist
        mahalanobis_dict[sp2][sp1] = mahalanobis_dist

        interpretation = interpret_combined(mahalanobis_dist, t_p)
        significance_dict[sp1][sp2] = interpretation
        significance_dict[sp2][sp1] = interpretation

        label = label_summary(mahalanobis_dist, t_p)
        label_dict[sp1][sp2] = label
        label_dict[sp2][sp1] = label

species = sorted(species)

# Output 1: accuracy
with open(f"{prefix}_classification_accuracy_matrix.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([""] + species)
    for sp1 in species:
        row = [sp1]
        for sp2 in species:
            row.append("—" if sp1 == sp2 else accuracy_dict.get(sp1, {}).get(sp2, ""))
        writer.writerow(row)

# Output 2: English significance matrix
with open(f"{prefix}_comparison_significance_matrix.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([""] + species)
    for sp1 in species:
        row = [sp1]
        for sp2 in species:
            row.append("—" if sp1 == sp2 else significance_dict.get(sp1, {}).get(sp2, ""))
        writer.writerow(row)

# Output 3: M distance matrix
with open(f"{prefix}_distance_matrix.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([""] + species)
    for sp1 in species:
        row = [sp1]
        for sp2 in species:
            row.append("—" if sp1 == sp2 else mahalanobis_dict.get(sp1, {}).get(sp2, ""))
        writer.writerow(row)

# Output 4: summary label matrix
with open(f"{prefix}_summary_label_matrix.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([""] + species)
    for sp1 in species:
        row = [sp1]
        for sp2 in species:
            row.append("—" if sp1 == sp2 else label_dict.get(sp1, {}).get(sp2, ""))
        writer.writerow(row)

