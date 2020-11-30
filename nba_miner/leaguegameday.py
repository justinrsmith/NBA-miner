from dataclasses import dataclass
from datetime import datetime

from typing import List

from nba_miner.api import NBAApi


BASE_URL = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00"


@dataclass
class Game:
    id: str
    date: datetime
    season: int
    home_team_id: int
    visitor_team_id: int
    game_status: str
    game_code: str
    arena: str
    home_pts: int = None
    visitor_pts: int = None

    def outcome(self) -> dict:
        if not self.home_pts or not self.visitor_pts:
            return None
        elif self.home_pts > self.visitor_pts:
            return {"winner": self.home_team_id, "loser": self.visitor_team_id}
        elif self.home_pts < self.visitor_pts:
            return {"winner": self.visitor_team_id, "loser": self.home_team_id}


@dataclass
class LeagueGameDayFinder(NBAApi):
    date: datetime
    home_team_id: int = None
    visitor_team_id: int = None
    team_id: int = None
    games: List[Game] = None

    def __post_init__(self):
        super().__init__(BASE_URL + f'&gameDate={self.date.strftime("%m/%d/%Y")}')
        self.get_games()

    def get_games(self) -> None:
        json = self.get().json()

        if json:
            self.games = []  # reset game attribute
            for header_row in json["resultSets"][0][
                "rowSet"
            ]:  # Loop over GameHeader data rows
                # Combine data with their keys
                game_header = dict(zip(json["resultSets"][0]["headers"], header_row))

                # Start setting up game object
                game = Game(
                    id=str(game_header["GAME_ID"]),
                    date=datetime.strptime(
                        game_header["GAME_DATE_EST"], "%Y-%m-%dT%H:%M:%S"
                    ),
                    season=game_header["SEASON"],
                    home_team_id=game_header["HOME_TEAM_ID"],
                    visitor_team_id=game_header["VISITOR_TEAM_ID"],
                    game_status=game_header["GAME_STATUS_TEXT"],
                    game_code=game_header["GAMECODE"],
                    arena=game_header["ARENA_NAME"],
                    # home_fg_pct=game_header[""]
                )

                for line_score_row in json["resultSets"][1][
                    "rowSet"
                ]:  # Loop over LineScore rows
                    # Combine data with their keys
                    game_line = dict(
                        zip(json["resultSets"][1]["headers"], line_score_row)
                    )

                    # If line row matches header row game_id then check if
                    # there is a match for either team on team_id and set that
                    # teams points
                    if game_line["GAME_ID"] == game_header["GAME_ID"]:
                        if game_line["TEAM_ID"] == game_header["HOME_TEAM_ID"]:
                            game.home_pts = game_line["PTS"]
                        elif game_line["TEAM_ID"] == game_header["VISITOR_TEAM_ID"]:
                            game.visitor_pts = game_line["PTS"]

                if self.home_team_id and self.home_team_id == game.home_team_id:
                    self.games.append(game)
                elif (
                    self.visitor_team_id
                    and self.visitor_team_id == game.visitor_team_id
                ):
                    self.games.append(game)
                elif self.team_id and (
                    self.team_id == game.home_team_id
                    or self.team_id == game.visitor_team_id
                ):
                    self.games.append(game)
                elif (
                    not self.home_team_id
                    and not self.visitor_team_id
                    and not self.team_id
                ):
                    self.games.append(game)
