from datetime import datetime

from nba_warehouse.api import NBAApi


BASE_URL = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00"


class ScheduleDay(NBAApi):
    def __init__(self, date):
        self.date = date
        super().__init__(BASE_URL + f'&gameDate={date.strftime("%m/%d/%Y")}')

    def get_json(self):
        request = self.get()
        return request.json()

    def get_games(self):
        json = self.get_json()

        game_header_keys = [
            header.lower() for header in json["resultSets"][0]["headers"]
        ]
        games_from_json = []
        for game in json["resultSets"][0]["rowSet"]:
            games_from_json.append(dict(zip(game_header_keys, game)))

            game_detail_keys = [
                header.lower() for header in json["resultSets"][1]["headers"]
            ]
            game_detail_values = json["resultSets"][1]["rowSet"]
            games_detail = []
            for game_detail in game_detail_values:
                games_detail.append(dict(zip(game_detail_keys, game_detail)))

                games = []
                for json_game in games_from_json:
                    game = Game(
                        json_game["game_id"],
                        json_game["game_date_est"],
                        json_game["season"],
                        json_game["home_team_id"],
                        json_game["visitor_team_id"],
                    )

                    for detail in games_detail:
                        if detail["game_id"] == json_game["game_id"]:
                            if detail["team_id"] == json_game["home_team_id"]:
                                game.home_pts = detail["pts"]
                            elif detail["team_id"] == json_game["visitor_team_id"]:
                                game.visitor_pts = detail["pts"]
                games.append(game)
        return games


class Game(object):
    def __init__(
        self,
        id,
        date,
        season,
        home_team_id,
        visitor_team_id,
        home_pts=None,
        visitor_pts=None,
    ):
        self.id = id
        self.date = date
        self.season = season
        self.home_team_id = home_team_id
        self.visitor_team_id = visitor_team_id
        self.home_pts = home_pts
        self.visitor_pts = visitor_pts

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def winner(self):
        if not self.home_pts or not self.visitor_pts:
            return None
        elif self.home_pts > self.visitor_pts:
            return self.home_team_id
        elif self.home_pts < self.visitor_pts:
            return self.visitor_team_id

    def loser(self):
        if not self.home_pts or not self.visitor_pts:
            return None
        elif self.home_pts > self.visitor_pts:
            return self.visitor_team_id
        elif self.home_pts < self.visitor_pts:
            return self.home_team_id
