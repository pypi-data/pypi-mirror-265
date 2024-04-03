import numpy as np
import pandas as pd
from typing import List, Any
from dataclasses import dataclass, field
from sklearn.metrics.pairwise import pairwise_distances
from topicgpt.walmart_llm import achat_complete, chat_complete

@dataclass
class MicroCluster:
    data: pd.DataFrame = None
    label: int = None
    children: List[Any] = field(default_factory=list)

    centroid: List[float] = None
    close_sets: List[str] = None
    within_cluster_dist: int = None
    
    topic: str = None
    description: str = None
    keywords: List[str] = None
    
    size: int = None
    percent: float = None


def update_microcluster_statistical_attributes(
    cluster: MicroCluster,
    embedding_col_name: str, 
    text_col_name: str,
    topk: int
):
    if len(cluster.data) > 0:
        if cluster.centroid is None:
            cluster.centroid = np.mean(np.array(cluster.data[embedding_col_name].tolist()), axis=0)
        dists = pairwise_distances(np.array([cluster.centroid]), np.array(cluster.data[embedding_col_name].tolist()))[0]
        cluster.within_cluster_dist = np.mean(dists)
        sorted_indices = np.argsort(dists)[:topk]
        cluster.close_sets = cluster.data.loc[sorted_indices, text_col_name].tolist()
        cluster.size = len(cluster.data)


def generate_microcluster_topic_prompts(
    cluster: MicroCluster,
    text_col_name: str,
    topk: int,
):
    template1 = """You are a good editor. Given some requirements and prompts, you need to summarize the main topic of those prompts and give a simple description of this topic according to those requirements.
    
    Here are some requirements you MUST follow:
    1. The topic should reflect the main intent of those prompts.
    2. The topic should be less than 10 words.
    3. The description should be less than 20 words.

    Here are the prompts you need to consider all:
    {user_prompt}"""
    
    template2 = """
    The output should be in the json format:
    {"topic": <summarize the main topic of those prompts>, "description": <output a discription for this topic, less than 20 words>}
    """
    sampled_data = cluster.data[text_col_name].sample(n=min(topk, len(cluster.data)))
    prompt_str = ""
    for i, text in enumerate(sampled_data, 1):
        prompt_str += (f"{i}. {text}\n")
    prompt = template1.format(user_prompt=prompt_str) + template2
    return prompt


def update_microcluster_topic_and_description(
    clusters: List[MicroCluster],
    text_col_name: str,
    topk: int,
    model: str = "gpt-4",
):
    prompts = [update_microcluster_topic_and_description(cluster, text_col_name, topk) for cluster in clusters]
    responses = achat_complete(prompts, model_version=model)
    for idx, (prompt, response) in enumerate(zip(prompts, responses)):
        try:
            response = eval(response)
        except:
            one_response = chat_complete([prompt], model_version="gpt-4", temperature=0.5)
            response = eval(one_response[0][0])
        
        clusters[idx].topic = eval(response)['topic']
        clusters[idx].description = eval(response)['description']

def generate_uppercluster_topic_prompts(
    cluster: MicroCluster,
    text_col_name: str,
    topk: int,
):
    template1 = """You are a good editor. Given some requirements and prompts, you need to summarize the main topic of those prompts and give a simple description of this topic according to those requirements.
    
    Here are some requirements you MUST follow:
    1. The topic should reflect the main intent of those prompts.
    2. The topic should be less than 10 words.
    3. The description should be less than 20 words.

    Here are the prompts you need to consider all:
    {user_prompt}"""
    
    template2 = """
    The output should be in the json format:
    {"topic": <summarize the main topic of those prompts>, "description": <output a discription for this topic, less than 20 words>}
    """
    sampled_data = cluster.data[text_col_name].sample(n=min(topk, len(cluster.data)))
    prompt_str = ""
    for i, text in enumerate(sampled_data, 1):
        prompt_str += (f"{i}. {text}\n")
    prompt = template1.format(user_prompt=prompt_str) + template2
    return prompt