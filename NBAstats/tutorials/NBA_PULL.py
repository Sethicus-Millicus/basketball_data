import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo, scoreboard, scoreboardv2, \
playerdashptshotdefend, boxscoreadvancedv2, boxscoremiscv2, boxscorescoringv2, \
boxscoresummaryv2, boxscoretraditionalv2, boxscoreusagev2, boxscoreplayertrackv2, \
boxscorefourfactorsv2, leaguegamelog, shotchartdetail, playbyplayv2, commonallplayers


import datetime as dt
import random
import time


teams  = pd.DataFrame(teams.get_teams())

games = pd.read_csv('game_dates_pulled.csv')
games = games[games['pulled']!= "done"]

custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

for i, row in games.iterrows():
    
    #add some sleep time between pulls
    if i%1000 == 0:
        time.sleep(random.uniform(0,60))
    elif i%100 == 0:
        time.sleep(random.uniform(0,10))
    elif i%10 == 0:
        time.sleep(random.uniform(0,3))
        
    # check to see if already done
    if row['pulled'] == 'done':
        pass
    # not done pull scoreboard
    else:
        gd = row['dates']
        sb = scoreboardv2.ScoreboardV2(game_date = gd, headers = custom_headers, timeout=100).get_data_frames()[0]
        sb= sb[(sb['HOME_TEAM_ID'].isin(teams.id)) & (sb['GAME_STATUS_TEXT'] != "PPD") & (sb['GAME_SEQUENCE']!= 0)]
        # If nothing in scoreboard- no games, preseason, or all star game, set pulled to done
        if len(sb)== 0:
            games.loc[i, 'pulled']='done'
            os.chdir("/Users/Dan/Desktop/medium_tutorials/intro_nba_api/")
            games.to_csv('game_dates_pulled.csv', index=False)
            pass
        gids = sb['GAME_ID']
        gids.reset_index(inplace=True, drop=True)
        # pulling data for each game ID (gids) that we gathered from scoreboards dataframe'
        for j, gid in enumerate(gids):
            if j == 0:
                player_bs_advanced = boxscoreadvancedv2.BoxScoreAdvancedV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0]
                team_bs_advanced= boxscoreadvancedv2.BoxScoreAdvancedV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1]

                player_bs_ff = boxscorefourfactorsv2.BoxScoreFourFactorsV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0]
                team_bs_ff = boxscorefourfactorsv2.BoxScoreFourFactorsV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1]

                player_bs_misc = boxscoremiscv2.BoxScoreMiscV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0]
                team_bs_misc = boxscoremiscv2.BoxScoreMiscV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1]

                player_bs_pt = boxscoreplayertrackv2.BoxScorePlayerTrackV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0]
                team_bs_pt = boxscoreplayertrackv2.BoxScorePlayerTrackV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1]

                player_bs_scoring = boxscorescoringv2.BoxScoreScoringV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0]
                team_bs_scoring = boxscorescoringv2.BoxScoreScoringV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1]

                player_bs_summ = boxscoresummaryv2.BoxScoreSummaryV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0]
                team_bs_summ = boxscoresummaryv2.BoxScoreSummaryV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1]

                player_bs_trad = boxscoretraditionalv2.BoxScoreTraditionalV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0]
                team_bs_trad = boxscoretraditionalv2.BoxScoreTraditionalV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1]

                player_bs_usage = boxscoreusagev2.BoxScoreUsageV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0]
            else:
                player_bs_advanced = player_bs_advanced.append(boxscoreadvancedv2.BoxScoreAdvancedV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0])
                team_bs_advanced = team_bs_advanced.append(boxscoreadvancedv2.BoxScoreAdvancedV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1])

                player_bs_ff = player_bs_ff.append(boxscorefourfactorsv2.BoxScoreFourFactorsV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0])
                team_bs_ff = team_bs_ff.append(boxscorefourfactorsv2.BoxScoreFourFactorsV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1])

                player_bs_misc = player_bs_misc.append(boxscoremiscv2.BoxScoreMiscV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0])
                team_bs_misc = team_bs_misc.append(boxscoremiscv2.BoxScoreMiscV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1])

                player_bs_pt = player_bs_pt.append(boxscoreplayertrackv2.BoxScorePlayerTrackV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0])
                team_bs_pt = team_bs_pt.append(boxscoreplayertrackv2.BoxScorePlayerTrackV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1])

                player_bs_scoring = player_bs_scoring.append(boxscorescoringv2.BoxScoreScoringV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0])
                team_bs_scoring = team_bs_scoring.append(boxscorescoringv2.BoxScoreScoringV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1])

                player_bs_summ = player_bs_summ.append(boxscoresummaryv2.BoxScoreSummaryV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0])
                team_bs_summ = player_bs_summ.append(boxscoresummaryv2.BoxScoreSummaryV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1])
                
                player_bs_trad = player_bs_trad.append(boxscoretraditionalv2.BoxScoreTraditionalV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0])
                team_bs_trad = team_bs_trad.append(boxscoretraditionalv2.BoxScoreTraditionalV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[1])

                player_bs_usage = player_bs_usage.append(boxscoreusagev2.BoxScoreUsageV2(gid, headers = custom_headers, timeout = 100).get_data_frames()[0])
        # Now we have all dfs and we can save them to csv files
        filename = 'nba_DFs/player_bs_advanced_{}.csv'.format(gd)
        player_bs_advanced['file_name'] = filename
        player_bs_advanced.to_csv(filename, index=False)

        filename = 'nba_DFs/team_bs_advanced_{}.csv'.format(gd)
        team_bs_advanced['file_name'] = filename
        team_bs_advanced.to_csv(filename, index=False)

        filename = 'nba_DFs/player_bs_ff_{}.csv'.format(gd)
        player_bs_ff['file_name'] = filename
        player_bs_ff.to_csv(filename, index=False)

        filename = 'nba_DFs/team_bs_ff_{}.csv'.format(gd)
        team_bs_ff['file_name'] = filename
        team_bs_ff.to_csv(filename, index=False)

        filename = 'nba_DFs/player_bs_misc_{}.csv'.format(gd)
        player_bs_misc['file_name'] = filename
        player_bs_misc.to_csv(filename, index=False)

        filename = 'nba_DFs/team_bs_misc_{}.csv'.format(gd)
        team_bs_misc['file_name'] = filename
        team_bs_misc.to_csv(filename, index=False)

        filename = 'nba_DFs/player_bs_pt_{}.csv'.format(gd)
        player_bs_pt['file_name'] = filename
        player_bs_pt.to_csv(filename, index=False)
        
        filename = 'nba_DFs/team_bs_pt_{}.csv'.format(gd)
        team_bs_pt['file_name'] = filename
        team_bs_pt.to_csv(filename, index=False)

        filename = 'nba_DFs/player_bs_scoring_{}.csv'.format(gd)
        player_bs_scoring['file_name'] = filename
        player_bs_scoring.to_csv(filename, index=False)

        filename = 'nba_DFs/team_bs_scoring_{}.csv'.format(gd)
        team_bs_scoring['file_name'] = filename
        team_bs_scoring.to_csv(filename, index=False)

        filename = 'nba_DFs/player_bs_summ_{}.csv'.format(gd)
        player_bs_summ['file_name'] = filename
        player_bs_summ.to_csv(filename, index=False)

        filename = 'nba_DFs/team_bs_summ_{}.csv'.format(gd)
        team_bs_summ['file_name'] = filename
        team_bs_summ.to_csv(filename, index=False)

        filename = 'nba_DFs/player_bs_trad_{}.csv'.format(gd)
        player_bs_trad['file_name'] = filename
        player_bs_trad.to_csv(filename, index=False)

        filename = 'nba_DFs/team_bs_trad_{}.csv'.format(gd)
        team_bs_trad['file_name'] = filename
        team_bs_trad.to_csv(filename, index=False)

        filename = 'nba_DFs/player_bs_usage_{}.csv'.format(gd)
        player_bs_usage['file_name'] = filename
        player_bs_usage.to_csv(filename, index=False)
        
        #mark as done
        games.loc[i, 'pulled']='done'
        games.to_csv('games_dates_pulled.csv', index=False)
        print("Completed pulling data for {}".format(gd))
