import utils
import regex as re
import pandas as pd

def import_nfl_team_data():
    ## Load data for NFL teams
    nfl_teams = utils.get_wiki_table("https://en.wikipedia.org/wiki/National_Football_League")

    ## Cleaning up
    remove_brackets = lambda string_with_brakets : re.sub(r'\[.*?\]', '', string_with_brakets)

    # Drop column multi-index
    nfl_teams_cleaned = nfl_teams.droplevel(1, axis=1)

    # Rename columns
    snake_case = lambda str_ : str_.lower().replace(" ", "_")
    nfl_teams_cleaned = nfl_teams_cleaned.rename(snake_case, axis=1)
    nfl_teams_cleaned = nfl_teams_cleaned.rename(remove_brackets, axis=1)

    # Remove footnotes
    nfl_teams_cleaned = nfl_teams_cleaned.applymap(remove_brackets)
    nfl_teams_cleaned.iloc[0]['coordinates'] 
    nfl_teams_cleaned.iloc[2]['coordinates']

    nfl_teams_cleaned['founding_member'] = nfl_teams_cleaned['club'].apply(lambda club : "†" in club)
    nfl_teams_cleaned['relocated'] = nfl_teams_cleaned['club'].apply(lambda club : "*" in club)

    remove_footnotes_in_teams_column = lambda team_with_footnote : team_with_footnote.replace("†","").replace("*","")
    nfl_teams_cleaned['club'] = nfl_teams_cleaned['club'].apply(remove_footnotes_in_teams_column)

    nfl_teams_cleaned = nfl_teams_cleaned[nfl_teams_cleaned['division'].isin(['East', 'West', 'North', 'South'])]
    nfl_teams_cleaned[['lat', 'lon']] = nfl_teams_cleaned['coordinates'].apply(utils.parse_coordinates).to_list()
    nfl_teams_cleaned.to_parquet('../data/teams.parquet')