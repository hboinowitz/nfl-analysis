import utils
import pandas as pd
import numpy as np
import streamlit as st

st.title('NFL Analysis')

@st.cache()
def load_teams():
    teams = pd.read_parquet("../data/teams.parquet")
    return teams

@st.cache(suppress_st_warning = True, allow_output_mutation=True)
def load_superbowl():
    superbowls = pd.read_parquet("../data/superbowls.parquet")
    return superbowls

# Load data
teams = load_teams()
superbowls = load_superbowl()

teams = utils.add_league_for_teams(teams)
map_of_teams = utils.generate_map_for_teams(teams)
st.plotly_chart(map_of_teams)

