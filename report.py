import pandas as pd

class Report{
    def __init__(self,csvFile):
        self.df = pd.read_csv(csvFile)
        self.df.set_index('LightID',inplace=True)

    def toHTML( self, *, page_no, report_file_name, way_name, agent ){
    
    }
}