import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import math

class Config:
    csvLocation = '../data'
    csvName = 'm_data.csv'
    templateLocation = '../templates'
    templateName = 'template.html'
    reportLocation = '../report'
    numberOfRowsPerPage = 15
    dataframeIndexColumn = 'LightID'

class Report:

    def __init__( self , csv_file , * , report_file_name , airport_name ,way_name , agent_name ):
        #Initialize report's parameters
        self.reportFileName = report_file_name
        self.airportName = airport_name
        self.wayName = way_name
        self.agentName = agent_name

        #Construct dataframe    
        self.df = pd.read_csv(csv_file)
        self.df.set_index(Config.dataframeIndexColumn,inplace=True)

    def __oneHTML( self , page_num , start_row , end_row ):
        #Get the entries for the current page
        cur_df = self.df.loc[start_row:end_row]
        m_table = cur_df.to_html() 
        #Render each page 
        each_page =  self.template.render(
                                    m_table=m_table,
                                    page_no=page_num+1, 
                                    report_file_name=self.reportFileName,
                                    air_port_name=self.airportName,
                                    way_name=self.wayName,
                                    agent=self.agentName
                                )
        #Export as HTML
        with open( os.path.join( Config.reportLocation , '{0}-{1}.html'.format(self.reportFileName,page_num+1) ) , "w" ) as html_file: 

            html_file.write(each_page)

    def toHTML( self ):
        file_loader = FileSystemLoader(Config.templateLocation) 
        env = Environment(loader=file_loader,trim_blocks=True)
        self.template = env.get_template(Config.templateName) 

        #Get the total number of entries
        num_of_rows  = self.df.shape[0]
        #Calculate the number of pages based on the config where the number of entries per page is set
        num_of_pages = math.ceil(num_of_rows/Config.numberOfRowsPerPage)
        
        row = 1
        
        for page_num in range(num_of_pages):
            start_row = row
            end_row = start_row + Config.numberOfRowsPerPage-1

            if end_row > num_of_rows:
                end_row = num_of_rows

            self.__oneHTML( page_num , start_row , end_row )

            row = end_row+1
            page_num += 1

#Test the module
if __name__ == '__main__':

    metaData = {'report_file_name':'07000178.pac',
                'airport_name':'Betong International Airport',
                'way_name':'RUNWAY EDGE - 07L',
                'agent_name':'FBT_Sp'
               }

    report = Report( os.path.join( Config.csvLocation , Config.csvName ) , **metaData )
    report.toHTML()

    
