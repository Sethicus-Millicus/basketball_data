import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt 
import base64
import numpy as np 
from nba_api.stats.static import players
from nba_api.stats.endpoints import fantasywidget



st.title('NBA Player Data')

# add mark down

# First we need to get out list of players from nba_api
nba_players = players.get_active_players()

# now we run a function to get the players info
@st.cache
def load_data():
	df = fantasywidget.FantasyWidget(todays_players = 'Y')
	df = df.get_data_frames()[0]
	df.round(1)
	df.rename(columns={"PLAYER_POSITION": "POS", "TEAM_ABBREVIATION": "TEAM", "FAN_DUEL_PTS":"FD"}, inplace=True)
	df.drop(columns=['PLAYER_ID', 'TEAM_ID', 'NBA_FANTASY_PTS', 'FT_PCT'], inplace=True)
	df = df.sort_values(by = ['TEAM'])
	df['team_rank'] = df.groupby(['TEAM'])['FD'].rank(method='max', ascending = False).astype(int)
	df = df[df['team_rank'] <= 5]
	return df
#will add a parameter for fucntion
playerstats = load_data()

#Team selection
sorted_unique_team = sorted(playerstats.TEAM.unique())
selected_team = st.multiselect('Team', sorted_unique_team, sorted_unique_team)


# filtering data
df_selected_team = playerstats[(playerstats.TEAM.isin(selected_team))]


st.header('Display Player Stats for Today')
st.write('Data Dimension:' + str(playerstats.shape[0]) +' rows and '+ str(playerstats.shape[0]) +' columns.')
st.dataframe(df_selected_team)



