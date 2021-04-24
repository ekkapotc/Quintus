import pandas as pd

def read_csv(path):
    df = pd.read_csv(path)
    df.set_index('LightID',inplace=True)
    #print(df.to_string())
    return df

#test
if __name__ == '__main__':
    df = read_csv('../data/m_data.csv')
    print(df.to_string())
    print(df.to_html())