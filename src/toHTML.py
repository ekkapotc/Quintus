import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import math
import configparser
import utils

class QConfig:
    
    csvLocation = '../data'
    csvName = 'm_data.csv'
    templateLocation = '../templates'
    templateName = 'template.html'
    reportLocation = '../report'
    numberOfRowsPerPage = 15
    dataframeIndexColumn = 'LightID'
    tempLocation = '../tmp'

    __directories = ['img','data','tmp','report'] 

    def __getCurPathInfo(self):
        #Get path components of the current path
        pathComponents = os.path.realpath(__file__).split(os.sep) 
        #Compute path info
        self.fileName  = pathComponents.pop()
        self.curFolder = pathComponents.pop()
        self.rootPath = pathComponents

    def __init__(self):
        #Get current working directory
        self.__getCurPathInfo()

        for directory in QConfig.__directories:
            #Compute target directory
            target = os.path.join(utils.getPath(self.rootPath),directory)
            #Check if the tmp folder  already exists
            if not os.path.exists(target):
                os.makedirs(target)

class QReport:

    def __init__( self , csv_file , * , report_file_name , airport_name ,way_name , agent_name ):
        #Initialize the config object
        self.config = QConfig()

        #Initialize report's parameters
        self.reportFileName = report_file_name
        self.airportName = airport_name
        self.wayName = way_name
        self.agentName = agent_name

        #Construct dataframe    
        self.df = pd.read_csv(csv_file)
        self.df.set_index(QConfig.dataframeIndexColumn,inplace=True)

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
        #Export as HTML to the tmp folder specified by QConfig.tempLocation
        with open( os.path.join( QConfig.tempLocation , '{0}-{1}.html'.format(self.reportFileName,page_num+1) ) , "w" ) as html_file: 
            html_file.write(each_page)

    def toHTML( self ):
        file_loader = FileSystemLoader(QConfig.templateLocation) 
        env = Environment(loader=file_loader,trim_blocks=True)
        self.template = env.get_template(QConfig.templateName) 

        #Get the total number of entries
        num_of_rows  = self.df.shape[0]
        #Calculate the number of pages based on the config where the number of entries per page is set
        num_of_pages = math.ceil(num_of_rows/QConfig.numberOfRowsPerPage)
        
        row = 1
        for page_num in range(num_of_pages):
            start_row = row
            end_row = start_row + QConfig.numberOfRowsPerPage-1

            if end_row > num_of_rows:
                end_row = num_of_rows

            #Export the current page as HTML
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

    report = QReport( os.path.join( QConfig.csvLocation , QConfig.csvName ) , **metaData )
    report.toHTML()
    

    