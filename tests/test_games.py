from datetime import datetime
from unittest import skipIf
from unittest.mock import Mock, patch

import pytest

from constants import SKIP_REAL
from nba_warehouse.games import get_games, format_games
from nba_warehouse.teams import get_teams


@pytest.fixture
def games():
    return {
        "resource": "scoreboardV2",
        "parameters": {"GameDate": "11/30/2018", "LeagueID": "00", "DayOffset": "0"},
        "resultSets": [
            {
                "name": "GameHeader",
                "headers": [
                    "GAME_DATE_EST",
                    "GAME_SEQUENCE",
                    "GAME_ID",
                    "GAME_STATUS_ID",
                    "GAME_STATUS_TEXT",
                    "GAMECODE",
                    "HOME_TEAM_ID",
                    "VISITOR_TEAM_ID",
                    "SEASON",
                    "LIVE_PERIOD",
                    "LIVE_PC_TIME",
                    "NATL_TV_BROADCASTER_ABBREVIATION",
                    "HOME_TV_BROADCASTER_ABBREVIATION",
                    "AWAY_TV_BROADCASTER_ABBREVIATION",
                    "LIVE_PERIOD_TIME_BCAST",
                    "ARENA_NAME",
                    "WH_STATUS",
                ],
                "rowSet": [
                    [
                        "2018-11-30T00:00:00",
                        1,
                        "0021800319",
                        3,
                        "Final",
                        "20181130/CLEBOS",
                        1610612738,
                        1610612739,
                        "2018",
                        4,
                        "     ",
                        "",
                        "NBCSB",
                        "FSO",
                        "Q4       - ",
                        "TD Garden",
                        1,
                    ],
                    [
                        "2018-11-30T00:00:00",
                        2,
                        "0021800320",
                        3,
                        "Final",
                        "20181130/UTACHA",
                        1610612766,
                        1610612762,
                        "2018",
                        4,
                        "     ",
                        "",
                        "FSSE-CHA",
                        "ATTSN-RM",
                        "Q4       - ",
                        "Spectrum Center",
                        1,
                    ],
                ],
            },
            {
                "name": "LineScore",
                "headers": [
                    "GAME_DATE_EST",
                    "GAME_SEQUENCE",
                    "GAME_ID",
                    "TEAM_ID",
                    "TEAM_ABBREVIATION",
                    "TEAM_CITY_NAME",
                    "TEAM_NAME",
                    "TEAM_WINS_LOSSES",
                    "PTS_QTR1",
                    "PTS_QTR2",
                    "PTS_QTR3",
                    "PTS_QTR4",
                    "PTS_OT1",
                    "PTS_OT2",
                    "PTS_OT3",
                    "PTS_OT4",
                    "PTS_OT5",
                    "PTS_OT6",
                    "PTS_OT7",
                    "PTS_OT8",
                    "PTS_OT9",
                    "PTS_OT10",
                    "PTS",
                    "FG_PCT",
                    "FT_PCT",
                    "FG3_PCT",
                    "AST",
                    "REB",
                    "TOV",
                ],
                "rowSet": [
                    [
                        "2018-11-30T00:00:00",
                        1,
                        "0021800319",
                        1610612739,
                        "CLE",
                        "Cleveland",
                        "Cavaliers",
                        "4-17",
                        26,
                        26,
                        20,
                        23,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        95,
                        0.39,
                        0.8,
                        0.318,
                        18,
                        36,
                        13,
                    ],
                    [
                        "2018-11-30T00:00:00",
                        1,
                        "0021800319",
                        1610612738,
                        "BOS",
                        "Boston",
                        "Celtics",
                        "12-10",
                        30,
                        32,
                        39,
                        27,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        128,
                        0.533,
                        0.813,
                        0.548,
                        30,
                        47,
                        10,
                    ],
                ],
            },
            {
                "name": "SeriesStandings",
                "headers": [
                    "GAME_ID",
                    "HOME_TEAM_ID",
                    "VISITOR_TEAM_ID",
                    "GAME_DATE_EST",
                    "HOME_TEAM_WINS",
                    "HOME_TEAM_LOSSES",
                    "SERIES_LEADER",
                ],
                "rowSet": [
                    [
                        "0021800319",
                        1610612738,
                        1610612739,
                        "2018-11-30T00:00:00",
                        3,
                        0,
                        "Boston",
                    ],
                    [
                        "0021800320",
                        1610612766,
                        1610612762,
                        "2018-11-30T00:00:00",
                        0,
                        1,
                        "Utah",
                    ],
                ],
            },
            {
                "name": "LastMeeting",
                "headers": [
                    "GAME_ID",
                    "LAST_GAME_ID",
                    "LAST_GAME_DATE_EST",
                    "LAST_GAME_HOME_TEAM_ID",
                    "LAST_GAME_HOME_TEAM_CITY",
                    "LAST_GAME_HOME_TEAM_NAME",
                    "LAST_GAME_HOME_TEAM_ABBREVIATION",
                    "LAST_GAME_HOME_TEAM_POINTS",
                    "LAST_GAME_VISITOR_TEAM_ID",
                    "LAST_GAME_VISITOR_TEAM_CITY",
                    "LAST_GAME_VISITOR_TEAM_NAME",
                    "LAST_GAME_VISITOR_TEAM_CITY1",
                    "LAST_GAME_VISITOR_TEAM_POINTS",
                ],
                "rowSet": [
                    [
                        "0021800319",
                        "0011800040",
                        "2018-10-06T00:00:00",
                        1610612738,
                        "Boston",
                        "Celtics",
                        "BOS",
                        102,
                        1610612739,
                        "Cleveland",
                        "Cavaliers",
                        "CLE",
                        113,
                    ],
                    [
                        "0021800320",
                        "0021700824",
                        "2018-02-09T00:00:00",
                        1610612766,
                        "Charlotte",
                        "Hornets",
                        "CHA",
                        94,
                        1610612762,
                        "Utah",
                        "Jazz",
                        "UTA",
                        106,
                    ],
                ],
            },
            {
                "name": "EastConfStandingsByDay",
                "headers": [
                    "TEAM_ID",
                    "LEAGUE_ID",
                    "SEASON_ID",
                    "STANDINGSDATE",
                    "CONFERENCE",
                    "TEAM",
                    "G",
                    "W",
                    "L",
                    "W_PCT",
                    "HOME_RECORD",
                    "ROAD_RECORD",
                ],
                "rowSet": [
                    [
                        1610612761,
                        "00",
                        "22018",
                        "11/30/2018",
                        "East",
                        "Toronto",
                        23,
                        19,
                        4,
                        0.826,
                        "10-2",
                        "9-2",
                    ],
                    [
                        1610612749,
                        "00",
                        "22018",
                        "11/30/2018",
                        "East",
                        "Milwaukee",
                        21,
                        15,
                        6,
                        0.714,
                        "11-2",
                        "4-4",
                    ],
                ],
            },
            {
                "name": "WestConfStandingsByDay",
                "headers": [
                    "TEAM_ID",
                    "LEAGUE_ID",
                    "SEASON_ID",
                    "STANDINGSDATE",
                    "CONFERENCE",
                    "TEAM",
                    "G",
                    "W",
                    "L",
                    "W_PCT",
                    "HOME_RECORD",
                    "ROAD_RECORD",
                ],
                "rowSet": [
                    [
                        1610612746,
                        "00",
                        "22018",
                        "11/30/2018",
                        "West",
                        "LA Clippers",
                        21,
                        15,
                        6,
                        0.714,
                        "9-1",
                        "6-5",
                    ],
                    [
                        1610612743,
                        "00",
                        "22018",
                        "11/30/2018",
                        "West",
                        "Denver",
                        22,
                        15,
                        7,
                        0.682,
                        "9-3",
                        "6-4",
                    ],
                ],
            },
            {
                "name": "Available",
                "headers": ["GAME_ID", "PT_AVAILABLE"],
                "rowSet": [["0021800328", 1], ["0021800326", 1]],
            },
            {
                "name": "TeamLeaders",
                "headers": [
                    "GAME_ID",
                    "TEAM_ID",
                    "TEAM_CITY",
                    "TEAM_NICKNAME",
                    "TEAM_ABBREVIATION",
                    "PTS_PLAYER_ID",
                    "PTS_PLAYER_NAME",
                    "PTS",
                    "REB_PLAYER_ID",
                    "REB_PLAYER_NAME",
                    "REB",
                    "AST_PLAYER_ID",
                    "AST_PLAYER_NAME",
                    "AST",
                ],
                "rowSet": [
                    [
                        "0021800319",
                        1610612738,
                        "Boston",
                        "Celtics",
                        "BOS",
                        202681,
                        "Kyrie Irving",
                        29,
                        203382,
                        "Aron Baynes",
                        9,
                        203935,
                        "Marcus Smart",
                        7,
                    ],
                    [
                        "0021800319",
                        1610612739,
                        "Cleveland",
                        "Cavaliers",
                        "CLE",
                        203903,
                        "Jordan Clarkson",
                        16,
                        202684,
                        "Tristan Thompson",
                        12,
                        202684,
                        "Tristan Thompson",
                        4,
                    ],
                ],
            },
            {
                "name": "TicketLinks",
                "headers": ["GAME_ID", "LEAG_TIX"],
                "rowSet": [
                    [
                        "0021800319",
                        "https://ticketmaster.com/event/0100550ADB09D7C3?brand=nba&extcmp=gw513142&wt.mc_id=NBA_LEAGUE_BOS_SINGLE_GAME_LINK&utm_source=NBA.com&utm_medium=client&utm_campaign=NBA_LEAGUE_BOS&utm_content=SINGLE_GAME_LINK",
                    ],
                    [
                        "0021800329",
                        "https://www.ticketmaster.com/portland-trail-blazers-vs-denver-nuggets-portland-oregon-11-30-2018/event/0F005515A8904734?brand=nba&extcmp=gw513160&wt.mc_id=NBA_LEAGUE_POR_SINGLE_GAME_LINK&utm_source=NBA.com&utm_medium=client&utm_campaign=NBA_LEAGUE_POR&utm",
                    ],
                ],
            },
            {"name": "WinProbability", "headers": [], "rowSet": []},
        ],
    }


