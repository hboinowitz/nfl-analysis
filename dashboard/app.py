#%%
import utils
import pandas as pd
import numpy as np
import streamlit as st

st.title('NFL Analysis')
teams = pd.read_parquet("../data/teams.parquet")
teams = utils.add_league_for_teams(teams)
map_of_teams = utils.generate_map_for_teams(teams)
st.plotly_chart(map_of_teams)

