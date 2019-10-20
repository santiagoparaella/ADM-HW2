#this file was written by Santo Palaia and shared with olthers group members

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Load the joson files
itMatch = pd.read_json(r'/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/matches/matches_England.json')
team=pd.read_json(r'/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/teams.json')

#load the match.json into list
jf=open('/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/matches/matches_England.json')
jfs=jf.read()
jfdata=json.loads(jfs)

#clean data -  This drops are need to improve efficiency
#team
team.drop('area', axis=1, inplace=True)
team.drop('officialName', axis=1, inplace=True)
team.drop('type', axis=1, inplace=True)
team.drop('city', axis=1, inplace=True)

#print('itMatch after\n', itMatch)
#itMatch

#add column with thw two team and remove the teamsData
first=[]
second=[]
for e in jfdata:
    first.append(list(e['teamsData'].keys())[0])
    second.append(list(e['teamsData'].keys())[1])

itMatch['team1']=first
itMatch['team2']=second

colToDrop=['seasonId', 'dateutc', 'teamsData', 'venue', 'wyId', 'label', 'referees', 'duration', 'competitionId', 'date']
itMatch.drop(colToDrop, axis=1, inplace=True)

#drop the matches with winner = 0

#rowToDrop=itMatch[itMatch.winner==0]
#itMatch.drop(rowToDrop.index, inplace=True)

#drop the matches that are not played yet
rowToDrop=itMatch.loc[itMatch.status!='Played']
itMatch.drop(rowToDrop.index, inplace=True)

itMatch.drop('status', axis=1, inplace=True)

#divide match into matches winner from someone and matches with a tied

itMatchWin=itMatch.loc[itMatch['winner']!=0]
#print('itMAtch win\n', itMatchWin)

itMatchTied=itMatch.loc[itMatch['winner']==0]
itMatchTied.drop('winner', axis=1, inplace=True)
#print('itMAtch tied\n', itMatchTied)

#saving in a json file
#export=itMatch.to_json(r'/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/matches/USmatches_Italy.json')

#Merge win match with team how wins
teamMatchWin=pd.merge(itMatchWin, team, left_on='winner', right_on='wyId', how='outer')

#Merge tied match with the two teams of the match
itMatchTied.loc[:,('team1')]=itMatchTied.loc[:, ('team1')].astype(int)
itMatchTied.loc[:,('team2')]=itMatchTied.loc[:, ('team2')].astype(int)
teamMatchTied=pd.merge(itMatchTied, team, left_on='team1', right_on='wyId', how='outer')
teamMatchTied.rename(columns={'name':'name_1'}, inplace=True)
teamMatchTied=pd.merge(teamMatchTied, team, left_on='team2', right_on='wyId', how='outer')
teamMatchTied.rename(columns={'name':'name_2'}, inplace=True)

# remove some row with NaN value
teamMatchWin.dropna(inplace=True)

teamMatchWin['roundId']=teamMatchWin['roundId'].astype(int)
teamMatchWin['gameweek']=teamMatchWin['gameweek'].astype(int)
teamMatchWin['winner']=teamMatchWin['winner'].astype(int)
#print('teamMatchWin\n', teamMatchWin)


d={}
for index, row in teamMatchWin.iterrows(): #inizilization of a dictionary with k: name of the team and value a list of list;
                                        #the fist element of internal list is the week, the second is the score
    d[str(row.loc['name'])]=[[0, 0]]


#we  want iterate over whe weeks to add to the dict a pair of (week, score) in order to obtain the point x, y for a plot


for i in range(1, 39):
    weekI=teamMatchWin.loc[teamMatchWin['gameweek']==i]
    weekIT=teamMatchTied.loc[teamMatchTied['gameweek']==i]

    #MatchWin

    for index, row in weekI.iterrows():
        #print(row['name'])
        listOfTeam=d[row.loc['name']]
        #print(listOfTeam)
        newScore=listOfTeam[len(listOfTeam)-1][1]+3
        d[row.loc['name']].append([i, newScore])

    #MAtchTied
    for index, row in weekIT.iterrows():
        #print(row)
        listOfTeam=d[row.loc['name_1']]
        #print(listOfTeam)
        newScore=listOfTeam[len(listOfTeam)-1][1]+1
        d[row.loc['name_1']].append([i, newScore])

        #print(row['name'])
        listOfTeam=d[row.loc['name_2']]
        #print(listOfTeam)
        newScore=listOfTeam[len(listOfTeam)-1][1]+1
        d[row.loc['name_2']].append([i, newScore])

#looking for longhest winning streak and longhest loosing streak
win1=''
win2=''
los1=''
los2=''

#winner

w=''
nw=0
for j in range(2):
    for k, v in d.items():
        #print(k)
        n=0
        prev=v[0]
        for i in range(1, len(v)):
            att=v[i]
            if att[0]==prev[0]+1:
                n+=1
            else:
                if n>nw and k!=win1:
                    nw=n
                    w=k
                n=0
            prev=att


    nw=0
    if j==0:
        win1=w
    else:
        win2=w

#print('win1 ', win1, 'win2', win2)

#save data of two "winner" to show them separately
w1=d[win1]
vec1=[i for [i, j] in w1]
wee1=[j for [i, j] in w1]
w2=d[win2]
vec2=[i for [i, j] in w2]
wee2=[j for [i, j] in w2]


#lost
w=''
nw=0
for j in range(2):
    for k, v in d.items():
        #print(k)
        n=0
        prev=v[0]
        for i in range(1, len(v)):
            att=v[i]

            n=att[0]-prev[0]
            if n>nw and k!=los1:
                nw=n
                w=k
            n=0
            prev=att


    nw=0
    if j==0:
        los1=w
    else:
        los2=w

#print('l1 ', los1, 'l2', los2)

#save data of two "lores" to show them separately
l1=d[los1]
vec1l=[i for [i, j] in l1]
wee1l=[j for [i, j] in l1]
l2=d[los2]
vec2l=[i for [i, j] in l2]
wee2l=[j for [i, j] in l2]


#delete the firt element \[0, 0\] or replace with \[1, 0\] used to star the line from 0 at the firs week
for v in d.values():
    if v[1][0]==1:
        v.pop(0)
    else:
        v[0][0]=1

#add the last element used to finish the line ad the 38th week
for v in d.values():
    if v[len(v)-1][0]!=38:
        v.append([38, v[len(v)-1][1]])


heigth=110
plt.axis([0, 39, 0, heigth]) #set the length of axis
plt.xticks(range(40), ['week '+str(i) for i in range(39)], rotation=30, fontsize='xx-small') #set the x-ticks, them text and other things
plt.yticks(list(range(0, heigth, 5))) #set the y-ticks

#we have to plot before the two winners and loosers
plt.plot(vec1, wee1, '*-',  label=win1)
plt.plot(vec2, wee2, '*-',  label=win2)
plt.plot(vec1l, wee1l, '*-', label=los1)
plt.plot(vec2l, wee2l, '*-', label=los2)
#cause we can remove them from dictionary and then print the remaining teams
del d[win1]
del d[win2]
del d[los1]
del d[los2]

#print of the remaining team
for k, v in d.items():
    #vector=[j for [i, j] in v]
    #week=[i for [i, j] in v]
    #print(k, v)
    plt.plot([i for [i, j] in v], [j for [i, j] in v], label=k)


#add legend
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

#save picture: the path and file name, the resolution, and the box to fit the image around legend and plot
plt.savefig('/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/matches/results', format='png', dpi=500, bbox_inches='tight')



plt.show()
