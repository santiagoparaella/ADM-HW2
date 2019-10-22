#This document was written by Santo Palaia (1st part) and Pooja (2nd part)

# First part --------------------------------------------------------------------
import json
import pandas as pd

#Load the joson files
event=pd.read_json(r'/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork2/Event/events_England.json')[['eventId', 'tags', 'playerId']]
pass_event_all=event.loc[event['eventId']==8] #only pass

#drop column eventId
pass_event_all.drop('eventId', axis=1, inplace=True) #we don't need eventId

myList=[]
for index, row in pass_event_all.iterrows():
    myList.append(1) if {'id':1801} in row['tags'] else myList.append(0) #create a list of 1 (pass compleate) and 0 (pass not totaly complete)

pass_event_all['pass']=myList #add this column
pass_event_all.drop('tags', axis=1, inplace=True) #we don't need tags

pass_event_final=pass_event_all.groupby('playerId').agg({'pass':['sum', 'count']}) #grouping on playerId and aggregating on sum(number of comlete pass) and count of total pass tried
pass_event_final.columns=['_'.join(col).strip() for col in pass_event_final.columns.values] #redefination of columns
pass_event_final=pass_event_final.reset_index() #reset the index

#we have 3 columuns and 3 keys.
#keys : 'playerId', 'pass_sum and pass_count.
#We can access with:
#    pass_event_final['playerId'] : the id pof the players
#    pass_event_final['pass_sum'] : the number of complete pass
#    pass_event_final['pass_count'] :  total number of pass tried

#print(pass_event_final['playerId'], '\n', pass_event_final['pass_sum'], '\n', pass_event_final['pass_count'])

# Second Part ------------------------------------------------------------------
