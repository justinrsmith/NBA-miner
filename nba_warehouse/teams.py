from collections import namedtuple

from nba_warehouse.api import NBAApi

Team = namedtuple('Team', ['is_nba_franchise', 'is_all_star', 'city',
'alt_city_name', 'full_name', 'tricode', 'team_id', 'nickname',
'url_name', 'conf_name', 'div_name'])

def get_teams():
    api = NBAApi('https://data.nba.net/prod/v2/2018/teams.json')
    response = api.get()
    if response:
        teams_json = response.json()

    teams = []
    for team_j in teams_json['league']['standard']:
        team = Team(
            is_nba_franchise=team_j['isNBAFranchise'],
            is_all_star=team_j['isAllStar'],
            city=team_j['city'],
            alt_city_name=team_j['altCityName'],
            full_name=team_j['fullName'],
            tricode=team_j['tricode'],
            team_id=team_j['teamId'],
            nickname=team_j['nickname'],
            url_name=team_j['urlName'],
            conf_name=team_j['confName'],
            div_name=team_j['divName']
        )
        teams.append(team)
    return teams