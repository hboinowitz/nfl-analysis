from typing import Tuple
from bs4 import BeautifulSoup
import requests as rq
import pandas as pd
import regex as re
import numpy as np

def get_wiki_table(url:str, first: bool = True) -> pd.DataFrame:
    """Load a table from Wikipedia for a given URL

    :param url: The url to request the table from
    :type url: str
    :param first: Boolean indicating, if all tables or just the first
    one should be returned
    :type num_table: bool
    :return: A pandas DataFrame containing the requested table
    :rtype: pd.DataFrame
    """
    response = rq.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_HTML = soup.findAll('table',{'class':"wikitable"})
    if first:
        return pd.read_html(str(table_HTML))[0]
    return pd.read_html(str(table_HTML))

def parse_coordinates(coordinates: str) -> str:

    combined_decimal_lon_lat = coordinates.replace("\ufeff", "").split('/')[-1]
    lon, lat = combined_decimal_lon_lat.split('°N ')
    lon = float(lon.strip())
    lat = float(f"-{lat[:-2].strip()}")
    return lat, lon

def parse_result(result: str) -> Tuple[int, int, bool]:
    overtime = False
    if pd.isna(result):
        return [np.nan for i in range(3)]
    splitted_result = result.split()
    if len(splitted_result) > 2:
        return ValueError("The `result` you have passed does not match the reuiqred format.")
    if len(splitted_result) == 2:
        result = "".join(splitted_result[:-1])
        overtime = True
    return overtime, *result.split(':')

remove_brackets = lambda string_with_brakets : re.sub(r'\[.*?\]', '', string_with_brakets)
snake_case = lambda str_ : str_.lower().replace(" ", "_")
