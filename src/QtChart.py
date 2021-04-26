import pandas as pd
import configparser
import os
from matplotlib import pyplot as plt

config = configparser.ConfigParser()
config.read('config.ini')

target = os.path.join('{0}'.format(config['Locations']['DataLocation']),'m_data.csv')

df = pd.read_csv(target)
df.set_index(config['DataFrame']['IndexColumn'], inplace=True)

print(df.to_string())