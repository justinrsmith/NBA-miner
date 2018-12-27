import json

import requests

from nba_warehouse.db.models import session, Team
from utils import camelcase_to_underscore

BASE_URL = 'https://data.nba.net/prod/v2/2018/teams.json'

r = requests.get(BASE_URL)

teams = json.loads(r.content)

nba_teams = []
for team in teams['league']['standard']:
    nba_team = {}
    for k, v in team.items():
        nba_team[camelcase_to_underscore(k)] = v
    nba_teams.append(nba_team)

for team in nba_teams:
    print(team)
    # team = Team(**team)
    # session.add(team)
    # session.commit()
