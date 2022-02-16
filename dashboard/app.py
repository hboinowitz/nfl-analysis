#%%
import pandas as pd
teams = pd.read_parquet("../data/teams.parquet")
teams['league'] = pd.np.nan
teams['league'].iloc[:16] = 'AFC'
teams['league'].iloc[16:] = 'NFC'
#%%
import plotly.graph_objects as go

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
            symbol = teams['division'].map({'East':'triangle-down', 'North':'triangle-up', 'West':'circle', 'South':'square'}),
            color = pd.Series(teams['league'] == 'NFC', dtype=int)
        )
        )
)

fig.update_layout(
        title = 'NFL-Teams',
        geo_scope='usa',
    )
fig.show()