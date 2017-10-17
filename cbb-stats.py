""" This is an attempt to collect NCAA D1 Basketball stats and create a
predictive model for the upcoming season. Much of the underlying math is
inspired by Ken Pomeroy and Jeff Sagarin. Stats pulled from
https://www.sports-reference.com/cbb/"""

import numpy as np
import pandas as pd

# Pull data for use
full_sheet = pd.read_csv('2017Stats.csv', sep=',')
team_rate = []

# Determine number of offensive possessions
def off_poss(fga, oreb, turnover, fta, games):
    return((int(fga) - int(oreb) + int(turnover) +.475*int(fta))/int(games))

# Determine effective field goal percentage
def efgp(fgm, threesmade, fga):
    return((fgm + threesmade * 0.5) / fga)

# Loop all teams to fill Team Ratings array with team names & ratings
for i in range(len(full_sheet)):
    temp_oposs = off_poss(full_sheet.loc[i,'FGA'],full_sheet.loc[i,'ORB'],full_sheet.loc[i,'TOV'],full_sheet.loc[i,'FTA'],full_sheet.loc[i,'G'])
    temp_efgp = efgp(full_sheet.loc[i,'FG'], full_sheet.loc[i,'3P'], full_sheet.loc[i,'FGA'])
    team_rate.append([full_sheet.loc[i,'School'], temp_oposs, temp_efpg])

print(team_rate)
