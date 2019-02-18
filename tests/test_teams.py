from unittest.mock import Mock, patch

from nba_warehouse.teams import get_teams, get_nba_teams


class TestAllTeams(object):
    @classmethod
    def setup_class(self):
        self.mock_get_patcher = patch("nba_warehouse.teams.requests.get")
        self.mock_get = self.mock_get_patcher.start()
        self.teams = {
            "league": {
                "standard": [
                    {
                        "isNBAFranchise": "true",
                        "isAllStar": "false",
                        "city": "Charlotte",
                        "altCityName": "Charlotte",
                        "fullName": "Charlotte Hornets",
                        "tricode": "CHA",
                        "teamId": "1610612766",
                        "nickname": "Hornets",
                        "urlName": "hornets",
                        "confName": "East",
                        "divName": "Southeast",
                    },
                    {
                        "isNBAFranchise": "false",
                        "isAllStar": "false",
                        "city": "Team",
                        "altCityName": "Team",
                        "fullName": "Team Africa",
                        "tricode": "AFR",
                        "teamId": "12326",
                        "nickname": "Africa",
                        "urlName": "africa",
                        "confName": "",
                        "divName": "",
                    },
                    {
                        "isNBAFranchise": "true",
                        "isAllStar": "false",
                        "city": "Atlanta",
                        "altCityName": "Atlanta",
                        "fullName": "Atlanta Hawks",
                        "tricode": "ATL",
                        "teamId": "1610612737",
                        "nickname": "Hawks",
                        "urlName": "hawks",
                        "confName": "East",
                        "divName": "Southeast",
                    },
                ]
            }
        }

    @classmethod
    def teardown_class(self):
        self.mock_get_patcher.stop()

    def test_request_response_is_ok(self):
        self.mock_get.return_value = Mock(ok=True)
        self.mock_get.return_value.json.return_value = self.teams

        response = get_teams()

        assert response.ok is True
        assert response.json() == self.teams

    def test_request_response_is_not_ok(self):
        self.mock_get.return_value = Mock(ok=False)

        response = get_teams()

        assert response is None


class TestNBATeams(object):
    @classmethod
    def setup_class(self):
        self.mock_get_teams_patcher = patch("nba_warehouse.teams.get_teams")
        self.mock_get_teams = self.mock_get_teams_patcher.start()
        self.teams = {
            "league": {
                "standard": [
                    {
                        "isNBAFranchise": "true",
                        "isAllStar": "false",
                        "city": "Charlotte",
                        "altCityName": "Charlotte",
                        "fullName": "Charlotte Hornets",
                        "tricode": "CHA",
                        "teamId": "1610612766",
                        "nickname": "Hornets",
                        "urlName": "hornets",
                        "confName": "East",
                        "divName": "Southeast",
                    },
                    {
                        "isNBAFranchise": "false",
                        "isAllStar": "false",
                        "city": "Team",
                        "altCityName": "Team",
                        "fullName": "Team Africa",
                        "tricode": "AFR",
                        "teamId": "12326",
                        "nickname": "Africa",
                        "urlName": "africa",
                        "confName": "",
                        "divName": "",
                    },
                    {
                        "isNBAFranchise": "true",
                        "isAllStar": "false",
                        "city": "Atlanta",
                        "altCityName": "Atlanta",
                        "fullName": "Atlanta Hawks",
                        "tricode": "ATL",
                        "teamId": "1610612737",
                        "nickname": "Hawks",
                        "urlName": "hawks",
                        "confName": "East",
                        "divName": "Southeast",
                    },
                ]
            }
        }

    @classmethod
    def teardown_class(self):
        self.mock_get_teams_patcher.stop()

    def test_getting_only_nba_teams(self):
        self.mock_get_teams.return_value = Mock()
        self.mock_get_teams.return_value.json.return_value = self.teams

        nba_teams = get_nba_teams()

        assert self.mock_get_teams.called == True
        assert nba_teams == [
            self.teams["league"]["standard"][0],
            self.teams["league"]["standard"][2],
        ]
