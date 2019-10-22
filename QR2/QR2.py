import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

def answer_ariss_Question(p):
    h0='Null Hypothesis: there isn\'t an home field advantage'
    h1='Alternate Hypothesis: there is an home field advantage'
    alpha=0.05
    print('We have two Hypotesis:', file=f)
    print(h0, file=f)
    print(h1, file=f)

    print('Our p-value is :{}'.format(p), file=f)
    print('Because ', end='', file=f)
    if(p<0.05):
        print('p-value is less than alpha=0.05, we have to reject the {} and'.format(h0), file=f)
        print('We have to accept the {}'.format(h1), file=f)
    else:
        print('p-value is grader than alpha=0.05, We have to accept the {}'.format(h0), file=f)


def get_contigency_table(teams):#teams: set of teamsIds
    if type(teams)!=set:
        teams=set([teams]) #this is for having only one function to give the cont. table of only one team or of a set of teams

    match = pd.read_json(r'/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/matches/matches_England.json')
    rowToDrop=match.loc[match.status!='Played']
    match.drop(rowToDrop.index, inplace=True)
    colToDrop=['status', 'roundId', 'gameweek', 'seasonId', 'dateutc', 'venue', 'label', 'date', 'referees', 'duration', 'competitionId']
    match.drop(colToDrop, axis=1, inplace=True)

    matchOfTeam=pd.DataFrame(columns=['wyId', 'side', 'winner'])#create a dataframe empty

    for team in teams:
        for idex, row in match.iterrows():#iterate over matches
            teamsDataDict=dict(row['teamsData'])#take the dictionary inside the field teamsData
            keys=list(teamsDataDict.keys())
            teams_copy=set(teams) #create a copy of our teams
            len_before=len(teams_copy)#the len of teams
            k1=keys[0] #take team1 in the match iteration
            k2=keys[1] #take team2 in the match iteration
            #print('teams before: ', teams_copy, '\n k1: {}, k2: {}'.format(k1, k2))
            teams_copy.discard(int(k1)) #delete team1 from the set of teams if it's present
            teams_copy.discard(int(k2)) #delete team2 from the set of teams if it's present
            #print('tems after: ', teams_copy)
            if len(teams_copy)==len_before-1:#if teams has only one less elemnt, so only k1 or k2 was remove.
                                            #it means the match includes only one team of our teams
                                            #if teams had only one element, its the same
                myRow={}
                infoTeam=list(teamsDataDict.values())[0] if keys[0]==str(team) else list(teamsDataDict.values())[1]
                #take the infoTeam inside the dictionary of teamsData
                myRow['wyId']=[row['wyId']]
                myRow['side']=[infoTeam['side']]
                myRow['winner']=[row['winner']]
                #and take information about side e winner
                myRowDf=pd.DataFrame(myRow, columns=['wyId', 'side', 'winner']) #create a dataframe to concatenate
                matchOfTeam=pd.concat([matchOfTeam, myRowDf], ignore_index=True) #compose the dataframe

    #now we have a dataframe with all match palyed

    #perform selection on this dataframe in order to fill this table
    #        Win  |  Draw  |  lose
    #------------------------------
    #home |       |        |
    #------------------------------
    #away |       |        |
    #------------------------------

    winHome= matchOfTeam.loc[(matchOfTeam['side']=='home') & (matchOfTeam['winner']==team)].shape[0]   #.shape[0] count the number of row
    winAway= matchOfTeam.loc[(matchOfTeam['side']=='away') & (matchOfTeam['winner']==team)].shape[0]
    drawHome= matchOfTeam.loc[(matchOfTeam['side']=='home') & (matchOfTeam['winner']==0)].shape[0]
    drawAway= matchOfTeam.loc[(matchOfTeam['side']=='away') & (matchOfTeam['winner']==0)].shape[0]
    loseHome= matchOfTeam.loc[(matchOfTeam['side']=='home') & (matchOfTeam['winner']!=team)].shape[0]
    loseAway= matchOfTeam.loc[(matchOfTeam['side']=='away') & (matchOfTeam['winner']!=team)].shape[0]
    #print(matchOfTeam)
    #print(winHome)
    arr=np.array([[winHome, drawHome, loseHome], [winAway, drawAway, loseAway]])
    #print(arr)
    return arr





#We choosed the following 5 teams with their id
Manchester_Utd = 1611
Manchester_city = 1625
Liverpool = 1623
Arsenal = 1609
Chelsea = 1610

with open('/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/matches/Answer_RQ2.txt', 'w') as f:


    #Manchester Utd
    print('Team 1\n', file=f)
    contTable=get_contigency_table(Manchester_Utd)
    print('Contingency Table\n', contTable, file=f)
    print('', file=f)

    #Manchester_city
    print('Team 2\n', file=f)
    contTable=get_contigency_table(Manchester_city)
    print('Contingency Table\n', contTable, file=f)
    print('', file=f)

    #Liverpool
    print('Team 3\n', file=f)
    contTable=get_contigency_table(Liverpool)
    print('Contingency Table\n', contTable, file=f)
    print('', file=f)

    #Arsenal
    print('Team 4\n', file=f)
    contTable=get_contigency_table(Arsenal)
    print('Contingency Table\n', contTable, file=f)
    print('', file=f)

    #Chelsea
    print('Team 5\n', file=f)
    contTable=get_contigency_table(Chelsea)
    print('Contingency Table\n', contTable, file=f)
    print('', file=f)


    s=set([Manchester_Utd, Manchester_city, Liverpool, Arsenal, Chelsea])
    uniqeContTable=get_contigency_table(s)
    print('Unique contingecy table: \n', uniqeContTable, file=f)
    chi2, p, dof, exp = chi2_contingency(uniqeContTable, correction=False)
    print('chi2 = {}\n p = {}\n dof = {}\n exp:\n{}'.format(chi2, p, dof, exp), file=f)
    answer_ariss_Question(p)
    print('Concludions:\n', file=f)
    print("we have too little data to carry out a meaningful analysis.", file=f)
    print("We should also carry out further tests in addition to chi2 in order to better investigate the correlation between the two variables analysed", file=f)
