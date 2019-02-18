import requests

BASE_URL = "https://data.nba.net/prod/v2/2018/teams.json"


def get_teams():
    response = requests.get(BASE_URL)
    if response.ok:
        return response
    else:
        return None


def get_nba_teams():
    teams = get_teams().json()

    nba_teams = []
    for team in teams["league"]["standard"]:
        if team["isNBAFranchise"] == "true":
            nba_teams.append(team)
    return nba_teams
