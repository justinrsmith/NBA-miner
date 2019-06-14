from dataclasses import dataclass
from datetime import datetime

from typing import List

from nba_warehouse.api import NBAApi


BASE_URL = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00"


@dataclass
class Game:
    id: str
    date: datetime
    season: int
    home_team_id: int
    visitor_team_id: int
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
class ScheduleDay(NBAApi):
    date: datetime
    games: List[Game] = None

    def __post_init__(self):
        super().__init__(BASE_URL + f'&gameDate={self.date.strftime("%m/%d/%Y")}')

    def get_json(self) -> dict:
        request = self.get()
        return request.json()

    def set_games(self) -> None:
        json = self.get_json()

        if json:
            self.games = []  # reset game attribute
            for header_row in json["resultSets"][0][
                "rowSet"
            ]:  # Loop over GameHeader data rows
                # Combine data with their keys
                game_header = dict(zip(json["resultSets"][0]["headers"], header_row))
                # Start setting up game object
                game = Game(
                    str(game_header["GAME_ID"]),
                    datetime.strptime(
                        game_header["GAME_DATE_EST"], "%Y-%m-%dT%H:%M:%S"
                    ),
                    int(game_header["SEASON"]),
                    game_header["HOME_TEAM_ID"],
                    game_header["VISITOR_TEAM_ID"],
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
                self.games.append(game)
