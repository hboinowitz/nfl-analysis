from termios import VLNEXT
import pytest
import pandas as pd
from nfl_analysis.etl import utils


class TestETLUtils:
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

    def test_coordinates_usa(self, teams):
        range_latitude = [19.50139, 64.85694]
        range_longitude = [-161.75583, -68.01197]
        assert range_latitude[0] <= teams["lat"].max() <= range_latitude[1]
        assert range_longitude[0] <= teams["lon"].max() <= range_longitude[1]

    def test_parse_coordinates(self):
        lat, lon = utils.parse_coordinates("39.278°N 76.623°W")
        assert lat == 39.278
        assert lon == -76.623

        # Check missing Longitude
        with pytest.raises(ValueError):
            utils.parse_coordinates("39.278°N")

        # Check missing Latitude
        with pytest.raises(ValueError):
            utils.parse_coordinates("76.623°W")

    def test_parse_historic_team_names(self, mapping):
        expected_rams_tuple = (
            "Los Angeles Rams",
            ["Los Angeles Rams", "St. Louis Rams"],
        )
        expected_cardinals_tuple = ("Arizona Cardinals", ["Arizona Cardinals"])
        assert expected_rams_tuple == utils.parse_historic_team_names(
            "Los Angeles Rams(St. Louis Rams 1995–2015)"
        )
        assert expected_cardinals_tuple == utils.parse_historic_team_names(
            "Arizona Cardinals"
        )

        assert mapping["current_name"].isin(mapping["historic_name"]).all()
