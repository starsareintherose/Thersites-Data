import re
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import defaultdict
from scipy.interpolate import interp1d
from numpy.linalg import svd

#####################################
# read TPS file
#####################################
def read_tps(file_path):
    """
    read TPS file and return taxa_names, landmarks, and lm_counts
        LM=7
        4017.00000 4657.00000
        3278.00000 4361.00000
        2771.00000 3942.00000
        3522.00000 2442.00000
        4917.00000 3055.00000
        4979.00000 4084.00000
        4592.00000 4405.00000
        IMAGE=novaehollandiae_C.584421_Barrington-Tops_01.tif
        ID=novaehollandiae_C.584421_Barrington-Tops_01

    """
    taxa_names = []
    landmarks = []
    lm_counts = []
    with open(file_path, 'r') as f:
        lines = f.read().strip().splitlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("LM="):
            # read num_landmarks
            num_landmarks = int(line.split("=")[1])
            lm_counts.append(num_landmarks)
            i += 1
            coords = []
            # read landmarks
            for j in range(num_landmarks):
                coord_line = lines[i].strip()
                coords.append(list(map(float, coord_line.split())))
                i += 1
            # read IMAGE line
            if i < len(lines) and lines[i].startswith("IMAGE="):
                _ = lines[i]  # you can save the image name if needed
                i += 1
            # read ID line
            id_val = None
            if i < len(lines) and lines[i].startswith("ID="):
                id_val = lines[i].split("=", 1)[1].strip()
                i += 1
            # skip empty lines
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            taxa_names.append(id_val)
            landmarks.append(np.array(coords))  # to numpy array
        else:
            i += 1
    return taxa_names, landmarks, lm_counts

#####################################
# align landmarks
#####################################
def align_landmarks(landmarks, target_points):
    """
    landmarks: list, each item is a (n,2) numpy array
    if the number of landmarks in a specimen is not equal to target_points,
    perform linear interpolation to make each specimen have target_points points.
    return a numpy array with shape (n_specimen, target_points, 2).
    """
    aligned_landmarks = []
    for lm in landmarks:
        current_points = lm.shape[0]
        if current_points == target_points:
            aligned_landmarks.append(lm)
        else:
            # perform linear interpolation
            x_old = np.linspace(0, 1, current_points)
            f = interp1d(x_old, lm, axis=0, kind='linear')
            x_new = np.linspace(0, 1, target_points)
            aligned_landmarks.append(f(x_new))
    return np.array(aligned_landmarks)

#####################################
# Procrustes fit
#####################################
def procrustes_align(source, target):

    U, _, Vt = svd(np.dot(target.T, source))
    R = np.dot(U, Vt)
    aligned = np.dot(source, R.T)
    return aligned

#####################################
# Generalized Procrustes Analysis (GPA)
#####################################
def generalized_procrustes(shapes, max_iter=100, tol=1e-5):
    """
    shapes: numpy array，shape = (n_specimen, n_points, 2)
    align all specimens using GPA, first centerize and normalize each specimen,
    return aligned shapes and the mean shape.
    """
    n, m, d = shapes.shape
    shapes_aligned = np.empty_like(shapes)
    # centerize and normalize each specimen
    for i in range(n):
        shape = shapes[i]
        centered = shape - np.mean(shape, axis=0)
        norm = np.linalg.norm(centered)
        shapes_aligned[i] = centered / norm
    
    mean_shape = np.mean(shapes_aligned, axis=0)
    
    for iteration in range(max_iter):
        new_shapes = []
        for i in range(n):
            aligned = procrustes_align(shapes_aligned[i], mean_shape)
            new_shapes.append(aligned)
        new_shapes = np.array(new_shapes)
        new_mean = np.mean(new_shapes, axis=0)
        diff = np.linalg.norm(new_mean - mean_shape)
        mean_shape = new_mean
        shapes_aligned = new_shapes
        if diff < tol:
            break
    return shapes_aligned, mean_shape

#####################################
# find best k value by silhouette score
#####################################
def find_best_k(X, k_range):
    best_k = k_range[0]
    best_score = -1
    scores = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        score = silhouette_score(X, labels)
        scores.append(score)
        if score > best_score:
            best_score = score
            best_k = k
    return best_k, scores

#####################################
# main function: read TPS -> align landmarks -> GPA -> PCA -> K-means
#####################################
def main():
    parser = argparse.ArgumentParser(description="TPS -> GPA -> PCA -> K-means clustering")
    parser.add_argument("input", help="input TPS file")
    parser.add_argument("output_prefix", help="output file prefix")
    args = parser.parse_args()

    # Step 1: read TPS file
    taxa_names, landmarks, lm_counts = read_tps(args.input)
    print("Loaded {} specimens.".format(len(taxa_names)))
    print("each specimen LM counts: ", lm_counts)
    
    # Step 2: confirm target_points
    target_points = min(lm_counts)
    print("target_points:", target_points)
    
    # Step 3: align landmarks
    landmarks_aligned = align_landmarks(landmarks, target_points)
    print("Landmarks has been aligned to have {} points.".format(target_points))
    
    # Step 4: Generalized Procrustes Analysis (GPA)
    landmarks_gpa, mean_shape = generalized_procrustes(landmarks_aligned)
    print("Procrustes alignment finished")
    
    # Step 5: reshape for PCA
    num_samples = landmarks_gpa.shape[0]
    X = landmarks_gpa.reshape(num_samples, -1)
    
    # Step 6: visualize PCA projection
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1])
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA Projection of GPA Aligned TPS Data")
    pca_file = f"{args.output_prefix}_pca_projection.svg"
    plt.savefig(pca_file, format="svg")
    plt.show()
    print(f"PCA images has been saved as {pca_file}")
    
    # Step 7: use Silhouette Score to find best K
    k_range = range(2, 10)
    best_k, scores = find_best_k(X_pca, k_range)
    
    # draw Silhouette Score vs. Number of Clusters
    plt.figure(figsize=(8, 6))
    plt.plot(list(k_range), scores, marker='o')
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Score vs. Number of Clusters")
    silhouette_file = f"{args.output_prefix}_silhouette_score.svg"
    plt.savefig(silhouette_file, format="svg")
    plt.show()
    print(f"Sillhouette Score map has been saved as {silhouette_file}")
    
    print("best K:", best_k)
    
    # Step 8: use K-means to cluster with best k value
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_pca)
    
    # draw clustering result
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=labels, palette="tab10", s=100)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA Projection with K-means Clustering")
    plt.legend(title="Cluster")
    clustering_file = f"{args.output_prefix}_clustering.svg"
    plt.savefig(clustering_file, format="svg")
    plt.show()
    print(f"clustering image has been saved as {clustering_file}")
    
    # Step 9: save clustering results
    cluster_dict = defaultdict(list)
    for taxon, label in zip(taxa_names, labels):
        cluster_dict[label].append(taxon)
    
    output_txt = f"{args.output_prefix}_clusters.txt"
    with open(output_txt, "w") as f:
        for cluster, taxa in cluster_dict.items():
            f.write(f"Cluster {cluster}:\n")
            for taxon in taxa:
                f.write(f"{taxon}\n")
            f.write("\n")
    print(f"clustering results has been saved as {output_txt}")

if __name__ == "__main__":
    main()

