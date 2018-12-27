from datetime import datetime, timedelta
import json
import time

import requests
from sqlalchemy import exc

from nba_warehouse.db.models import session, Game, Team
from utils import camelcase_to_underscore, HEADERS

BASE_URL = 'https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00'

# Get number of days between start and end of season
season_start_date = datetime(2016, 10, 25)
season_end_date = datetime(2017, 4, 12)
delta = season_end_date - season_start_date

# Loop over each day of the season and wait 20 seconds
for i in range(delta.days + 1):
    date = season_start_date + timedelta(i)
    date_string = date.strftime('%m/%d/%Y')
    print(date_string)

    r = requests.get(BASE_URL + f'&gameDate={date_string}', headers=HEADERS)
    games = json.loads(r.content)

    # Get basic game information into a list of dictionaries
    game_basic_headers = games['resultSets'][0]['headers']
    game_basic_headers = [header.lower() for header in game_basic_headers]
    game_basic_values = games['resultSets'][0]['rowSet']
    games_basic = []
    for basic in game_basic_values:
        game_basic = dict(zip(game_basic_headers, basic))
        games_basic.append(game_basic)

    # Get detailed game information into a list of dictionaries
    game_detail_headers = games['resultSets'][1]['headers']
    game_detail_headers = [header.lower() for header in game_detail_headers]
    game_detail_values = games['resultSets'][1]['rowSet']
    games_detail = []
    for detail in game_detail_values:
        game_detail = dict(zip(game_detail_headers, detail))
        games_detail.append(game_detail)

    # Setup data from api that needs to be inserted into database
    games = []
    for basic in games_basic:
        game = {}
        game['game_id'] = basic['game_id']
        game['game_date_est'] = basic['game_date_est']
        game['season'] = basic['season']
        game['home_team_id'] = basic['home_team_id']
        game['visitor_team_id'] = basic['visitor_team_id']

        # After getting all data needed from the basic information go into
        # detail and when we have a match grab what else is needed
        for detail in games_detail:
            if detail['game_id'] == basic['game_id']:
                if detail['team_id'] == basic['home_team_id']:
                    game['home_pts'] = detail['pts']
                elif detail['team_id'] == basic['visitor_team_id']:
                    game['visitor_pts'] = detail['pts']
        games.append(game)

    # Insert
    for game in games:
        try:
            game_to_add = Game(**game)
            session.add(game_to_add)
            session.commit()
        except exc.IntegrityError:
            print('integrity error', game)
            session.rollback()

    time.sleep(20)
