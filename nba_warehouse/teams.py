from nba_warehouse.api import NBAApi

BASE_URL = "https://data.nba.net/prod/v2/2018/teams.json"


def get_teams():
    nba_api = NBAApi(BASE_URL)
    return nba_api.get()


def get_nba_teams(teams):
    nba_teams = []
    for team in teams["league"]["standard"]:
        if team["isNBAFranchise"] == "true":
            nba_teams.append(team)
    return nba_teams
