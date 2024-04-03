import warnings
warnings.filterwarnings("ignore")
import os
import yaml
import time
import math
import asyncio
from tqdm import tqdm
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode
from langchain.schema import HumanMessage
from topicgpt.walmart_llm.chat_model import WalmartAzureOpenAiChatModels
from topicgpt.walmart_llm.embed_model import WalmartAzureOpenaiEmbeddings
from topicgpt import config

os.environ['OPENAI_API_KEY'] = config.consumer_id


def get_timestamp() -> int:
    """Create timestamp
    Returns:
        int: timestamp
    """
    return int(time.time()) * 1000
 
def sign_data(private_key: str, data: str) -> bytes:
    """Create authorization signature
    Args:
        private_key (str): Path to private key
        data (str): Additional information needed to generate key in format:
            consumer_id
            timestamp
            key version
    Returns:
        bytes: authorization signature
    """
    key = open(private_key, "r").read()
    rsakey = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data.encode("utf-8"))
    sign = signer.sign(digest)
    return b64encode(sign)
 
def generate_auth_sig(consumer_id: str, private_key_path: str, key_version: str = "1"):
    """_summary_
    Args:
        consumer_id (str): Service App. consumer ID
        private_key_path (str): private key path
        key_version (str) , Defaults to "1" : SOA key version
    Returns:
        tuple: epoch_time, auth_signature
    """
    epoch_time = get_timestamp()
    data = f"{consumer_id}\n{epoch_time}\n{key_version}\n"
    auth_signature = sign_data(private_key_path, data).decode()
    return epoch_time, auth_signature


def instantiate_walmart_chat_completion(model_version="gpt-35-turbo", temperature=0.):
    """The helper function that calls LLM gateway LLM
    Args:
        temperature (_type_): _description_
        max_tokens (_type_): _description_
        top_p (_type_): _description_
        presence_penalty (_type_): _description_
        frequency_penalty (_type_): _description_
        model_version (str): LLM model version
    Returns:
        _type_: _description_
    """
    epoch_ts, auth_sig = generate_auth_sig(config.consumer_id, config.private_key_path)
    consumer_params = {
        "consumer_id": config.consumer_id,
        "consumer_timestamp": str(epoch_ts),
        "consumer_key_version": "1",
        "consumer_auth_signature": auth_sig,
        "svc_env": config.mso_llm_env,
    }
    chat_client = WalmartAzureOpenAiChatModels(
        vendor="azure-openai",
        task="chat/completions",
        model_name=model_version,
        temperature=temperature,
        **consumer_params,
    )
    return chat_client

def achat_complete(messages, model_version="gpt-35-turbo", temperature=0., batch=500):

    @retry(wait=wait_random_exponential(min=2, max=60), stop=stop_after_attempt(6))
    async def batch_achat_complete(model, messages):
        res = await model.agenerate(messages)
        return res.generations
    
    size = len(messages)
    batchs = math.ceil(size/batch)
    llm = instantiate_walmart_chat_completion(
        model_version=model_version,
        temperature=temperature
    )
    
    responses = []
    for start in tqdm(range(0, size, batch), total=batchs):
        batch_messages = [[HumanMessage(content=message)] for message in messages[start: start+batch]]
        batch_responses = asyncio.run(batch_achat_complete(llm, batch_messages))
        responses.extend([response[0].text for response in batch_responses])
    return responses

def chat_complete(messages, model_version="gpt-35-turbo", temperature=0.):
    llm = instantiate_walmart_chat_completion(
        model_version=model_version,
        temperature=temperature
    )
    new_messages = [[HumanMessage(content=message)] for message in messages]
    res = llm.generate(new_messages)
    return res.generations

def instantiate_walmart_embedding(model_version="text-embedding-ada-002"):
    epoch_ts, auth_sig = generate_auth_sig(config.consumer_id, config.private_key_path)
    consumer_params = {
        "consumer_id": config.consumer_id,
        "consumer_timestamp": str(epoch_ts),
        "consumer_key_version": "1",
        "consumer_auth_signature": auth_sig,
        "svc_env": config.mso_llm_env,
    }
    embedding_client = WalmartAzureOpenaiEmbeddings(vendor="azure-openai", model_name=model_version, **consumer_params)
    return embedding_client

@retry(wait=wait_random_exponential(min=2, max=60), stop=stop_after_attempt(6))
def embed_documents(documents, model_version="text-embedding-ada-002"):
    model = instantiate_walmart_embedding(model_version=model_version)
    embeddings = model.embed_documents(documents)
    return embeddings

def embed_documents_by_batch(documents, model_version="text-embedding-ada-002", batch_size=100):
    
    @retry(wait=wait_random_exponential(min=2, max=60), stop=stop_after_attempt(6))
    def embed_batch_documents(batch_documents, model):
        return model.embed_documents(batch_documents)
    
    def embed_each_documents(batch_documents, model):
        embeddings = []
        for document in batch_documents:
            try:
                embedding = model.embed_query(document)
            except:
                print("API Error:", document)
                embedding = []
            embeddings.append(embedding)
        return embeddings
    
    model = instantiate_walmart_embedding(model_version=model_version)
    embeddings = []
    size = len(documents)
    for start in tqdm(range(0, size, batch_size), total=math.ceil(size/batch_size)):
        batch_documents = documents[start: start + batch_size]
        try:
            batch_embeddings = embed_batch_documents(batch_documents, model)
        except:
            batch_embeddings = embed_each_documents(batch_documents, model)
        
        embeddings.extend(batch_embeddings)
    return embeddings