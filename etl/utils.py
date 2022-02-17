from typing import List, Tuple, Union
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
    return overtime, *map(int, result.split(':'))

remove_brackets = lambda string_with_brakets : re.sub(r'\[.*?\]', '', string_with_brakets)
snake_case = lambda str_ : str_.lower().replace(" ", "_")

def parse_historic_team_names(team_name: str) -> Tuple[str, Union[str, List[str]]]:
    split_names = team_name.split('(')
    if len(split_names) == 1:
        historic_names = split_names
        current_name = split_names[0]
    else:
        split_names = list(map(str.strip, split_names))
        current_name = split_names[0]
        historic_names = ([name[:-11] for name in split_names[1:]])
    return current_name, historic_names

def team_names_to_mapping(team_names: pd.Series) -> pd.DataFrame:
    team_names = pd.DataFrame(team_names)
    team_names[['current_name', 'historic_name']] = team_names['Team'].apply(parse_historic_team_names).to_list()
    team_names = team_names.drop('Team', axis=1)
    return team_names.explode('historic_name').reset_index(drop=True)