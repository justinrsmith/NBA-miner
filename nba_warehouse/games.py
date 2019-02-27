from dataclasses import dataclass, field
from datetime import datetime

from nba_warehouse.api import NBAApi


BASE_URL = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00"


@dataclass
class ScheduleDay(NBAApi):
    date: datetime
    games: list = field(default_factory=list)

    def __post_init__(self):
        super().__init__(BASE_URL + f'&gameDate={self.date.strftime("%m/%d/%Y")}')

    def get_json(self) -> dict:
        request = self.get()
        return request.json()

    def set_games(self) -> None:
        json = self.get_json()

        if json:
            self.games = []
            # Get the data keys for GameHeader
            game_header_keys = [
                header.lower() for header in json["resultSets"][0]["headers"]
            ]
            game_line_score_keys = [
                header.lower() for header in json["resultSets"][1]["headers"]
            ]

            header_rows = []  # Store GameHeader data as dicts
            for header_row in json["resultSets"][0][
                "rowSet"
            ]:  # Loop GameHeader data rows
                keyed_row = dict(zip(game_header_keys, header_row))
                game = Game(
                    str(keyed_row["game_id"]),
                    datetime.strptime(keyed_row["game_date_est"], "%Y-%m-%dT%H:%M:%S"),
                    int(keyed_row["season"]),
                    keyed_row["home_team_id"],
                    keyed_row["visitor_team_id"],
                )

                for line_row in json["resultSets"][1]["rowSet"]:
                    keyed_line_row = dict(zip(game_line_score_keys, line_row))

                    if keyed_line_row["game_id"] == keyed_row["game_id"]:
                        if keyed_line_row["team_id"] == keyed_row["home_team_id"]:
                            game.home_pts = keyed_line_row["pts"]
                        elif keyed_line_row["team_id"] == keyed_row["visitor_team_id"]:
                            game.visitor_pts = keyed_line_row["pts"]
                print(game, "game")
                self.games.append(game)


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
