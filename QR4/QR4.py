#This document was written by Santo Palaia (1st part) and Pooja (2nd part)

# First part --------------------------------------------------------------------
import json
import pandas as pd

#Load the joson files
event=pd.read_json(r'/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/Event/events_England.json')[['eventId', 'tags', 'playerId']]
pass_event_all=event.loc[event['eventId']==8]

#drop column eventId
pass_event_all.drop('eventId', axis=1, inplace=True)

myList=[]
for index, row in pass_event_all.iterrows():
    myList.append(1) if {'id':1801} in row['tags'] else myList.append(0)

pass_event_all['pass']=myList
pass_event_all.drop('tags', axis=1, inplace=True)

pass_event_final=pass_event_all.groupby('playerId').agg({'pass':['sum', 'count']})
pass_event_final.columns=['_'.join(col).strip() for col in pass_event_final.columns.values]
pass_event_final=pass_event_final.reset_index()

#we have 3 columuns and 3 keys.
#keys : 'playerId', 'pass_sum and pass_count.
#We can access with:
#    pass_event_final['playerId'] : the id pof the players
#    pass_event_final['pass_sum'] : the number of complete pass
#    pass_event_final['pass_count'] :  total number of pass tried

#print(pass_event_final['playerId'], '\n', pass_event_final['pass_sum'], '\n', pass_event_final['pass_count'])

# Second Part ------------------------------------------------------------------
