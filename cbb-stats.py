"""This is an attempt to collect NCAA D1 Basketball stats and create a
predictive model for the upcoming season. Much of the underlying math is
inspired by Ken Pomeroy and Jeff Sagarin. Stats pulled from
https://www.sports-reference.com/cbb/"""

import numpy as np
import pandas as pd
import random

# Pull data for use
full_sheet = pd.read_csv('2017Stats.csv', sep=',')
team_names = []
team_rate = []
avg_o = 0
avg_d = 0
sim_result = []


# Create game report for a single game
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

# Add luck factor to results
def chaos(stat):
    a_min = int(round(stat * .95))
    a_max = int(round(stat * 1.05))
    a = random.randint(a_min, a_max)
    return a

# Run individual game simulation
def play(home, away, neutral):
    totalposs = int(round(home[1] + away[1]) / 2)
    totalposs = chaos(totalposs)
    temp_home_o = home[2]-avg_o
    temp_home_d = home[3]-avg_d
    temp_away_o = away[2]-avg_o
    temp_away_d = away[3]-avg_d
    if neutral == False:
        homescore = ((temp_home_o + temp_away_d + avg_o) + .0325) * totalposs
    elif neutral == True:
        homescore = (temp_home_o + temp_away_d + avg_o) * totalposs
    awayscore = (temp_home_d + temp_away_o + avg_o) * totalposs
    x = chaos(homescore)
    y = chaos(awayscore)
    boxscore(home[0], x, away[0], y, totalposs)
    if x > y:
        return 1
    elif y > x:
        return 2
# Using efgp as tiebreaker
    elif homescore == awayscore:
        if home[4] > away[4]:
            return 1
        elif away[4] > home[4]:
            return 2
        else:
            return None
    else:
        return None

# Run bulk simulation
def sim():
    a = ""
    b = ""
    c = ""
    neutral = True
    neutral_list = ["y", "Y", "n", "N"]
    while a not in team_names:
        a = input("Home team: ")
    a_ind = team_names.index(a)
    while b not in team_names:
        b = input("Away team: ")
    b_ind = team_names.index(b)
    while c not in neutral_list:
        c = input("Neutral site Y/N: ")
        if c == "y" or "Y":
            neutral = False
        elif c == "n" or "C":
            neutral == False
    for i in range(0, 100):
        result = play(team_rate[a_ind], team_rate[b_ind], neutral)
        sim_result.append(result)
    print(a, sim_result.count(1), (sim_result.count(1)/len(sim_result)), b, sim_result.count(2), (sim_result.count(2)/len(sim_result)))

# Loop all teams to fill Team Ratings dictionary with team names & ratings
for i in range(len(full_sheet)):
    if full_sheet.loc[i, 'School'].endswith("\xa0"):
        full_sheet.loc[i, 'School'] = full_sheet.loc[i, 'School'][:-1]
    temp_poss = find_poss(full_sheet.loc[i,'FGA'],full_sheet.loc[i,'ORB'],full_sheet.loc[i,'TOV'],full_sheet.loc[i,'FTA'],full_sheet.loc[i,'G'])
    temp_efgp = find_efgp(full_sheet.loc[i,'FG'], full_sheet.loc[i,'3P'], full_sheet.loc[i,'FGA'])
    temp_oppp = find_oppp(full_sheet.loc[i,'Tm.'], full_sheet.loc[i,'G'], temp_poss)
    temp_dppp = find_dppp(full_sheet.loc[i,'Opp.'], full_sheet.loc[i,'G'], temp_poss)
    team_names.append(full_sheet.loc[i,'School'])
    if avg_o == 0:
        avg_o = temp_oppp
    else:
        avg_o += temp_oppp
        avg_o = avg_o/2
    if avg_d == 0:
        avg_d = temp_dppp
    else:
        avg_d += temp_dppp
        avg_d = avg_d/2
    team_rate.append([full_sheet.loc[i,'School'], temp_poss, temp_oppp, temp_dppp, temp_efgp])

#for i in team_rate:
#    print(i, '\n')

sim()
