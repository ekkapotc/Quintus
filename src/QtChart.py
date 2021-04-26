import pandas as pd
import numpy as np
import configparser
import os
from matplotlib import pyplot as plt

config = configparser.ConfigParser()
config.read('config.ini')

target = os.path.join('{0}'.format(config['Locations']['DataLocation']),'m_data.csv')

df = pd.read_csv(target)
df.set_index(config['DataFrame']['IndexColumn'], inplace=True)

new_df = df.loc[:,['V1','V2','V3','V4','V5','V6','V7','V8']]
     
new_df['V_avg'] = 0.0
new_df['V_max'] = 0.0

light_ids = []

for i in range(new_df.shape[0]):
    light_ids.append(i+1)

avgs = []

for index, row in new_df.iterrows():
    elems = []
    #for col in range(8):
    for col in ['V1','V2','V3','V4','V5','V6','V7','V8']:
        elems.append(row[col])

    avg = np.average(elems)
    avgs.append(avg)
    new_df.loc[index,['V_avg']] = avg
    new_df.loc[index,['V_max']] = np.max(elems)

x_ticks = []

for i in range(0,new_df.shape[0],5):
    x_ticks.append(i)

plt.xticks(ticks=x_ticks)
plt.xlabel('Light ID')
plt.ylabel('Average Candela (in Kcd)')
plt.bar( light_ids,avgs )
plt.savefig('../img/barchart.png',dpi=400)
plt.show()