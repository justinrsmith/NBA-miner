from unittest import skipIf
from unittest.mock import Mock, patch

import pytest

from constants import SKIP_REAL
from nba_warehouse.teams import Teams


@pytest.fixture
def mock_teams():
    return {
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


class TestAllTeams(object):
    @classmethod
    def setup_class(self):
        self.mock_get_patcher = patch("nba_warehouse.api.requests.get")
        self.mock_get = self.mock_get_patcher.start()

    @classmethod
    def teardown_class(self):
        self.mock_get_patcher.stop()

    def test_request_response_is_ok(self, mock_teams):
        self.mock_get.return_value = Mock(ok=True)
        self.mock_get.return_value.json.return_value = mock_teams

        teams = Teams()

        assert teams.get().ok is True
        assert teams.get().json() == mock_teams

    def test_request_response_is_not_ok(self):
        self.mock_get.return_value = Mock(ok=False)

        teams = Teams()

        assert teams.get() is None


class TestNBATeams(object):
    @classmethod
    def setup_class(self):
        self.mock_get_teams_patcher = patch("nba_warehouse.api.requests.get")
        self.mock_get_teams = self.mock_get_teams_patcher.start()

    @classmethod
    def teardown_class(self):
        self.mock_get_teams_patcher.stop()

    def test_getting_only_nba_teams(self, mock_teams):
        self.mock_get_teams.return_value = Mock()
        self.mock_get_teams.return_value.json.return_value = mock_teams
        teams = Teams()
        nba_teams = teams.nba_only()

        assert nba_teams == [
            mock_teams["league"]["standard"][1],
            mock_teams["league"]["standard"][2],
        ]


@skipIf(SKIP_REAL, "Skipping tests that hit the real API server")
def test_integeration_contract(mock_teams):
    # Call the service to hit actual API
    teams = Teams()
    actual_keys = teams.get().json().keys()

    # Call the esrvice to hit the mocked API
    with patch("nba_warehouse.api.requests.get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = mock_teams

        mocked = Teams()
        mocked_keys = mocked.get().json().keys()

    assert list(actual_keys) == list(mocked_keys)
