import pytest
from nfl_analysis.data import load


class TestData:
    def test_loader(self):
        expected_tables = [
            "team_mapping",
            "teams",
            "superbowl_stats_per_team",
            "superbowls",
        ]

        for table in expected_tables:
            load(table)

        unexpected_table = "star_wars"

        with pytest.raises(ValueError):
            load(unexpected_table)
