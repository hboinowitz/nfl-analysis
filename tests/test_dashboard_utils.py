import pytest
import pandas as pd
from nfl_analysis.dashboard import utils

class TestDashboardUtils:
    @pytest.fixture
    def teams(self):
        teams = pd.read_parquet("nfl_analysis/data/teams.parquet")
        return teams
    
    @pytest.fixture
    def superbowls(self):
        superbowls = pd.read_parquet("nfl_analysis/data/superbowls.parquet")
        return superbowls
    
    @pytest.fixture
    def mapping(self):
        mapping = pd.read_parquet("nfl_analysis/data/team_mapping.parquet")
        return mapping

    @pytest.fixture
    def num_of_superbowls(self, superbowls):
        from datetime import datetime
        num_of_superbowls = (
            superbowls[superbowls['datum'] < datetime.today()].drop_duplicates('datum').reset_index().shape[0]
        )
        return num_of_superbowls

    def test_add_league(self, teams):
        teams = utils.add_league_for_teams(teams)
        assert (teams.loc[16:, 'league'] == 'NFC').all()
        assert (teams.loc[:16, 'league'] == 'AFC').all()

    def test_expand_superbowl_data_vertically(self, superbowls, mapping, teams, num_of_superbowls):
        expanded_data = utils.expand_superbowl_data_vertically(superbowls, mapping, teams)
        expanded_data_agg = expanded_data.groupby(['league', 'division']).agg(wins = ('winner', 'sum'), losses = ('looser', 'sum'))
        assert expanded_data_agg.sum().loc['wins'] == expanded_data_agg.sum().loc['losses']
        assert expanded_data_agg.sum().loc['wins'] == num_of_superbowls
    
    def test_add_current_team_names_to_superbowl_data(self, superbowls, mapping, num_of_superbowls):
        superbowls_current_teams = (
            utils.add_current_team_names_to_superbowl_data(superbowls, mapping).drop_duplicates('datum')
        )
        
        assert superbowls_current_teams.shape == (num_of_superbowls, 3)
        assert superbowls_current_teams['current_name_looser'].isin(mapping['current_name']).all()
        
        expected_columns = ['datum', 'current_name_looser', 'current_name_winner']
        assert all([column in expected_columns for column in superbowls_current_teams.columns])