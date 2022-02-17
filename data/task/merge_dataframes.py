from typing import Dict
import pandas as pd


def merge_dataframes(json1, json2):
    if isinstance(json2, Dict):
        return json1
    df1 = pd.read_json(json1)
    df2 = pd.read_json(json2)
    df3 = pd.concat([df1, df2])
    df3.fillna(0, inplace=True)
    df3.drop_duplicates(inplace=True)
    df_json = df3.to_json(orient="split")
    return df_json
