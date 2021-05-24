import sys
import os
import pandas as pd

curDir = os.path.abspath(os.getcwd())
srcDir = os.path.join(curDir,'src')
sys.path.append(curDir)
sys.path.append(srcDir)

import QtPDF

def main():

    headerData = {  
                    'report_file_name':'07000178.pac',
                    'airport_name':'Betong International Airport',
                    'way_name':'RUNWAY EDGE - 07L',
                    'agent_name':'FBT_Sp'
    }

    df = pd.read_csv('data/m_data.csv')
    report = QtPDF.QtReport(df,**headerData)
    report.generate()

main()