import sys
import os
import pandas as pd

curDir = os.path.abspath(os.getcwd())
srcDir = os.path.join(curDir,'src')
sys.path.append(curDir)
sys.path.append(srcDir)

import QtPDF

def main():
    df = pd.read_csv('data/m_data.csv')
    report = QtPDF.QtReport(df)
    report.generate()

main()