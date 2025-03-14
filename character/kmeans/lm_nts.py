#!/usr/bin/env python3
import sys
import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import defaultdict

#####################################
# read csv file, return id and features
#####################################
def read_csv(file_path):
    ids = []
    features = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.append(row['id'])
            # exclude 'id' column
            feat = [float(row[key]) for key in row if key != 'id']
            features.append(feat)
    return ids, np.array(features)

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
# main function: read csv file, find best k value, k-means clustering, save result
#####################################
def main():
    parser = argparse.ArgumentParser(description="CSV -> K-means clustering")
    parser.add_argument("input", help="input csv file")
    parser.add_argument("output_prefix", help="output file prefix")
    args = parser.parse_args()

    # Step 1: read csv file
    ids, features = read_csv(args.input)
    print("Loaded {} specimens.".format(len(ids)))
    print("Features shape:", features.shape)

    # Step 2: use silhouette score to find best k value
    k_range = range(2, 10)
    best_k, scores = find_best_k(features, k_range)

    # draw silhouette score vs. number of clusters
    plt.figure(figsize=(8, 6))
    plt.plot(list(k_range), scores, marker='o')
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Score vs. Number of Clusters")
    silhouette_file = f"{args.output_prefix}_silhouette_score.svg"
    plt.savefig(silhouette_file, format="svg")
    plt.show()
    print(f" Sillhouette Score map has been saved as {silhouette_file}")

    print("best K:", best_k)

    # Step 3: use best k value to do k-means clustering
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(features)

    # draw clustering result
    if features.shape[1] >= 2:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=features[:, 0], y=features[:, 1], hue=labels, palette="tab10", s=100)
        plt.xlabel("SV1")
        plt.ylabel("SV2")
        plt.title("Clustering Result")
        plt.legend(title="Cluster")
        clustering_file = f"{args.output_prefix}_clustering.svg"
        plt.savefig(clustering_file, format="svg")
        plt.show()
        print(f"clustering image has been saved as {clustering_file}")
    else:
        print(" SV dimension is less than 2, cannot draw clustering result")

    # Step 4: save clustering result
    cluster_dict = defaultdict(list)
    for specimen_id, label in zip(ids, labels):
        cluster_dict[label].append(specimen_id)
    output_txt = f"{args.output_prefix}_clusters.txt"
    with open(output_txt, "w") as f:
        for cluster, specimen_ids in cluster_dict.items():
            f.write(f"Cluster {cluster}:\n")
            for specimen_id in specimen_ids:
                f.write(f"{specimen_id}\n")
            f.write("\n")
    print(f"clustering results has been saved as {output_txt}")

if __name__ == "__main__":
    main()

