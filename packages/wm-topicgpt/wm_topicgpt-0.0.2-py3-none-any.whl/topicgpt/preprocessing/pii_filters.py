import re
import math
import asyncio
from tqdm import tqdm
from typing import List
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.ai.textanalytics import PiiEntityCategory
from azure.core.credentials import AzureKeyCredential
from topicgpt import config
from topicgpt.utils import timer


def authenticate_client():
    ta_credential = AzureKeyCredential(config.azure_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=config.azure_endpoint,
        credential=ta_credential
    )
    return text_analytics_client


async def name_filter(input_list: List[str]) -> List[str]:
    result = []
    client = authenticate_client()
    async with client:
        response = await client.recognize_pii_entities(documents=input_list, language="en", categories_filter = [PiiEntityCategory.PERSON], verify_ssl=False)
        result_ls = [doc for doc in response if not doc.is_error]
        for doc in result_ls:
            res= re.sub(r'[*]+', 'PersonName', doc.redacted_text)
            result.append(res)
    await client.close()
    return result

@timer
def batch_name_filter(input_list: List[str]) -> List[str]:
    results = []
    batch_size = 5 # Max 5 records are permitted.
    size = len(input_list)
    batch_num = math.ceil(size / batch_size)
    for start in tqdm(range(0, size, batch_size), total=batch_num):
        batch = input_list[start: start+batch_size]
        batch_responses = asyncio.run(name_filter(batch))
        results.extend(batch_responses)
    return results