class TestGetGames(object):
    @classmethod
    def setup_class(self):
        self.mock_get_patcher = patch("nba_warehouse.games.requests.get")
        self.mock_get = self.mock_get_patcher.start()
        self.date = datetime(2018, 11, 30)

    @classmethod
    def teardown_class(self):
        self.mock_get_patcher.stop()

    def test_request_response_is_ok(self, games):
        self.mock_get.return_value = Mock(ok=True)
        self.mock_get.return_value.json.return_value = games

        response = get_games(self.date)

        assert response.ok is True
        assert response.json() == games

    def test_request_response_is_not_ok(self):
        self.mock_get.return_value = Mock(ok=False)

        response = get_games(self.date)

        assert response is None

    def test_games_are_for_provided_date(self, games):
        self.mock_get.return_value = Mock(ok=True)
        self.mock_get.return_value.json.return_value = games

        response = get_games(self.date)

        assert response.json()["parameters"]["GameDate"] == self.date.strftime(
            "%m/%d/%Y"
        )


class TestFormatGames(object):
    @classmethod
    def setup_class(self):
        self.mock_get_games_patcher = patch("nba_warehouse.games.get_games")
        self.mock_get_games = self.mock_get_games_patcher.start()
        self.date = datetime(2018, 11, 30)

    @classmethod
    def teardown_class(self):
        self.mock_get_games_patcher.stop()

    def test_games_formatted_as_expected(self, games):
        self.mock_get_games.return_value = Mock()
        self.mock_get_games.return_value.json.return_value = games
        formatted_games = format_games(self.date)

        expected_keys = [
            "game_id",
            "game_date_est",
            "season",
            "home_team_id",
            "visitor_team_id",
            "visitor_pts",
            "home_pts",
        ]

        assert self.mock_get_games.called == True
        assert type(formatted_games) == list
        assert list(formatted_games[0].keys()) == expected_keys

    def test_same_number_games_formatted_as_from_api(self, games):
        self.mock_get_games.return_value = Mock()
        self.mock_get_games.return_value.json.return_value = games
        with patch("nba_warehouse.games.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = games
            response = get_games(self.date)
        formatted_games = format_games(self.date)

        assert self.mock_get_games.called == True
        assert len(response.json()["resultSets"][0]["rowSet"]) == len(formatted_games)


@skipIf(SKIP_REAL, "Skipping tests that hit the real API server")
def test_integeration_contract(games):
    # Call the service to hit actual API
    response = get_games(datetime(2018, 11, 30))
    actual_keys = response.json().keys()

    # Call the esrvice to hit the mocked API
    with patch("nba_warehouse.games.requests.get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = games

        mocked = get_games(datetime(2018, 11, 30))
        mocked_keys = mocked.json().keys()

    assert list(actual_keys) == list(mocked_keys)
