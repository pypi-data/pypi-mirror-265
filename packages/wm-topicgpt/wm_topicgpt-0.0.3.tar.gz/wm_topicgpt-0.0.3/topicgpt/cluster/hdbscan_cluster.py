import pandas as pd
from umap import UMAP
from typing import List, Any
from dataclasses import dataclass, field
from sklearn.cluster import HDBSCAN
from topicgpt.cluster import update_microcluster_statistical_attributes, MicroCluster, generate_microcluster_topic_prompts
from topicgpt.walmart_llm import chat_complete


def generate_cluster_tree(dataframe, embedding_col_name, dim, n_neighbors, min_cluster_size, tier=1):

    def dfs_generate_clusters(root, subframe, n_neighbors, tier):
        print("\t"*(tier-1),"Tier:", tier, "Size:", len(subframe), "Neighbors:", n_neighbors)

        reducer = UMAP(n_neighbors=n_neighbors, n_components=dim, metric='cosine')
        reduced_embeddings = reducer.fit_transform(subframe[embedding_col_name].tolist())

        cluster = HDBSCAN(min_cluster_size=min_cluster_size, n_jobs=-1)
        cluster.fit(reduced_embeddings)
        subframe['cluster'] = cluster.labels_

        for label in sorted(set(cluster.labels_)):
            cluster_data = subframe[subframe['cluster'] == label].reset_index(drop=True)
            print("\t"*(tier-1), "Cluster:", label, "Size:", len(cluster_data))

            if len(cluster_data) <= min_cluster_size:
                root.children.append(MicroCluster(data=cluster_data, label=label))
            else:
                next_neighbors = int(n_neighbors // 2)
                if next_neighbors < 2:
                    root.children.append(MicroCluster(data=cluster_data, label=label))
                else:
                    sub_root = dfs_generate_clusters(MicroCluster(), cluster_data, next_neighbors, tier+1)
                    root.children.append(sub_root.children[0] if len(sub_root.children) == 1 else sub_root)
        return root.children[0] if len(root.children) == 1 else root
    
    return dfs_generate_clusters(MicroCluster(), dataframe, n_neighbors, tier=tier)


def generate_topic_for_cluster_tree(root, text_col_name, embedding_col_name, topk=3):
    
    def postorder_traversal(root):
        for child in root.children:
            postorder_traversal(child)

        # if len(root.children) == 0 and root.data is not None:
        #     update_microcluster_statistical_attributes(root, embedding_col_name, text_col_name, topk)
        #     prompt = generate_microcluster_topic_prompts(root, text_col_name, topk)
        #     response = chat_complete([prompt], model_version="gpt-4", temperature=0.)
        #     root.topic = eval(response[0][0].text)['topic']
        #     root.description = eval(response[0][0].text)['description']
            
        if len(root.children) != 0 and root.data is None:
            root.data = pd.concat([child.data for child in root.children], axis=0).reset_index(drop=True)

        update_microcluster_statistical_attributes(root, embedding_col_name, text_col_name, topk)
        prompt = generate_microcluster_topic_prompts(root, text_col_name, topk)
        response = chat_complete([prompt], model_version="gpt-4", temperature=0.)
        root.topic = eval(response[0][0].text)['topic']
        root.description = eval(response[0][0].text)['description']

        if len(root.children) == 0:
            root.size = len(root.data)
        else:
            root.size = sum([child.size for child in root.children])
            for child in root.children:
                child.percent = round(child.size / root.size, 3)
    
    postorder_traversal(root)
    root.percent = 1.
    return root
