import json

from nba_warehouse.api import NBAApi
from nba_warehouse.teams import get_teams, Team

class TestGetTeams(object):
    @classmethod
    def setup_class(self):
        self.teams = get_teams()
        with open('tests/teams.json') as json_in:
            self.teams_json = json.load(json_in)

    def test_teams_api_return_response(self):
        """api call for teams should return proper data"""
        api = NBAApi("https://data.nba.net/prod/v2/2018/teams.json")
        response = api.get()

        assert response is not None

    def test_teams_api_returns_valid_json_response(self):
        """api call should return expected json"""
        api = NBAApi("https://data.nba.net/prod/v2/2018/teams.json")
        response = api.get()

        assert response.json() == self.teams_json

    def test_get_teams_returns_a_list(self):
        """get_teams should return a list"""
        assert type(self.teams) == list

    def test_get_teams_returns_a_list_of_team_objects(self):
        """get_teams should return a list of Team objects"""
        assert type(self.teams[0]) == Team

    def test_team_object_has_expected_attributes(self):
        """get_teams should return a Team object with proper attributes set"""
        expected = ("is_nba_franchise", "is_all_star", "city", "alt_city_name",
        "full_name", "tricode", "team_id", "nickname", "url_name",
        "conf_name", "div_name",)

        assert self.teams[0]._fields == expected

    def test_is_nba_franchise_attribute_is_type_boolean(self):
        """is_nba_franchise attribute should be a boolean"""
        assert type(self.teams[0].is_nba_franchise) == bool
        
    def test_is_all_star_attribute_is_type_boolean(self):
        """is_all_star attribute should be a boolean"""
        assert type(self.teams[0].is_all_star) == bool

    def test_city_attribute_is_type_string(self):
        """city attribute should be a string"""
        assert type(self.teams[0].city) == str

    def test_alt_city_name_attribute_is_type_string(self):
        """alt_city_name attribute should be a string"""
        assert type(self.teams[0].alt_city_name) == str

    def test_full_name_attribute_is_type_string(self):
        """full_name attribute should be a string"""
        assert type(self.teams[0].full_name) == str

    def test_tricode_attribute_is_type_string(self):
        """tricode attribute should be a string"""
        assert type(self.teams[0].tricode) == str
  
    def test_team_id_attribute_is_type_string(self):
        """team_id attribute should be a string"""
        assert type(self.teams[0].team_id) == str

    def test_nickname_attribute_is_type_string(self):
        """nickname attribute should be a string"""
        assert type(self.teams[0].nickname) == str

    def test_url_name_attribute_is_type_string(self):
        """url_name attribute should be a string"""
        assert type(self.teams[0].url_name) == str

    def test_conf_name_attribute_is_type_string(self):
        """is_nba_franchise attribute should be a string"""
        assert type(self.teams[0].conf_name) == str

    def test_div_name_attribute_is_type_string(self):
        """is_nba_franchise attribute should be a string"""
        assert type(self.teams[0].div_name) == str

