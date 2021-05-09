import random
import datetime
import pandas as pd
import numpy as np

def random_date():
    current_datetime= datetime.datetime.now()
    random_datetime = current_datetime + random.random()*datetime.timedelta(minutes=1)
    return random_datetime.replace(microsecond=0)

records = int(input('Enter the number of records to generate: '))

print('Generating {0} records...\n'.format(records))

columns =('Timestamp','Airport','Way Name','Light ID','v1','v2','v3','v4','v5','v6','v7','v8','Distance','C','S')

possible_colors   =['G', 'W', 'R', 'Y']
possible_outcomes =['Pass', 'Fail']

timestamps = []
lightids   = []
v1s = []
v2s = []
v3s = []
v4s = []
v5s = []
v6s = []
v7s = []
v8s = []
distances = []
colors = []
outcomes = []
airports = []
waynames = []

#randomly generate records
for i in range(0, records):
    airports.append('BETONG INTERNATIONAL AIRPORT')
    waynames.append('RUNWAY EDGE - 07L')
    lightids.append(i+1)
    timestamps.append(random_date()) 
    v1s.append(random.uniform(8,22))
    v2s.append(random.uniform(8,22))
    v3s.append(random.uniform(8,22))
    v4s.append(random.uniform(8,22))
    v5s.append(random.uniform(8,22))
    v6s.append(random.uniform(8,22))
    v7s.append(random.uniform(8,22))
    v8s.append(random.uniform(8,22))
    distances.append(random.uniform(0.50,1.80))
    colors.append(np.random.choice(possible_colors,p=[0.25,0.25,0.25,0.25]))
    outcomes.append(np.random.choice(possible_outcomes,p=[0.95,0.05]))

#assemble columns 
data = {    columns[0]:timestamps,
            columns[1]:airports,
            columns[2]:waynames,
            columns[3]:lightids,
            columns[4]:v1s,
            columns[5]:v2s,
            columns[6]:v3s,
            columns[7]:v4s,
            columns[8]:v5s,
            columns[9]:v6s,
            columns[10]:v7s,
            columns[11]:v8s,
            columns[12]:distances,
            columns[13]:colors,
            columns[14]:outcomes
       }

#construct data frame
df = pd.DataFrame(data,columns=columns)
pd.options.display.max_rows = records

#set 'LightID' as index
df.set_index(['Light ID'],inplace=True)

#save data frame tp .csv file
#note this code works only when the python script QtRandCSV.py is called from this folder.
df.to_csv('../data/m_data.csv',float_format='%.2f')
