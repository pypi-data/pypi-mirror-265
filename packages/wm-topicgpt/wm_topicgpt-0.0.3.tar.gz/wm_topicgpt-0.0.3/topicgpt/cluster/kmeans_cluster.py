import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from topicgpt.cluster import MicroCluster
from topicgpt.cluster import update_microcluster_statistical_attributes

def generate_micro_clusters(
    data: pd.DataFrame,
    embedding_col_name: str, 
    text_col_name: str,
    n_clusters: int = 500,
    topk: int = 5,
    seed: int = 42,
):
    kmeans = KMeans(n_clusters=n_clusters, random_state=seed, n_init="auto")
    kmeans.fit(np.array(data[embedding_col_name].tolist(), dtype=np.float32))
    data['cluster'] = kmeans.labels_

    clusters = {}
    for label in sorted(set(kmeans.labels_)):
        subset = data[data['cluster'] == label].reset_index(drop=True)
        
        cluster = MicroCluster()
        cluster.data = subset
        cluster.centroid = kmeans.cluster_centers_[label]
        cluster.label = label
        update_microcluster_statistical_attributes(cluster, embedding_col_name, text_col_name, topk)
        clusters[label] = cluster
    
    return clusters