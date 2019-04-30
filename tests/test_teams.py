import json
from unittest import skipIf
from unittest.mock import patch, Mock

import pytest

from constants import SKIP_REAL
from nba_warehouse.api import NBAApi
from nba_warehouse.teams import get, Team
from tests.fixtures import json_teams


@pytest.fixture
def mock_json_teams():
    return json_teams


class TestGetTeams(object):
    @classmethod
    def setup_class(self):
        self.mock_requests_patcher = patch("nba_warehouse.api.requests.get")
        self.mock_requests = self.mock_requests_patcher.start()

    def test_get_teams_returns_a_list(self, mock_json_teams):
        """get should return a list"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams) == list

    def test_get_teams_returns_a_list_of_team_objects(self, mock_json_teams):
        """get should return a list of Team objects"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0]) == Team

    def test_team_object_has_expected_attributes(self, mock_json_teams):
        """get should return a Team object with proper attributes set"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        expected = (
            "is_nba_franchise",
            "is_all_star",
            "city",
            "alt_city_name",
            "full_name",
            "tricode",
            "team_id",
            "nickname",
            "url_name",
            "conf_name",
            "div_name",
        )

        assert teams[0]._fields == expected

    def test_is_nba_franchise_attribute_is_type_boolean(self, mock_json_teams):
        """is_nba_franchise attribute should be a boolean"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].is_nba_franchise) == bool

    def test_is_all_star_attribute_is_type_boolean(self, mock_json_teams):
        """is_all_star attribute should be a boolean"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].is_all_star) == bool

    def test_city_attribute_is_type_string(self, mock_json_teams):
        """city attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].city) == str

    def test_alt_city_name_attribute_is_type_string(self, mock_json_teams):
        """alt_city_name attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].alt_city_name) == str

    def test_full_name_attribute_is_type_string(self, mock_json_teams):
        """full_name attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].full_name) == str

    def test_tricode_attribute_is_type_string(self, mock_json_teams):
        """tricode attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].tricode) == str

    def test_team_id_attribute_is_type_string(self, mock_json_teams):
        """team_id attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].team_id) == str

    def test_nickname_attribute_is_type_string(self, mock_json_teams):
        """nickname attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].nickname) == str

    def test_url_name_attribute_is_type_string(self, mock_json_teams):
        """url_name attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].url_name) == str

    def test_conf_name_attribute_is_type_string(self, mock_json_teams):
        """is_nba_franchise attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].conf_name) == str

    def test_div_name_attribute_is_type_string(self, mock_json_teams):
        """is_nba_franchise attribute should be a string"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get()

        assert type(teams[0].div_name) == str

    def test_when_nba_only_param_true_only_nba_returned(self, mock_json_teams):
        """when nba_only is true get should only return nba_teams"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        teams = get(nba_only=True)

        assert any(not team.is_nba_franchise for team in teams) == False

    def test_when_nba_only_param_false_all_returned(self, mock_json_teams):
        """when nba_only is false all teams should be returned"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        expected = get()

        teams = get(nba_only=False)

        assert len(expected) == len(teams)

    def test_when_not_nba_only_param_all_returned(self, mock_json_teams):
        """when no nba_only param is passed all teams should be returned"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_teams

        expected = get()

        teams = get()

        assert len(expected) == len(teams)


@skipIf(SKIP_REAL, "Skipping tests that hit the real api server")
def test_integration_contract(mock_json_teams):
    # Get the raw api response
    api = NBAApi("https://data.nba.net/prod/v2/2018/teams.json")
    actual_keys = api.get().json()["league"]["standard"][0].keys()

    # Call the service to hit mocked API
    with patch("nba_warehouse.api.requests.get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = mock_json_teams

        mocked_keys = mock_json_teams["league"]["standard"][0].keys()

    assert list(actual_keys) == list(mocked_keys)
