from datetime import datetime

from nba_warehouse.api import NBAApi
from nba_warehouse.utils import HEADERS

BASE_URL = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00"


class Games(NBAApi):
	def __init__(self, date, url=None):
		self.url = BASE_URL + f'&gameDate={date.strftime("%m/%d/%Y")}'
		self.date = date
		#self.data = NBAApi(self.url) # this is a problem most likely
	
	def formatted(self):
		games = self.response.json()
		game_header_keys = [header.lower() for header in games["resultSets"][0]["headers"]]
		games_to_format = []
		for game in games["resultSets"][0]["rowSet"]:
			games_to_format.append(dict(zip(game_header_keys, game)))
	
			game_detail_keys = [header.lower() for header in games["resultSets"][1]["headers"]]
			game_detail_values = games["resultSets"][1]["rowSet"]
			games_detail = []
			for game_detail in game_detail_values:
				games_detail.append(dict(zip(game_detail_keys, game_detail)))
	
				formatted_games = []
				for game in games_to_format:
					game_formatted = {}
					game_formatted["game_id"] = game["game_id"]
					game_formatted["game_date_est"] = game["game_date_est"]
					game_formatted["season"] = game["season"]
					game_formatted["home_team_id"] = game["home_team_id"]
					game_formatted["visitor_team_id"] = game["visitor_team_id"]
					
					# After getting all data needed from the basic information go into
					# detail and when we have a match grab what else is needed
					for detail in games_detail:
						if detail["game_id"] == game["game_id"]:
							if detail["team_id"] == game["home_team_id"]:
								game_formatted["home_pts"] = detail["pts"]
							elif detail["team_id"] == game["visitor_team_id"]:
								game_formatted["visitor_pts"] = detail["pts"]
					formatted_games.append(game_formatted)

		return formatted_games
