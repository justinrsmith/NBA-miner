from datetime import datetime
import json
import time

import requests

from nba_warehouse.db.models import session, Game, Team, ActualGameSpread

# Build a list of distinct game dates
epoch_game_dates = []
for value in session.query(Game.game_date_est).filter(
        Game.season == '2016').distinct():
    # Add time to game_date date object then use timestamp to get epoch value
    game_date_timestamp = datetime.combine(
        value[0], datetime.min.time()).timestamp()

    # Have the epoch time include milliseconds
    epoch_datetime = round(game_date_timestamp * 1000)
    epoch_game_dates.append(epoch_datetime)

# Loop over epoch game dates
for epoch_game_date in epoch_game_dates:
    # Check to see if speads exists for the current date being iterated over
    actual_game_spreads = session.query(ActualGameSpread).filter(
        ActualGameSpread.epoch_datetime == str(epoch_game_date)
    ).all()

    # If no spreads for current date
    if not actual_game_spreads:
        # Convert epoch time back to date object for querying Games later
        game_date = datetime.fromtimestamp(epoch_game_date / 1000).date()
        print(epoch_game_date)
        print(game_date)
        
        api_url = 'https://www.sportsbookreview.com/ms-odds-v2/odds-v2-service?query={+eventsByDateByLeagueGroup(+leagueGroups:+[{+mtid:+401,+lid:+5,+spid:+5+}],+providerAcountOpener:+3,+hoursRange:+25,+showEmptyEvents:+true,+marketTypeLayout:+%22PARTICIPANTS%22,+ic:+false,+startDate:+' + str(epoch_game_date) + ',+timezoneOffset:+0,+nof:+true,+hl:+true,+sort:+{by:+[%22lid%22,+%22dt%22,+%22des%22],+order:+ASC}+)+{+events+{+eid+lid+spid+des+dt+es+rid+ic+ven+tvs+cit+cou+st+sta+hl+seid+writeingame+consensus+{+eid+mtid+bb+boid+partid+sbid+paid+lineid+wag+perc+vol+tvol+wb+sequence+}+plays(pgid:+2,+limitLastSeq:+3,+pgidWhenFinished:+-1)+{+eid+sqid+siid+gid+nam+val+tim+}+scores+{+partid+val+eid+pn+sequence+}+participants+{+eid+partid+psid+ih+rot+tr+sppil+startingPitcher+{+fn+lnam+}+source+{+...+on+Player+{+pid+fn+lnam+}+...+on+Team+{+tmid+lid+nam+nn+sn+abbr+cit+}+...+on+ParticipantGroup+{+partgid+nam+lid+participants+{+eid+partid+psid+ih+rot+source+{+...+on+Player+{+pid+fn+lnam+}+...+on+Team+{+tmid+lid+nam+nn+sn+abbr+cit+}+}+}+}+}+}+marketTypes+{+mtid+spid+nam+des+settings+{+sitid+did+alias+layout+format+template+sort+url+}+}+currentLines(paid:+[20,+3,+10,+8,+9,+44,+29,+38,+16,+65,+92,+28,+83,+84,+82,+4,+15,+35,+45,+54,+22,+18,+5,+36,+78])+openingLines+eventGroup+{+egid+nam+}+statistics(sgid:+3,+sgidWhenFinished:+4)+{+val+eid+nam+partid+pid+typ+siid+sequence+}+league+{+lid+nam+rid+spid+sn+settings+{+alias+rotation+ord+shortnamebreakpoint+}+}+}+maxSequences+{+events:+eventsMaxSequence+scores:+scoresMaxSequence+currentLines:+linesMaxSequence+statistics:+statisticsMaxSequence+plays:+playsMaxSequence+consensus:+consensusMaxSequence+}+}+}'

        print(api_url)

        r = requests.get(api_url)
        try:
            sbr_data = json.loads(r.content)
        except json.decoder.JSONDecodeError:
            r = requests.get(api_url)
            sbr_data = json.loads(r.content)

        for event in sbr_data['data']['eventsByDateByLeagueGroup']['events']:
            # Get the home team city
            home_team_city = event['des'].split('@')[1]
            if home_team_city == 'L.A. Lakers':
                home_team_city = 'Los Angeles'
            elif home_team_city == 'L.A. Clippers':
                home_team_city = 'Los Angeles'

            # Dict that will hold needed data from api
            home_team_detail = {}
            # Loop over participants and find the record that matches the
            # home team
            for participant in event['participants']:
                if participant['source']['cit'] == home_team_city:
                    # Participant id
                    home_team_detail['partid'] = participant['partid']
                    # Team abbreviation which will match up with Teams table
                    home_team_detail['abbr'] = participant['source']['abbr']

            # Loop over the currentLines objects and get the record that is
            # pinnacle book (which seems to be paid=20) and partid matches
            # current home team
            for line in event['currentLines']:
                if line['paid'] == 20 and \
                        home_team_detail['partid'] == line['partid']:
                    # Get spread number
                    home_team_detail['adj'] = line['adj']
                    # Get spread moneyline
                    home_team_detail['ap'] = line['ap']
            # Query for game that matches the data and home team on abbr
            game = session.query(Game).filter_by(
                game_date_est=game_date).join(Game.home_team).filter(
                Team.tricode == home_team_detail['abbr']).first()
            try:
                # Setup data for insert and insert it
                game_spread_insert = {
                    'game_id': game.game_id,
                    'pinnacle_closing': home_team_detail['adj'],
                    'pinnacle_moneyline': home_team_detail['ap'],
                    'epoch_datetime': epoch_game_date
                }
                # print('inserting': game_spread_insert)
                game_spread = ActualGameSpread(**game_spread_insert)
                session.add(game_spread)
                session.commit()
            except AttributeError:
                print('*****************************')
                print('err inserting: ', home_team_detail)

        time.sleep(20)
