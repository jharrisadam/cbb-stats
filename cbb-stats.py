"""This is an attempt to collect NCAA D1 Basketball stats and create a
predictive model for the upcoming season. Much of the underlying math is
inspired by Ken Pomeroy and Jeff Sagarin. Stats pulled from
https://www.sports-reference.com/cbb/"""

import numpy as np
import pandas as pd

# Pull data for use
full_sheet = pd.read_csv('2017Stats.csv', sep=',')
team_names = []
team_rate = []


# Create simulation report
def boxscore(home, homescore, away, awayscore, totalposs):
        print(home, ": ", homescore, ", ", away, ": ", awayscore, ", Possessions: ", totalposs)

# Determine number of possessions
def find_poss(fga, oreb, turnover, fta, games):
    return((int(fga) - int(oreb) + int(turnover) +.475*int(fta))/int(games))

# Determine effective field goal percentage
def find_efgp(fgm, threesmade, fga):
    return((fgm + threesmade * 0.5) / fga)

# Determine offensive points per possession
def find_oppp(opoints, games, poss):
    return((opoints/games)/poss)

# Determine defensive points per possession
def find_dppp(dpoints, games, poss):
    return((dpoints/games)/poss)

def play(home, away):
    totalposs = int(round(home[1] + away[1]) / 2)
    homescore = int(round(((home[2] + away[3]) / 2) * totalposs) + 3.25)
    awayscore = int(round(((home[3] + away[2]) / 2) * totalposs))
    boxscore(home[0], homescore, away[0], awayscore, totalposs)

# Run simulation
def sim():
    a = ""
    b = ""
    while a not in team_names:
        a = input("Home team: ")
    a_ind = team_names.index(a)
    while b not in team_names:
        b = input("Away team: ")
    b_ind = team_names.index(b)
    play(team_rate[a_ind], team_rate[b_ind])

# Loop all teams to fill Team Ratings dictionary with team names & ratings
for i in range(len(full_sheet)):
    if full_sheet.loc[i, 'School'].endswith("\xa0"):
        full_sheet.loc[i, 'School'] = full_sheet.loc[i, 'School'][:-1]
    temp_poss = find_poss(full_sheet.loc[i,'FGA'],full_sheet.loc[i,'ORB'],full_sheet.loc[i,'TOV'],full_sheet.loc[i,'FTA'],full_sheet.loc[i,'G'])
    temp_efgp = find_efgp(full_sheet.loc[i,'FG'], full_sheet.loc[i,'3P'], full_sheet.loc[i,'FGA'])
    temp_oppp = find_oppp(full_sheet.loc[i,'Tm.'], full_sheet.loc[i,'G'], temp_poss)
    temp_dppp = find_dppp(full_sheet.loc[i,'Opp.'], full_sheet.loc[i,'G'], temp_poss)
    team_names.append(full_sheet.loc[i,'School'])
    team_rate.append([full_sheet.loc[i,'School'], temp_poss, temp_oppp, temp_dppp])

for i in team_rate:
    print(i, '\n')

sim()
