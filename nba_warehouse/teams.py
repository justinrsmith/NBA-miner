from nba_warehouse.api import NBAApi


class Teams(NBAApi):
    def __init__(self):
        super().__init__("https://data.nba.net/prod/v2/2018/teams.json")

    def nba_only(self):
        r = self.get()
        teams = r.json()
        nba_teams = []
        for team in teams["league"]["standard"]:
            if team["isNBAFranchise"] == "true":
                nba_teams.append(team)
        return nba_teams
