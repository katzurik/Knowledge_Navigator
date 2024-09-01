
from tqdm import tqdm

import json
import os
import numpy as np
import pickle

# cluster
from sklearn.cluster import AgglomerativeClustering,KMeans,OPTICS
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score

import umap



def extract_data_for_clustering(data,top_k=1000):

    data = data[0:np.min([top_k,len(data)])]
    # Extract vectors, titles, and abstracts
    vectors = [item[3] for item in data]
    titles_abstracts = [(item[0], item[1],item[2]) for item in data]

    # Convert list of vectors to a numpy matrix
    vector_matrix = np.array(vectors)

    return vector_matrix, titles_abstracts

def cluster_papers(embeddings, titles_abstracts, n_clusters, cluster_method, is_umap, do_bic,do_silhouette):


  if is_umap:
    embeddings = umap.UMAP(n_neighbors= np.min([int((len(embeddings) - 1) ** 0.5) ,50])  ,
                           n_components=20,
                           min_dist=0,
                           metric='cosine',
                           random_state=42
                         ).fit_transform(embeddings)

  if cluster_method == 'Kmeans':
    clustering_model = KMeans(n_clusters=n_clusters)

  elif cluster_method == 'HCL':  # Renamed from 'HCl' for consistency
    clustering_model = AgglomerativeClustering(
                                            # metric='cosine',
                                            distance_threshold=2,
                                            n_clusters=None)
  elif cluster_method == 'OPTICS':
    clustering_model = OPTICS(metric='cosine', min_samples=2)

  elif cluster_method == 'GMM':
    covariance_type = 'full'
    threshold = 0.1
    min_clusters = 5
    #reg_covar = 1e-6
    # Select the optimal number of clusters based on BIC
    bic_scores = []
    silhouette_scores = []
    optimal_n_clusters = n_clusters
    cluster_range = range(min_clusters, n_clusters + 1)
    #cluster_range = range(1, n_clusters*2 + 1)
    for n in tqdm(cluster_range):
        gmm = GaussianMixture(n_components=n,
                              random_state=42,
                              covariance_type=covariance_type)
        gmm.fit(embeddings)
        if do_bic:
            bic_scores.append(gmm.bic(embeddings))
        if do_silhouette and n > 1:  # Silhouette score requires at least 2 clusters to be meaningful
            cluster_labels = gmm.predict(embeddings)
            silhouette_scores.append(silhouette_score(embeddings, cluster_labels))

    # # Select the optimal number of clusters based on BIC or silhouette
    if do_bic:
        optimal_n_clusters = cluster_range[np.argmin(bic_scores)]
        print(f"Optimal number of clusters based on BIC (GMM): {optimal_n_clusters}")
    if do_silhouette:
        optimal_n_clusters = cluster_range[np.argmax(silhouette_scores)]
        print(f"Optimal number of clusters based on silhouette score (GMM): {optimal_n_clusters}")


    # Create the final model with the selected number of clusters
    clustering_model = GaussianMixture(n_components=optimal_n_clusters,
                                       covariance_type=covariance_type,
                                       random_state=42)

    print(f"Optimal number of clusters (GMM): {optimal_n_clusters}")

  else:  # Handle invalid clustering methods
    raise ValueError("Invalid clustering method specified")

  clustering_model.fit(embeddings)
  if cluster_method =='GMM':
    probabilities = clustering_model.predict_proba(embeddings)
    cluster_assignment =  [np.where(p > threshold)[0] for p in probabilities]

  else:
    cluster_assignment = clustering_model.labels_


  clusters = dict()
  for paper_id,cluster_names in enumerate(cluster_assignment):
    for cluster in cluster_names:
        if cluster not in clusters:
          clusters[cluster] = []

        clusters[cluster].append(titles_abstracts[paper_id])

  clusters = dict(sorted(clusters.items(), key=lambda item: len(item[1]),reverse=True))

  # Preparing output
  cluster_output = {}
  for cluster_id, papers in clusters.items():
    cluster_output[str(cluster_id)] = [{'title': paper[0], 'abstract': paper[1],'link':paper[2]} for paper in papers]



  return cluster_output,embeddings,cluster_assignment


def run_cluster_subtopics(emeddings,query,output_dir):
    """
    Runs the clustering of subtopics.
    """
    # Load the data
    if not os.path.exists(f"{output_dir}/{query}/{query}_cluster.json"):

        vector_matrix, titles_abstracts = extract_data_for_clustering(emeddings,top_k=1000)

        n_clusters = len(vector_matrix) // 10 #Max number of clusters is 10% of the number of papers
        cluster_method = 'GMM'
        is_umap = True
        do_bic = False
        do_silhouette = True
        # Cluster the papers
        cluster_output,embeddings_after_cluster,cluster_assignment = cluster_papers(vector_matrix,
                                                                                    titles_abstracts,
                                                                                    n_clusters,
                                                                                    cluster_method,
                                                                                    is_umap,
                                                                                    do_bic,
                                                                                    do_silhouette)

        with open(f"{output_dir}/{query}/{query}_cluster.json","w") as f:
            json.dump(cluster_output, f)

    else:
        with open(f"{output_dir}/{query}/{query}_cluster.json") as f:
            cluster_output = json.load(f)

    return cluster_output


if __name__ == "__main__":


    query = 'Neuroblastoma'
    output_dir = 'Data'

    with open(f"{output_dir}/{query}/{query}_embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)

    run_cluster_subtopics(embeddings,query,output_dir)
