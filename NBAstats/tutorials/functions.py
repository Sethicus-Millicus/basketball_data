import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt 
import base64
import numpy as np 
from nba_api.stats.static import players



st.title('NBA Player Data')

# add mark down

# First we need to get out list of players from nba_api
nba_players = players.get_active_players()

# now we run a function to get the players info