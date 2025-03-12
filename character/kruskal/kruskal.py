#!/usr/bin/env python
import argparse
import pandas as pd
import numpy as np
import sys
import tempfile
import os
import warnings
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.stats import kruskal
from ete3 import Tree, TreeStyle, faces, AttrFace, ImgFace, TextFace
from PIL import Image
import re

warnings.filterwarnings("ignore", category=SyntaxWarning)

VARIABLES = ["Width", "Height", "phallus", "epiphallus1", "epiphallus2", "flagellum"]

def compute_node_pvalues(node, df):
    if node.is_leaf():
        seq = node.name
        if seq in df.index:
            data = df.loc[seq].to_dict()
            node.add_feature("data", data)
            node.add_feature("data_list", [data])
        else:
            sys.stderr.write(f"Warning: {seq} not found in CSV\n")
            node.add_feature("data", None)
            node.add_feature("data_list", [])
        return node.data_list
    else:
        child_data_lists = []
        for child in node.get_children():
            child_data = compute_node_pvalues(child, df)
            child_data_lists.append(child_data)
        combined = []
        for group in child_data_lists:
            combined.extend(group)
        node.add_feature("data_list", combined)
        pvals = {}
        for var in VARIABLES:
            groups = []
            valid = True
            for group in child_data_lists:
                values = [d[var] for d in group if pd.notna(d[var])]
                if len(values) == 0:
                    valid = False
                    break
                groups.append(values)
            if not valid or len(groups) < 2:
                pvals[var] = np.nan
            else:
                try:
                    stat, pval = kruskal(*groups)
                    pvals[var] = pval
                except Exception as e:
                    pvals[var] = np.nan
        node.add_feature("pvalues", pvals)
        if not hasattr(compute_node_pvalues, "counter"):
            compute_node_pvalues.counter = 1
        node.add_feature("node_id", f"Node{compute_node_pvalues.counter}")
        compute_node_pvalues.counter += 1
        return combined

