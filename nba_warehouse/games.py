from datetime import datetime

import requests

from nba_warehouse.utils import HEADERS

BASE_URL = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00"


def get_games(date):
    url = BASE_URL + f'&gameDate={date.strftime("%m/%d/%Y")}'

    response = requests.get(url, headers=HEADERS)

    if response.ok:
        return response
    else:
        return None


def format_games(date):
    games = get_games(date)
    games = games.json()
    game_header_keys = [header.lower() for header in games['resultSets'][0]['headers']]
    games_to_format = []
    for game in games['resultSets'][0]['rowSet']:
       games_to_format.append(dict(zip(game_header_keys, game)))

    game_detail_keys = [header.lower() for header in games['resultSets'][1]['headers']]
    game_detail_values = games['resultSets'][1]['rowSet']
    games_detail = []
    for game_detail in game_detail_values:
        games_detail.append(dict(zip(game_detail_keys, game_detail)))

    formatted_games = []
    for game in games_to_format:
        game_formatted = {}
        game_formatted['game_id'] = game['game_id']
        game_formatted['game_date_est'] = game['game_date_est']
        game_formatted['season'] = game['season']
        game_formatted['home_team_id'] = game['home_team_id']
        game_formatted['visitor_team_id'] = game['visitor_team_id']

        # After getting all data needed from the basic information go into
        # detail and when we have a match grab what else is needed
        for detail in games_detail:
            if detail['game_id'] == game['game_id']:
                if detail['team_id'] == game['home_team_id']:
                    game_formatted['home_pts'] = detail['pts']
                elif detail['team_id'] == game['visitor_team_id']:
                    game_formatted['visitor_pts'] = detail['pts']
        formatted_games.append(game_formatted)
    for f in formatted_games:
        print(f)
    return formatted_games
    
