import math
import asyncio
from tqdm import tqdm
from typing import List
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from topicgpt.walmart_llm import embed_documents_by_batch
from topicgpt.utils import timer

def _embedding_documents_with_BGE(
    data: List[str],
    batch_size: int = 500, 
    device: str = "mps",
) -> List[float]:
    """Embedding a list of texts"""
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": True}
    hf = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    embeddings = []
    for start in tqdm(range(0, len(data), batch_size), total=math.ceil(len(data)/batch_size)):
        batch_texts = data[start: start+batch_size]
        batch_embeddings = asyncio.run(hf.aembed_documents(batch_texts))
        embeddings.extend(batch_embeddings)
    return embeddings

@timer
def embed_documents(
    data: List[str],
    model_name: str,
    batch_size: int = 100,
    device: str = "mps",
) -> List[float]:
    
    if model_name == "ada-002":
        return embed_documents_by_batch(data, batch_size=batch_size)
    elif model_name == "bge-small":
        return _embedding_documents_with_BGE(data, batch_size=batch_size, device=device)
    else:
        raise ValueError("Only support 'ada-002' and 'bge-small' models")