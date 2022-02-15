import utils

import pandas as pd

def import_nfl_team_data():
    ## Load data for NFL teams
    nfl_teams = utils.get_wiki_table("https://en.wikipedia.org/wiki/National_Football_League")

    ## Cleaning up

    # Drop column multi-index
    nfl_teams_cleaned = nfl_teams.droplevel(1, axis=1)

    # Rename columns
    nfl_teams_cleaned = nfl_teams_cleaned.rename(utils.snake_case, axis=1)
    nfl_teams_cleaned = nfl_teams_cleaned.rename(utils.remove_brackets, axis=1)

    # Remove footnotes
    nfl_teams_cleaned = nfl_teams_cleaned.applymap(utils.remove_brackets)
    nfl_teams_cleaned.iloc[0]['coordinates'] 
    nfl_teams_cleaned.iloc[2]['coordinates']

    nfl_teams_cleaned['founding_member'] = nfl_teams_cleaned['club'].apply(lambda club : "†" in club)
    nfl_teams_cleaned['relocated'] = nfl_teams_cleaned['club'].apply(lambda club : "*" in club)

    remove_footnotes_in_teams_column = lambda team_with_footnote : team_with_footnote.replace("†","").replace("*","")
    nfl_teams_cleaned['club'] = nfl_teams_cleaned['club'].apply(remove_footnotes_in_teams_column)

    nfl_teams_cleaned = nfl_teams_cleaned[nfl_teams_cleaned['division'].isin(['East', 'West', 'North', 'South'])]
    nfl_teams_cleaned[['lat', 'lon']] = nfl_teams_cleaned['coordinates'].apply(utils.parse_coordinates).to_list()
    nfl_teams_cleaned.to_parquet('../data/teams.parquet')