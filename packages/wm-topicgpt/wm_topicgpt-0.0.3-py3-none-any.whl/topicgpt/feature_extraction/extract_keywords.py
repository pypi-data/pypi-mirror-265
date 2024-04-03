import spacy
import pandas as pd
import multiprocessing
from typing import List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from topicgpt.utils import timer
from topicgpt.walmart_llm import achat_complete


nlp = spacy.load("en_core_web_sm")

def spacy_tokenizer(text, nlp):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])

def parallel_tokenize(texts, nlp):
    with multiprocessing.Pool() as pool:
        tokenized_texts = pool.starmap(spacy_tokenizer, [(text, nlp) for text in texts])
    return tokenized_texts

@timer
def extract_cluster_keywords_tfidf(
    clusters: List[Any],
    col_name: str,
    topk: int = 10,
    ngram_range: tuple = (1, 2),
    tokenizer: bool = False,
):
    corpus = ['. '.join(cluster.data[col_name].tolist()) for cluster in clusters]
    processed_corpus = parallel_tokenize(corpus, nlp) if tokenizer else corpus
    vectorizer = TfidfVectorizer(ngram_range=ngram_range, stop_words='english')
    tfidf = vectorizer.fit_transform(processed_corpus)

    feature_names = vectorizer.get_feature_names_out()
    for idx, cluster in enumerate(clusters):
        tfidf_values = tfidf[idx].toarray().flatten()
        sorted_indices = tfidf_values.argsort()[::-1]
        top_keywords_indices = sorted_indices[:topk]
        top_keywords = [feature_names[idx] for idx in top_keywords_indices]
        cluster.keywords = top_keywords

@timer
def extract_keywords_by_llm(
    dataframe: pd.DataFrame, 
    text_col_name: str, 
    model: str = "gpt-35-turbo",
    temperature: float = 0.,
    batch_size: int = 300,
):
    
    template1 = """You are a good editor. Given a paragraph, your task is to extract several keywords from this paragraph according to the following requirements.
    
    Here are some requirements that you must adhere to:
    1. DON'T output person's name.
    2. Must extract less than 10 keywords.
        
    Here is the paragraph:
    {user_input}
    """
    template2 = """
    Your output should follow the json template below.
    {"keywords":["keyword1", "keyword2", "keyword3",...]}"""
    
    prompts = []
    for text in dataframe[text_col_name]:
        prompts.append(template1.format(user_input=text) + template2)

    responses = achat_complete(prompts, model_version=model, temperature=temperature, batch=batch_size)
    keywords = []
    count = 0
    for response in responses:
        try:
            word_list = eval(response)['keywords']
            keyword = ",".join([word.lower() for word in word_list])
        except:
            keyword = "#error#"
            print(f"#error: {count}")
            count += 1
        keywords.append(keyword)
    return keywords
