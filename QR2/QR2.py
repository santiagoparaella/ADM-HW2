#this file was written by Santo Palaia and shared with olthers group members

import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

def get_team_contingecy_table(team): #return the dataframe that rapresent the contigency table of a team(number)
    match = pd.read_json(r'/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/matches/matches_England.json')
    rowToDrop=match.loc[match.status!='Played']
    match.drop(rowToDrop.index, inplace=True)
    colToDrop=['status', 'roundId', 'gameweek', 'seasonId', 'dateutc', 'venue', 'label', 'date', 'referees', 'duration', 'competitionId']
    match.drop(colToDrop, axis=1, inplace=True)
    matchOfTeam=pd.DataFrame(columns=['wyId', 'side', 'winner'])#create a dataframe empty
    for idex, row in match.iterrows():#iterate over matches
        teamsDataDict=dict(row['teamsData'])#take the dictionary inside the field teamsData
        keys=list(teamsDataDict.keys())

        if keys[0]==str(team) or keys[1]==str(team):#if a match includes our team
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
      
    winHome= matchOfTeam.loc[(matchOfTeam['side']=='home') & (matchOfTeam['winner']==team)].shape[0]    
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






    
#We choosed the following 5 teams with their id
Manchester_Utd = 1611
Manchester_city = 1625
Liverpool = 1623
Arsenal = 1609
Chelsea = 1610

with open('/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/matches/Answer_RQ2.txt', 'w') as f:
    
    
    #Manchester Utd
    print('Test 1\n', file=f)
    contTable=get_team_contingecy_table(Manchester_Utd)
    chi2_1, p_1, dof_1, exp_1 = chi2_contingency(contTable, correction=False)
    print('Contingency Table\n', contTable, file=f)
    print('chi2: ', chi2_1, file=f)
    print('p: ', p_1, file=f)
    print('dof: ', dof_1, file=f)
    print('expeted: ','\n', exp_1, file=f)
    answer_ariss_Question(p_1)
    print('', file=f)
    
    #Manchester_city
    print('Test 2\n', file=f)
    print('Contingency Table\n', contTable, file=f)
    contTable=get_team_contingecy_table(Manchester_city)
    chi2_2, p_2, dof_2, exp_2 = chi2_contingency(contTable, correction=False)
    print('chi2: ', chi2_2, file=f)
    print('p: ', p_2, file=f)
    print('dof: ', dof_2, file=f)
    print('expeted: ','\n', exp_2, file=f)
    answer_ariss_Question(p_2)
    print('', file=f)
    
    #Liverpool
    print('Test 3\n', file=f)
    print('Contingency Table\n', contTable, file=f)
    contTable=get_team_contingecy_table(Liverpool)
    chi2_3, p_3, dof_3, exp_3 = chi2_contingency(contTable, correction=False)
    print('chi2: ', chi2_3, file=f)
    print('p: ', p_3, file=f)
    print('dof: ', dof_3, file=f)
    print('expeted: ','\n', exp_3, file=f)
    answer_ariss_Question(p_3)
    print('', file=f)
    
    #Arsenal
    print('Test 4\n', file=f)
    print('Contingency Table\n', contTable, file=f)
    contTable=get_team_contingecy_table(Manchester_Utd)
    chi2_4, p_4, dof_4, exp_4 = chi2_contingency(contTable, correction=False)
    print('chi2: ', chi2_4, file=f)
    print('p: ', p_4, file=f)
    print('dof: ', dof_4, file=f)
    print('expeted: ','\n', exp_4, file=f)
    answer_ariss_Question(p_4)
    print('', file=f)
    
    #Chelsea
    print('Test 5\n', file=f)
    print('Contingency Table\n', contTable, file=f)
    contTable=get_team_contingecy_table(Manchester_Utd)
    chi2_5, p_5, dof_5, exp_5 = chi2_contingency(contTable, correction=False)
    print('chi2: ', chi2_5, file=f)
    print('p: ', p_5, file=f)
    print('dof: ', dof_5, file=f)
    print('expeted: ','\n', exp_5, file=f)
    answer_ariss_Question(p_5)
    print('', file=f)
    
    print('Concludions:\n', file=f)
    print("we have too little data to carry out a meaningful analysis.", file=f)
    print("We should also carry out further tests in addition to chi2 in order to better investigate the correlation between the two variables analysed", file=f)
