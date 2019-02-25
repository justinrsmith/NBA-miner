from datetime import datetime
from unittest import skipIf
from unittest.mock import MagicMock, Mock, patch

import pytest

from constants import SKIP_REAL
from tests.fixtures import json_games, games
from nba_warehouse.games import Game, ScheduleDay


@pytest.fixture
def mock_json_games():
    return json_games


@pytest.fixture
def mock_games():
    return games


@pytest.fixture
def mock_game():
    return Game(1, datetime(2018, 11, 30), 2018, 24, 35, 128, 121)


class TestScheduleDay(object):
    @classmethod
    def setup_class(self):
        self.mock_requests_patcher = patch("nba_warehouse.api.requests.get")
        self.mock_requests = self.mock_requests_patcher.start()
        self.date = datetime(2018, 11, 30)
        self.schedule_day = ScheduleDay(self.date)

    @classmethod
    def teardown_class(self):
        self.mock_requests_patcher.stop()

    def test_date_attribute_is_expected_value(self):
        """ScheduleDay object data should match value passed in"""
        assert self.date == self.schedule_day.date

    def test_get_json_is_valid(self, mock_json_games):
        """Get games method should return valid json"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        json_games = self.schedule_day.get_json()

        assert json_games == mock_json_games

    def test_get_json_is_valid_and_for_expected_date(self, mock_json_games):
        """Get games method should return valid json for the correct date"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        json_games = self.schedule_day.get_json()

        assert json_games["parameters"]["GameDate"] == self.date.strftime("%m/%d/%Y")

    def test_set_games_attribute_to_list_of_games_for_day(self, mock_json_games):
        """Get games method should return a list containing game objects"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        self.schedule_day.set_games()

        assert type(self.schedule_day.games) == list
        assert type(self.schedule_day.games[0]) == Game
        assert self.schedule_day.games[0].date == self.date

    def test_set_games_sets_correct_amount_of_games(self, mock_json_games, mock_games):
        """Set games should set the proper amount of Game objects"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        self.schedule_day.set_games()
        assert len(self.schedule_day.games) == len(mock_games)

    def test_get_games_returns_expected_data(self, mock_json_games, mock_games):
        """Should return a valid list of Game objects"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        self.schedule_day.set_games()
        assert self.schedule_day.games[0] in mock_games
        assert self.schedule_day.games[1] in mock_games

    def test_get_games_not_return_expected_data(self, mock_json_games, mock_games):
        """Should return a valid list of Game objects"""
        self.mock_requests.return_value = Mock(ok=True)
        self.mock_requests.return_value.json.return_value = mock_json_games

        self.schedule_day.set_games()
        assert (
            Game("0444440", datetime(2018, 11, 30), 2018, 26, 36, 105, 104)
            not in self.schedule_day.games
        )


class TestGame(object):
    @classmethod
    def setup_class(self):
        self.id = 1
        self.date = datetime(2018, 11, 30)
        self.season = 2018
        self.home_team_id = 24
        self.visitor_team_id = 35
        self.home_pts = 128
        self.visitor_pts = 121

    def test_game_attributes_are_expected_values(self, mock_game):
        """Game attributes should be expected values"""
        assert mock_game.id == self.id
        assert mock_game.date == self.date
        assert mock_game.season == self.season
        assert mock_game.home_team_id == self.home_team_id
        assert mock_game.visitor_team_id == self.visitor_team_id
        assert mock_game.home_pts == self.home_pts
        assert mock_game.visitor_pts == self.visitor_pts

    def test_game_score_defaults_to_none(self):
        """Game home and away score should default to None if not provided"""
        game = Game(
            self.id, self.date, self.season, self.home_team_id, self.visitor_team_id
        )
        assert game.home_pts is None

    def test_get_winner_is_home_team(self, mock_game):
        """Game winner method should return team id of winner"""
        assert mock_game.winner() == self.home_team_id

    def test_get_winner_is_visiting_team(self, mock_game):
        """Game winner method should return team id of winner"""
        mock_game.visitor_pts = 131
        assert mock_game.winner() == self.visitor_team_id

    def test_get_winner_is_none_when_no_score(self, mock_game):
        """Game winner method should return None if no score exists yet"""
        mock_game.home_pts = None
        mock_game.visitor_pts = None
        assert mock_game.winner() is None

    def test_get_loser_is_home_team(self, mock_game):
        """Game loser method should return team id of game loser"""
        mock_game.visitor_pts = 131
        assert mock_game.loser() == self.home_team_id

    def test_get_loser_is_visiting_team(self, mock_game):
        """Game loser method should return team id of game loser"""
        assert mock_game.loser() == self.visitor_team_id

    def test_get_loser_is_none_when_no_score(self, mock_game):
        """Game loser method should return None if no score exists yet"""
        mock_game.home_pts = None
        mock_game.visitor_pts = None
        assert mock_game.loser() is None

    def test_games_with_different_id_not_equal(self, mock_game):
        """Games with different id should not be equal"""
        game = Game(
            444,
            self.date,
            self.season,
            self.home_team_id,
            self.visitor_team_id,
            110,
            105,
        )
        assert mock_game != game


@skipIf(SKIP_REAL, "Skipping tests that hit the real API server")
def test_integeration_contract(mock_json_games):
    # Call the service to hit actual API
    schedule_day = ScheduleDay(datetime(2018, 11, 30))
    actual_keys = schedule_day.get().json().keys()

    # Call the service to hit the mocked API
    with patch("nba_warehouse.api.requests.get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = mock_json_games

        mocked = ScheduleDay(datetime(2018, 11, 30))
        mocked_keys = mocked.get().json().keys()

    assert list(actual_keys) == list(mocked_keys)
