import pandas as pd
from topicgpt.preprocessing import drop_short_words_data, drop_long_words_data, batch_name_filter
from topicgpt.embedding import embed_documents
from topicgpt.cluster import generate_cluster_tree, generate_topic_for_cluster_tree
from topicgpt.visualization import plot_cluster_tree


def build_taxonomy_by_hdbscan(
    dataframe: pd.DataFrame,
    text_col_name: str,
    min_words: int = None,
    max_words: int = None,
    name_filter: bool = False,
    embed_col_name: str = 'embeddings',
    embed_model: str = "bge-small",
    device: str = "mps",
    reduced_dim: int = 10,
    n_neighbors: int = 10,
    min_cluster_size: int = 100,
    topk: int = 3,
):
    # preprocessing
    if min_words:
        dataframe = drop_short_words_data(dataframe, text_col_name, min_words=min_words)
    if max_words:
        dataframe = drop_long_words_data(dataframe, text_col_name, max_words=max_words)
    if name_filter:
        dataframe[text_col_name] = batch_name_filter(dataframe[text_col_name].tolist())
    
    # embedding
    dataframe[embed_col_name] = embed_documents(dataframe[text_col_name].tolist(), model_name=embed_model, device=device)
    
    # clustering
    root = generate_cluster_tree(dataframe, embed_col_name, dim=reduced_dim, n_neighbors=n_neighbors, min_cluster_size=min_cluster_size)
    generate_topic_for_cluster_tree(root, text_col_name, embed_col_name, topk=topk)

    # plot
    plot_cluster_tree(root)
