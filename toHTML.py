
import pandas as pd
import datetime
from jinja2 import Environment, FileSystemLoader

import readmCSV

def dfToHTML(df,*,page_no,report_file_name,way_name,agent):

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader,trim_blocks=True)

    template = env.get_template('template.html')
    m_table = df.to_html() #default class = dataframe
    m_page =  template.render(m_table=m_table,
                                page_no=page_no,
                                report_file_name=report_file_name,
                                way_name=way_name,
                                agent=agent)

    with open('report/{0}-{1}.html'.format(report_file_name,page_no), "w") as o_file:
        o_file.write(m_page)

#test
if __name__ == '__main__':
    try:
        df = readmCSV.read_csv('data/m_data.csv')
    except Exception as e:
        print(e)
    try:
        meta_data = {   'page_no':1 , 
                        'report_file_name':'07000178.pac',
                        'way_name':'RUNWAY EDGE - 07L',
                        'agent':'FBT_Sp'}
        dfToHTML(df,**meta_data)
    except Exception as e:
        print(e)