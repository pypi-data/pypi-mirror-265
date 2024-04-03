import pandas as pd


def _count_words(text: str) -> int:
    return len(str(text).strip().split()) if text else 0


def drop_short_words_data(
    dataframe: pd.DataFrame,
    col_name: str,
    min_words: int,
) -> pd.DataFrame:
    
    dataframe['count'] = dataframe[col_name].apply(_count_words)
    dataframe = dataframe[dataframe['count'] >= min_words]
    dataframe = dataframe.drop(columns=['count'])
    dataframe.reset_index(drop=True, inplace=True)
    return dataframe


def drop_long_words_data(
    dataframe: pd.DataFrame,
    col_name: str,
    max_words: int,
) -> pd.DataFrame:
    
    dataframe['count'] = dataframe[col_name].apply(_count_words)
    dataframe = dataframe[dataframe['count'] <= max_words]
    dataframe = dataframe.drop(columns=['count'])
    dataframe.reset_index(drop=True, inplace=True)
    return dataframe