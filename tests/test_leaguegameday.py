from datetime import datetime
import json
from unittest import skipIf
from unittest.mock import Mock, patch

import pytest

from constants import SKIP_REAL
from nba_miner.api import NBAApi
from nba_miner.leaguegameday import BASE_URL, Game, LeagueGameDayFinder


@pytest.fixture
def mock_json_games():
    path = "tests/fixtures/scoreboard.json"
    with open(path) as f:
        data = json.load(f)
    return data


@pytest.fixture
def mock_game():
    return Game(
        id=1,
        date=datetime(2018, 11, 30),
        season=2018,
        home_team_id=24,
        visitor_team_id=35,
        home_pts=128,
        visitor_pts=121,
        game_status="Final",
        game_code="20181130/CLEBOS",
        arena="TD Garden",
    )


class TestLeagueGameDayFinder(object):
    @classmethod
    def setup_class(self):
        self.mock_requests_patcher = patch("nba_miner.api.requests.get")
        self.mock_requests = self.mock_requests_patcher.start()
        self.date = datetime(2018, 11, 30)
        self.schedule_day = LeagueGameDayFinder(self.date)

    @classmethod
    def teardown_class(self):
        self.mock_requests_patcher.stop()

    def test_date_attribute_is_expected_value(self):
        """LeagueGameDayFinder object data should match value passed in"""
        assert self.date == self.schedule_day.date

    def test_get_json_is_valid(self, mock_json_games):
        """Games attribute should contain list of game objects when there is
        a response from the api"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        gameday = LeagueGameDayFinder(self.date)

        assert type(gameday.games[0]) == Game

    def test_get_outcome_is_dict(self, mock_game):
        """Outcome should be a dict if not None"""
        assert type(mock_game.outcome()) is dict

    def test_get_outcome_winner_is_expected(self, mock_game):
        """Home team scored more so winner should be home team"""
        assert mock_game.outcome()["winner"] == mock_game.home_team_id

    def test_get_outcome_loser_is_expected(self, mock_game):
        """Home team scored less so loser should be home team"""
        mock_game.home_pts = 119
        assert mock_game.outcome()["loser"] == mock_game.home_team_id

    def test_get_outcome_is_none(self, mock_game):
        """If no points yet then outcome should return None"""
        mock_game.home_pts = None
        mock_game.visitor_pts = None
        assert mock_game.outcome() is None

    def test_games_returned_is_expected_date(self, mock_json_games):
        """Get games method should Game objects for provided date"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        gameday = LeagueGameDayFinder(date=self.date)

        assert any(game.date == self.date for game in gameday.games)

    def test_when_home_team_id_param_return_only_home_team_game(self, mock_json_games):
        """When home_team_id param is provided games list should only contain
        that teams home games"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games
        gameday = LeagueGameDayFinder(date=self.date, home_team_id=1610612738)

        assert any(game.home_team_id == 1610612738 for game in gameday.games)

    def test_when_visitor_team_id_param_return_only_visitor_team_game(
        self, mock_json_games
    ):
        """When visitor_team_id param is provided games list should only contain
        that teams away games"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games
        gameday = LeagueGameDayFinder(date=self.date, visitor_team_id=1610612739)

        assert any(game.visitor_team_id == 1610612739 for game in gameday.games)

    def test_when_home_and_visitor_team_id_proper_game_returned(self, mock_json_games):
        """Should return only one Game object in games list matching the
        provided home_team_id and visitor_team_id"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games
        gameday = LeagueGameDayFinder(
            date=self.date, home_team_id=1610612766, visitor_team_id=1610612762
        )

        assert len(gameday.games) == 1
        assert gameday.games[0].home_team_id == 1610612766
        assert gameday.games[0].visitor_team_id == 1610612762

    def test_team_id_filters_games_for_home_or_visitor(self, mock_json_games):
        """When providing team_id it should filter games to be only for thee
        team_id provided regardless of home or visitor"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        gameday = LeagueGameDayFinder(date=self.date, team_id=1610612738)

        assert len(gameday.games) > 0
        assert gameday.games[0].home_team_id == 1610612738

        gameday = LeagueGameDayFinder(date=self.date, team_id=1610612741)

        assert len(gameday.games) > 0
        assert gameday.games[0].visitor_team_id == 1610612741


@skipIf(SKIP_REAL, "Skipping tests that hit the real API server")
def test_integeration_contract(mock_json_games):
    # Call the service to hit actual API
    url = BASE_URL + "&gamedate=11/30/2018"
    json = NBAApi(url).get().json()
    actual_keys = json.keys()

    # Call the service to hit the mocked API
    with patch("nba_miner.api.requests.get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = mock_json_games

        mocked_json = NBAApi(url).get().json()
        mocked_keys = mocked_json.keys()

    assert list(actual_keys) == list(mocked_keys)
