import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import math
import configparser
import datetime
import utils
import configure



class QReport:

    def __init__( self , csv_file , * , report_file_name , airport_name ,way_name , agent_name , date_of_report , time_of_report ):
        #Configure the underlying settings
        configure.QConfig()

        #Initialize report's parameters
        self.reportFileName = report_file_name
        self.airportName = airport_name
        self.wayName = way_name
        self.agentName = agent_name
        self.dateOfReport = date_of_report
        self.timeOfReport = time_of_report

        #Construct dataframe    
        self.df = pd.read_csv(csv_file)
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.df.set_index(config['DataFrame']['indexColumn'],inplace=True)

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
                                    agent_name=self.agentName,
                                    date_of_report=self.dateOfReport,
                                    time_of_report=self.timeOfReport
                                )
        #Export as HTML to the tmp folder specified by tempLocation in the config.ini file
        config = configparser.ConfigParser()
        config.read('config.ini')
        with open( os.path.join( config['Locations']['templocation'] , '{0}-{1}.html'.format(self.reportFileName,page_num+1) ) , "w" ) as html_file: 
            html_file.write(each_page)

    def toHTML( self ):
        config = configparser.ConfigParser()
        config.read('config.ini')

        file_loader = FileSystemLoader(config['Locations']['templatelocation']) 
        env = Environment(loader=file_loader,trim_blocks=True)
        self.template = env.get_template('template.html') 

        #Get the total number of entries
        num_of_rows  = self.df.shape[0]
        #Calculate the number of pages based on the config where the number of entries per page is set
        num_of_pages = math.ceil(num_of_rows/int(config['ReportFormat']['numberofrowsperpage']))
        
        row = 1
        for page_num in range(num_of_pages):
            start_row = row
            end_row = start_row + int(config['ReportFormat']['numberofrowsperpage']) -1

            if end_row > num_of_rows:
                end_row = num_of_rows

            #Export the current page as HTML
            self.__oneHTML( page_num , start_row , end_row )

            row = end_row+1
            page_num += 1

#Test the module
if __name__ == '__main__':
    datetime_of_report = datetime.datetime.today()
    headerData = {  
                    'report_file_name':'07000178.pac',
                    'airport_name':'Betong International Airport',
                    'way_name':'RUNWAY EDGE - 07L',
                    'agent_name':'FBT_Sp',
                    'date_of_report': utils.getDate(datetime_of_report),
                    'time_of_report': utils.getTime(datetime_of_report)
                 }

    report = QReport( 'C:\Workspace\Quintus\data\m_data.csv' , **headerData )
    report.toHTML()