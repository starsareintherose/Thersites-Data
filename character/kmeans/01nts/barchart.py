import os
import matplotlib.pyplot as plt

# Mapping: use the first three (or special) characters to get species name and color
prefix_to_species = {
    'nov': 'novaehollandiae',
    'mit': 'mitchellae',
    'dar': 'darlingtoni',
    'ric': 'richmondiana',
    'sp1': 'sp1',
    'sp2': 'sp2'
}

species_to_color = {
    'novaehollandiae': '#ff888a',
    'mitchellae': '#48b9ff',
    'darlingtoni': '#75ff66',
    'richmondiana': '#ede100',
    'sp1': '#0057b7',
    'sp2': '#b3b3b3'
}

# Fixed display order for the species
species_order = ['darlingtoni', 'mitchellae', 'novaehollandiae', 'richmondiana', 'sp1', 'sp2']

def parse_file(filename):
    """
    Parse the file and return a dictionary:
       { cluster_number: { species: count, ... }, ... }
    """
    clusters = {}
    current_cluster = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Check if the line is a cluster header (e.g., "Cluster 1:")
            if line.lower().startswith("cluster"):
                try:
                    parts = line.split()
                    cluster_num = parts[1].replace(":", "")
                    current_cluster = cluster_num
                    if current_cluster not in clusters:
                        clusters[current_cluster] = {}
                except Exception as e:
                    print(f"Error parsing cluster line: {line}, error: {e}")
                    current_cluster = None
                continue
            
            # Process entry lines
            if current_cluster is None:
                continue
            # Get the prefix (first three characters) from the entry
            prefix = line[:3]
            # Special handling for sp1 and sp2 (which may be longer)
            if line.startswith("sp1"):
                prefix = "sp1"
            elif line.startswith("sp2"):
                prefix = "sp2"
            
            species = prefix_to_species.get(prefix)
            if species is None:
                continue
            clusters[current_cluster][species] = clusters[current_cluster].get(species, 0) + 1
    return clusters

# Files to be processed
file_list = ["fl50_clusters.txt", "lm_clusters.txt", "slm1_clusters.txt", "slm2_clusters.txt"]

# Create 2x2 subplots
fig, axs = plt.subplots(1, 4, figsize=(12, 4))
axs = axs.flatten()

# Create legend patches for species
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=species_to_color[sp], label=sp) for sp in species_order]

# Process each file and generate subplots
for i, filename in enumerate(file_list):
    clusters = parse_file(filename)
    ax = axs[i]
    
    # Determine subplot title based on filename
    if "fl50" in filename or "fl_50" in filename:
        plot_title = "flagellum tip shape"
    elif "slm1" in filename:
        plot_title = "body whorl shape"
    elif "slm2" in filename:
        plot_title = "aperture shape"
    elif "lm" in filename:
        plot_title = "shell shape"
    else:
        plot_title = filename
    
    # Sort clusters (e.g., cluster 0 and cluster 1)
    sorted_clusters = sorted(clusters.items(), key=lambda x: int(x[0]))
    cluster_labels = [f"Cluster {c[0]}" for c in sorted_clusters]
    x = list(range(len(sorted_clusters)))
    
    # Draw stacked bar chart for each cluster with a thinner bar width
    width = 0.3
    for xi, (cluster_num, species_counts) in zip(x, sorted_clusters):
        bottom = 0
        for sp in species_order:
            count = species_counts.get(sp, 0)
            if count > 0:
                ax.bar(xi, count, width, bottom=bottom, color=species_to_color[sp])
                bottom += count
    
    ax.set_xticks(x)
    ax.set_xticklabels(cluster_labels)
    ax.set_title(plot_title)
    ax.set_ylabel("Count")
    
    # If this is the flagellum tip shape plot, add legend at upper left to avoid overlap
    if "fl50" in filename or "fl_50" in filename:
        ax.legend(handles=legend_elements, loc='upper left', fontsize=7, markerscale=0.8)
    
    # Annotate subplot with label A, B, C, D at the bottom left (in English)
    letter = chr(65 + i)  # A, B, C, D
    ax.text(0.05, -0.15, letter, transform=ax.transAxes, fontsize=12, fontweight='bold', va='top')

# Adjust layout to leave space for subplot labels at the bottom
fig.tight_layout(rect=[0, 0.05, 1, 1])

# Save the figure as SVG
plt.savefig("clusters.svg", format="svg")
plt.show()

