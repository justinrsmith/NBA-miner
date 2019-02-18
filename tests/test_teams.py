from unittest import skipIf
from unittest.mock import Mock, patch

from nba_warehouse.teams import get_teams, get_nba_teams
from constants import SKIP_REAL


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


@skipIf(SKIP_REAL, "Skipping tests that hit the real API server")
def test_integeration_contract():
    # Call the service to hit actual API
    teams = get_teams()
    actual_keys = teams.json().keys()

    # Call the esrvice to hit the mocked API
    with patch("nba_warehouse.teams.requests.get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "_internal": {
                "pubDateTime": "2018-08-30 20:00:04.422",
                "xslt": "xsl/league/roster/marty_teams_list.xsl",
                "eventName": "league_roster",
            },
            "league": {
                "standard": [
                    {
                        "isNBAFranchise": "false",
                        "isAllStar": "false",
                        "city": "Adelaide",
                        "altCityName": "Adelaide",
                        "fullName": "Adelaide 36ers",
                        "tricode": "ADL",
                        "teamId": "15019",
                        "nickname": "36ers",
                        "urlName": "36ers",
                        "confName": "Intl",
                        "divName": "",
                    },
                    {
                        "isNBAFranchise": "true",
                        "isAllStar": "false",
                        "city": "Miami",
                        "altCityName": "Miami",
                        "fullName": "Miami Heat",
                        "tricode": "MIA",
                        "teamId": "1610612748",
                        "nickname": "Heat",
                        "urlName": "heat",
                        "confName": "Sacramento",
                        "divName": "",
                    },
                    {
                        "isNBAFranchise": "true",
                        "isAllStar": "false",
                        "city": "Sacramento",
                        "altCityName": "Sacramento",
                        "fullName": "Sacramento Kings",
                        "tricode": "SAC",
                        "teamId": "1610612758",
                        "nickname": "Kings",
                        "urlName": "kings",
                        "confName": "Sacramento",
                        "divName": "",
                    },
                ],
                "vegas": [
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
                        "confName": "summer",
                        "divName": "",
                    }
                ],
                "utah": [
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
                        "confName": "Utah",
                        "divName": "",
                    }
                ],
            },
        }

        mocked = get_teams()
        mocked_keys = mocked.json().keys()

    assert list(actual_keys) == list(mocked_keys)
