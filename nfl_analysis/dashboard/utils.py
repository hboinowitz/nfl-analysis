import pandas as pd
import plotly.graph_objects as go
import numpy as np

def add_league_for_teams(teams: pd.DataFrame) -> pd.DataFrame:
    teams['league'] = np.nan
    teams.loc[:16, 'league'] = 'AFC'
    teams.loc[16:, 'league'] = 'NFC'
    return teams

def generate_map_for_teams(teams: pd.DataFrame) -> go.Figure:
    # Prepare mapping of league to colors
    color_mapping = {'NFC': 'blue', 'AFC': 'red'}
    color_for_team = teams['league'].map(color_mapping)
    
    # Prepare mapping of division to shape
    symbol_mapping = {'East': 'triangle-down', 'North': 'triangle-up', 
                      'West': 'circle', 'South': 'square'}
    symbol_for_team = teams['division'].map(symbol_mapping)

    fig = go.Figure(data=go.Scattergeo(
            lon = teams['lat'],
            lat = teams['lon'],
            text = teams['club'],
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                symbol = symbol_for_team,
                color = color_for_team
            )
            )
    )

    fig.update_layout(
            autosize=False,
            width = 1300,
            height = 800,
            title = 'NFL-Teams',
            geo_scope='usa',
        )
    return fig

def generate_superbowl_points_plot(superbowl: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
            x = superbowl['datum'].dt.year,
            y = superbowl['total_points'],
            line_color = 'rgba(0, 0, 255, .3)',
            name = 'total points'
        )
    )

    fig.add_trace(go.Scatter(
            x = superbowl['datum'].dt.year,
            y = superbowl['points_winner'],
            name = 'points winner'
        )
    )

    fig.add_trace(go.Scatter(
            x = superbowl['datum'].dt.year,
            y = superbowl['points_looser'],
            name = 'points looser'
        )
    )

    fig.update_layout(
            width = 1000,
            height = 500,
            title = 'Points in the Superbowls',
            xaxis_title = 'year',
            yaxis_title = 'points'
    )

    return fig

def plot_wins_and_losses_per_division(
    wins_and_losses_per_division_cumulated: pd.DataFrame, 
    league: str, 
    division: str
):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
            x = wins_and_losses_per_division_cumulated.index.year,
            y = wins_and_losses_per_division_cumulated[('winner', league, division)],
            line_color = 'rgba(0, 0, 255, .3)',
            name = 'wins'
        )
    )

    fig.add_trace(go.Scatter(
            x = wins_and_losses_per_division_cumulated.index.year,
            y = wins_and_losses_per_division_cumulated[('looser', league, division)],
            name = 'losses'
        )
    )
    fig.update_layout(
            width = 1000,
            height = 500,
            title = f'Appearances of the {league} {division} in the Super Bowl',
            xaxis_title = 'year',
            yaxis_title = 'appearances'
    )

    return fig

def add_current_team_names_to_superbowl_data(superbowl: pd.DataFrame, mapping: pd.DataFrame):
    superbowls_with_current_team_names = (
    superbowl.merge(mapping, left_on='sieger', 
                        right_on='historic_name')
                  .merge(mapping, left_on='verlierer', 
                        right_on='historic_name', suffixes = ('_winner', '_looser'))
                  .sort_values('datum')
    )[['datum', 'current_name_looser', 'current_name_winner']]

    return superbowls_with_current_team_names

def get_mapping_club_to_division(teams: pd.DataFrame):
    teams = add_league_for_teams(teams)
    mapping_club_to_divison = teams[['club', 'division', 'league']]
    return mapping_club_to_divison

def add_divisions_to_superbowl_data(superbowl: pd.DataFrame, mapping: pd.DataFrame, teams: pd.DataFrame):
    mapping_club_to_divison = get_mapping_club_to_division(teams)
    superbowls_nfl_with_current_team_names = add_current_team_names_to_superbowl_data(superbowl, mapping)

    superbowls_nfl_with_divisions = (
        superbowls_nfl_with_current_team_names.merge(mapping_club_to_divison,        
                                                        left_on='current_name_winner',
                                                        copy=False, 
                                                        right_on='club')
                                            .merge(mapping_club_to_divison, 
                                                        left_on='current_name_looser', 
                                                        right_on='club',
                                                        copy=False, 
                                                        suffixes = ('_winner', '_looser'))
                                            .sort_values('datum')
    )

    return superbowls_nfl_with_divisions

def seperate_looser_and_winner_frame(base_frame: pd.DataFrame, indicator: str):
    seperated_frame = base_frame[['datum', f'league_{indicator}', f'division_{indicator}']]
    remove_indicator = lambda str_with_indicator: str_with_indicator.replace(f"_{indicator}", "")
    seperated_frame = seperated_frame.rename(remove_indicator, axis=1)
    seperated_frame[indicator] = 1
    
    return seperated_frame

def expand_superbowl_data_vertically(superbowl: pd.DataFrame, mapping: pd.DataFrame, teams: pd.DataFrame):
    superbowls_nfl_with_divisions = add_divisions_to_superbowl_data(superbowl, mapping, teams)
    superbowls_nfl_with_divisions = superbowls_nfl_with_divisions.drop_duplicates('datum')
    winner = seperate_looser_and_winner_frame(superbowls_nfl_with_divisions, 'winner')
    looser = seperate_looser_and_winner_frame(superbowls_nfl_with_divisions, 'looser')
    combined_wins_and_losses = pd.concat([winner, looser]).fillna(0)

    return combined_wins_and_losses

def get_cumulated_wins_per_division(superbowl: pd.DataFrame, mapping: pd.DataFrame, teams: pd.DataFrame):
    combined_wins_and_losses = expand_superbowl_data_vertically(superbowl, mapping, teams)
    wins_and_losses_per_division_cumulated = (
        combined_wins_and_losses.pivot(index='datum', columns=['league','division'], values=['winner', 'looser'])
                .fillna(0).cumsum()
    )

    return wins_and_losses_per_division_cumulated, combined_wins_and_losses