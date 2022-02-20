import utils
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title='NFL Analysis', layout="wide")
st.title('NFL Analysis 🏈')

@st.cache(suppress_st_warning = True, allow_output_mutation=True)
def load_teams():
    teams = pd.read_parquet("../data/teams.parquet")
    return teams

@st.cache(suppress_st_warning = True, allow_output_mutation=True)
def load_superbowl():
    superbowls = pd.read_parquet("../data/superbowls.parquet")
    return superbowls

@st.cache(suppress_st_warning = True, allow_output_mutation=True)
def load_mapping():
    mapping = pd.read_parquet("../data/team_mapping.parquet")
    return mapping


# Load data
teams = load_teams()
superbowls = load_superbowl()
mapping = load_mapping()

teams = utils.add_league_for_teams(teams)
map_of_teams = utils.generate_map_for_teams(teams)
st.plotly_chart(map_of_teams)

superbowl_points_figure = utils.generate_superbowl_points_plot(superbowls)
st.plotly_chart(superbowl_points_figure)

wins_and_losses_per_division_cumulated, combined_wins_and_losses = utils.get_cumulated_wins_per_division(superbowls, mapping, teams)

wins_and_losses_per_division_figure = utils.plot_wins_and_losses_per_division(wins_and_losses_per_division_cumulated, 'NFC', 'East')

apperances_per_division = (
    combined_wins_and_losses.groupby(['league', 'division'])
                            .agg(wins = ('winner', 'sum'), losses = ('looser', 'sum'))
)

st.plotly_chart(wins_and_losses_per_division_figure)
st.markdown('#### Overview of the Wins and Losses per Division')
st.dataframe(apperances_per_division)