def draw_heatmap_imgface(data, width=60, height=45, thresh_levels=(0.05, 0.01, 0.001)):
    """
    Draw a 2×3 heatmap, resize the heatmap displayed on the node.
    """
    if np.all(np.isnan(data)):
        return None
    fig, ax = plt.subplots(figsize=(1.5, 1))
    masked_data = np.ma.masked_invalid(data)
    cmap = plt.cm.viridis.copy()
    cmap.set_bad(color='none')
    ax.imshow(masked_data, interpolation='nearest', cmap=cmap, vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    # add black broader
    rect = plt.Rectangle((-0.5, -0.5), 3, 2, fill=False, edgecolor='black', linewidth=3, clip_on=False)
    ax.add_patch(rect)
    ax.axis('off')
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.savefig(tmp.name, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)
    return tmp.name

def create_heatmap_bar_horizontal(width=8, height=0.5):
    """
    Generate a horizontal global heatmap bar image,
    the data matrix shape is (1,100), and the color gradient is from 0 to 1.
    The output is SVG format.
    """
    fig, ax = plt.subplots(figsize=(width, height))
    data = np.linspace(0, 1, 100).reshape((1, 100))
    ax.imshow(data, aspect="auto", cmap=plt.cm.viridis)
    ax.set_xticks([])
    ax.set_yticks([])
    tmp = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
    plt.savefig('bar.svg', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)

def layout_with_labels(node):
    """
    Leaf nodes display italic names (larger font), internal nodes:
    - If there are p-values, add a larger node heatmap in branch-top;
    - Also add node labels (node_id) in branch-right.
    """
    if node.is_leaf():
        name_face = AttrFace("name", fsize=14, fstyle="italic")
        faces.add_face_to_node(name_face, node, 0, position="branch-right")
    else:
        if hasattr(node, "pvalues"):
            pvals = node.pvalues
            data = [pvals.get(var, np.nan) for var in VARIABLES]
            data = np.array(data).reshape((2, 3))
            img_file = draw_heatmap_imgface(data, width=60, height=45)
            if img_file is not None:
                img_face = ImgFace(img_file, width=60, height=45)
                img_face.margin_top = -45
                faces.add_face_to_node(img_face, node, 0, position="branch-top")
            label_face = AttrFace("node_id", fsize=20, fgcolor="red")
            faces.add_face_to_node(label_face, node, 0, position="branch-right")

def layout_without_labels(node):
    """
    Leaf nodes display italic names; if internal nodes have p-values, only a larger heatmap is added to the branch-top without displaying labels.
    """
    if node.is_leaf():
        name_face = AttrFace("name", fsize=50, fstyle="italic")
        faces.add_face_to_node(name_face, node, 0, position="branch-right")
    else:
        if hasattr(node, "pvalues"):
            pvals = node.pvalues
            data = [pvals.get(var, np.nan) for var in VARIABLES]
            data = np.array(data).reshape((2, 3))
            img_file = draw_heatmap_imgface(data, width=140, height=105)
            if img_file is not None:
                img_face = ImgFace(img_file, width=140, height=105)
                #img_face.margin_top = -100
                img_face.margin_bottom = 10
                img_face.margin_right = 20
                faces.add_face_to_node(img_face, node, 0, position="branch-top")

def main():
    parser = argparse.ArgumentParser(
        description="plot KW test heatmap on the tree"
    )
    parser.add_argument("-t", "--tree", required=True, help="Newick file path")
    parser.add_argument("-c", "--csv", required=True, help="CSV including 'seq' column corresponding to tree tip")
    parser.add_argument("--svg1", default="tree_with_labels.svg", help="svg with node labels")
    parser.add_argument("--svg2", default="tree_without_labels.svg", help="svg without node labels")
    parser.add_argument("--table", default="pvalues_table.csv", help="p-values table")
    args = parser.parse_args()

    # read data
    df = pd.read_csv(args.csv, na_values=["?"])
    if "seq" not in df.columns:
        sys.stderr.write("CSV 文件中必须包含 'seq' 列\n")
        sys.exit(1)
    df.set_index("seq", inplace=True)

    # read Newick tree
    try:
        tree = Tree(args.tree, format=1)
    except Exception as e:
        sys.stderr.write(f"读取树失败: {e}\n")
        sys.exit(1)

    # compute p-values for each internal node
    compute_node_pvalues(tree, df)

    # adjust tree style
    for n in tree.traverse():
        n.img_style["hz_line_width"] = 10
        n.img_style["vt_line_width"] = 10
        n.img_style["size"] = 0

    ts_scale = 170

    # output p-values table
    records = []
    for node in tree.traverse():
        if not node.is_leaf() and hasattr(node, "pvalues"):
            record = {"node_id": node.node_id}
            for var in VARIABLES:
                record[var] = node.pvalues.get(var, np.nan)
            records.append(record)
    pd.DataFrame(records).to_csv(args.table, index=False)
    sys.stdout.write(f"p-value has been saved as {args.table}\n")

    # create tree style
    ts_with = TreeStyle()
    ts_with.mode = "r"
    ts_with.force_topology = True
    ts_with.branch_vertical_margin = 10
    ts_with.show_leaf_name = False
    ts_with.layout_fn = layout_with_labels
    ts_with.scale = ts_scale

    ts_without = TreeStyle()
    ts_without.mode = "r"
    ts_without.force_topology = True
    ts_without.branch_vertical_margin = 10
    ts_without.show_leaf_name = False
    ts_without.layout_fn = layout_without_labels
    ts_without.scale = ts_scale

    create_heatmap_bar_horizontal(width=8, height=0.5)

    tree.render(args.svg1, tree_style=ts_with)
    sys.stdout.write(f"tree with node labels has been saved as {args.svg1}\n")

    tree.render(args.svg2, tree_style=ts_without)
    sys.stdout.write(f"tree without node labels has been saved as {args.svg2}\n")

if __name__ == "__main__":
    main()

