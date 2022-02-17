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
            title = 'NFL-Teams',
            geo_scope='usa',
        )
    return fig