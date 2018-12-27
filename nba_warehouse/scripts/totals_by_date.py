from datetime import datetime, timedelta
import json
import time

import requests

from nba_warehouse.db.models import (
    session, TotalsDate, OpponentTotalsDate, TotalsDateTrending,
    OpponentTotalsDateTrending
)
from utils import HEADERS

season = '2016-17'
# trending_days = None
trending_days = 30

BASE_URL = f'https://stats.nba.com/stats/leaguedashteamstats?Conference=&Division=&Season={season}&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='

# Get number of days between start and end of season
season_start_date = datetime(2016, 10, 25)
season_end_date = datetime(2017, 4, 12)
delta = season_end_date - season_start_date


def prepare_totals(totals_in):
    team_totals_headers = totals_in['resultSets'][0]['headers']
    team_totals_headers = [header.lower() for header in team_totals_headers]
    team_totals_values = totals_in['resultSets'][0]['rowSet']

    totals = []
    for team_total in team_totals_values:
        team_total_with_headers = dict(zip(team_totals_headers, team_total))
        team_total_with_headers['date'] = date_to_string
        totals.append(team_total_with_headers)

    return totals

# Loop over each day of the season and wait 20 seconds
for i in range(delta.days + 1):
    date_to = season_start_date + timedelta(i)
    date_to_string = date_to.strftime('%m/%d/%Y')
    if not trending_days:
        date_from_string = season_start_date.strftime('%m/%d/%Y')
    else:
        date_from = date_to - timedelta(days=30)
        date_from_string = date_from.strftime('%m/%d/%Y')
    # print(date_from_string)
    # print(date_to_string)
    # print('*************')

    url = BASE_URL + f'&DateFrom={date_from_string}&DateTo={date_to_string}&MeasureType=Base'
    print(date_to_string, 'team')
    r = requests.get(url, headers=HEADERS)
    team_totals = json.loads(r.content)

    team_totals_insert = prepare_totals(team_totals)

    for team_total in team_totals_insert:
        if not trending_days:
            totals = TotalsDate(**team_total)
        else:
            totals = TotalsDateTrending(**team_total)
        session.add(totals)
        session.commit()

    time.sleep(20)

    url = BASE_URL + f'&DateFrom={date_from_string}&DateTo={date_to_string}&MeasureType=Opponent'
    print(date_to_string, 'opponent')
    r = requests.get(url, headers=HEADERS)
    team_totals = json.loads(r.content)

    team_totals_insert = prepare_totals(team_totals)

    for team_total in team_totals_insert:
        if not trending_days:
            totals = OpponentTotalsDate(**team_total)
        else:
            totals = OpponentTotalsDateTrending(**team_total)
        session.add(totals)
        session.commit()

    time.sleep(20)
