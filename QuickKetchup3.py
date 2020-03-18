import os
#import numpy as np

def get_index(header, name):
    try:
        ind = header.index(name)
    except:
        print("Typo in Name")
        return "Error"
    return ind

def check_float(f):
    try:
        float(f)
    except ValueError:
        return False
    return True

#parameters
file_path = "C:/Users/benja/OneDrive/Documents/DDSPF/Leagues/S17W12final/Output/S17W12final_Games.csv"
num_strats = 1
num_test_sims = 300
team_to_test = "Home"

# Build Custom Dictionary
trial_count = 0
strat_dictionary = {}
cur_strat = 1
with open(file_path) as game_data_file:
    header = game_data_file.readline().strip().split(",")
    for line in game_data_file:
        temp = line.strip().split(",")
        line = []
        for li in temp:
            if check_float(li):
                line.append(float(li))
            else:
                line.append(li)
        gametype = line[-2]
        if gametype != "Exhibition":
            continue
        trial_count+=1
        if trial_count < num_test_sims:
            if cur_strat in strat_dictionary.keys():
                strat_dictionary[cur_strat].append([l for l in line])
            else:
                strat_dictionary[cur_strat] = [[l for l in line]]
        else:
            if cur_strat == num_strats:
                break
            trial_count = 0
            cur_strat+=1
            strat_dictionary[cur_strat] = [[l for l in line]]

# Compute All Stats
for strat in strat_dictionary.keys():
    wins = []
    top = []
    score_for = []
    score_against = []
    rush_for = []
    rush_against = []
    pass_for = []
    pass_against = []
    third_down_conv = []
    turnovers = []
    penal = []
    #rush_1 = []
    #rush_2 = []
    #rush_3 = []
    #pass_1 = []
    #pass_2 = []
    #pass_3 = []
    for trial in strat_dictionary[strat]:

        # Win %
        home_score = trial[get_index(header, "HomeScore")]; away_score = trial[get_index(header, "AwayScore")]
        if team_to_test == "Home":
            if home_score > away_score:
                wins.append(1)
            else:
                wins.append(0)
        else:
            if away_score > home_score:
                wins.append(1)
            else:
                wins.append(0)

        # Average TOP
        if team_to_test == "Home":
            ind = get_index(header, "HomeTOP")
            top.append(trial[ind])
        else:
            ind = get_index(header, "AwayTOP")
            top.append(trial[ind])

        # Average Score for
        if team_to_test == "Home":
            ind = get_index(header, "HomeScore")
            score_for.append(trial[ind])
        else:
            ind = get_index(header, "AwayScore")
            score_for.append(trial[ind])

        # Average Score against
        if team_to_test == "Home":
            ind = get_index(header, "AwayScore")
            score_against.append(trial[ind])
        else:
            ind = get_index(header, "HomeScore")
            score_against.append(trial[ind])

        # Rush Yards for
        if team_to_test == "Home":
            ind = get_index(header, "HomeRushYds")
            rush_for.append(trial[ind])
        else:
            ind = get_index(header, "AwayRushYds")
            rush_for.append(trial[ind])

        # Pass Yards for
        if team_to_test == "Home":
            ind = get_index(header, "HomePassYds")
            pass_for.append(trial[ind])
        else:
            ind = get_index(header, "AwayPassYds")
            pass_for.append(trial[ind])

        # Rush Yards against
        if team_to_test == "Home":
            ind = get_index(header, "AwayRushYds")
            rush_against.append(trial[ind])
        else:
            ind = get_index(header, "HomeRushYds")
            rush_against.append(trial[ind])

        # Pass Yards against
        if team_to_test == "Home":
            ind = get_index(header, "AwayPassYds")
            pass_against.append(trial[ind])
        else:
            ind = get_index(header, "HomePassYds")
            pass_against.append(trial[ind])

        # 3rd Down Conversion %
        if team_to_test == "Home":
            ind1 = get_index(header, "Home3rdDownAtt")
            ind2 = get_index(header, "Home3rdDownComp")
            third_down_conv.append(float(trial[ind2])/trial[ind1])
        else:
            ind1 = get_index(header, "Away3rdDownAtt")
            ind2 = get_index(header, "Away3rdDownComp")
            third_down_conv.append(float(trial[ind2])/trial[ind1])

        #Turnovers
        if team_to_test == "Home":
            ind1 = get_index(header, "AwayInt")
            ind2 = get_index(header, "HomeFumblesLost")
            turnovers.append(trial[ind1]+trial[ind2])
        else:
            ind1 = get_index(header, "HomeInt")
            ind2 = get_index(header, "AwayFumblesLost")
            turnovers.append(trial[ind1] + trial[ind2])
            turnovers.append(trial[ind])

        #Penalties
        if team_to_test == "Home":
            ind = get_index(header, "HomePenalties")
            penal.append(trial[ind])
        else:
            ind = get_index(header, "AwayPenalties")
            penal.append(trial[ind])

    #Compute Final Summary Stats for this strat
    win_per = float(sum(wins))/len(wins)
    avg_top = float(sum(top))/len(top)#; stddev_top = np.std(top)
    avg_score_for = float(sum(score_for)) / len(score_for)#; stddev_score_for = np.std(score_for)
    avg_score_against = float(sum(score_against)) / len(score_against)#; stddev_score_against = np.std(score_against)
    avg_rush_for = float(sum(rush_for)) / len(rush_for)#; stddev_rush_for = np.std(rush_for)
    avg_rush_against = float(sum(rush_against)) / len(rush_against)#; stddev_rush_against = np.std(rush_against)
    avg_pass_for = float(sum(pass_for)) / len(pass_for)#; stddev_pass_for = np.std(pass_for)
    avg_pass_against = float(sum(pass_against)) / len(pass_against)#; stddev_pass_against = np.std(pass_against)
    avg_third_down = float(sum(third_down_conv)) / len(third_down_conv)#; stddev_third_down = np.std(third_down_conv)
    avg_turnover = float(sum(turnovers)) / len(turnovers)#; stddev_turnover = np.std(turnovers)
    avg_penal = float(sum(penal)) / len(penal)#; stddev_penal = np.std(penal)

    #Output results of Strat
    print("-----------------------------------")
    print("Strategy", strat)
    print("Win Percentage:", win_per, "%")
    print("Points Scored:", avg_score_for)#, "+/-", stddev_score_for
    print("Points Against:", avg_score_against)#, "+/-", stddev_score_against
    print("Rushing Yards:", avg_rush_for)#, "+/-", stddev_rush_for
    print("Passing Yards:", avg_pass_for)#, "+/-", stddev_pass_for
    print("Time of Possession:", avg_top)#, "+/-"
    print("Third Down Conversion Rate:", avg_third_down)#, "%", "+/-", stddev_third_down
    print("Rushing Yards Against:", avg_rush_against)#, "+/-", stddev_rush_against
    print("Passing Yards Against:", avg_pass_against)#, "+/-", stddev_pass_against
    #print "Turnovers:", avg_turnover, "+/-", stddev_turnover
    print("Penalties:", avg_penal)#, "+/-", stddev_penal
    print("-----------------------------------")











