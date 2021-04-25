import random
import datetime
import pandas as pd
import numpy as np

def random_date():
    current_datetime= datetime.datetime.now()
    random_datetime = current_datetime + random.random()*datetime.timedelta(minutes=1)
    return random_datetime

records = int(input('Enter the number of records to generate: '))

print('Generating {0} records...\n'.format(records))

columns =('LightID','Timestamp','V1','V2','V3','V4','V5','Distance','Color','Result')

possible_colors   =['W', 'R', 'B', 'G']
possible_outcomes =['Pass', 'Fail']

timestamps = []
lightids   = []
v1s = []
v2s = []
v3s = []
v4s = []
v5s = []
distances = []
colors = []
outcomes = []

#randomly generate records
for i in range(0, records):
    lightids.append(i+1)
    timestamps.append(random_date()) 
    v1s.append(random.uniform(40,50))
    v2s.append(random.uniform(40,50))
    v3s.append(random.uniform(40,50))
    v4s.append(random.uniform(40,50))
    v5s.append(random.uniform(40,50))
    distances.append(random.uniform(0.50,1.80))
    colors.append(np.random.choice(possible_colors,p=[0.25,0.25,0.25,0.25]))
    outcomes.append(np.random.choice(possible_outcomes,p=[0.95,0.05]))

#assemble columns 
data = {    columns[0]:lightids,
            columns[1]:timestamps,
            columns[2]:v1s,
            columns[3]:v2s,
            columns[4]:v3s,
            columns[5]:v4s,
            columns[6]:v5s,
            columns[7]:distances,
            columns[8]:colors,
            columns[9]:outcomes
       }

#construct data frame
df = pd.DataFrame(data,columns=columns)
pd.options.display.max_rows = records

#set 'LightID' as index
df.set_index(['LightID'],inplace=True)

#save data frame tp .csv file
df.to_csv('../data/m_data.csv',float_format='%.2f')
