import os
import math
import configparser
import PyPDF2
import pandas as pd
from weasyprint import HTML,CSS
from weasyprint.fonts import FontConfiguration
from jinja2 import Environment, FileSystemLoader
from matplotlib import pyplot as plt
import QtUtils
import QtConfigure

class QtReport:

    def __init__( self , csv_file , * , report_file_name , airport_name ,way_name , agent_name , date_of_report , time_of_report ):
        #Configure the underlying settings
        QtConfigure.QtConfig()
        self.config = configparser.ConfigParser();
        self.config.read("config.ini")
        
        #Configure the DLL searc path the weasyprint module depends on 
        QtUtils.setDLLSearchPath()

        #Initialize report's parameters
        self.reportFileName = report_file_name
        self.airportName = airport_name
        self.wayName = way_name
        self.agentName = agent_name
        self.dateOfReport = date_of_report
        self.timeOfReport = time_of_report

        #Construct dataframe    
        self.df = pd.read_csv(csv_file)

        self.__transformDF()

        #config = configparser.ConfigParser()
        #config.read('config.ini')

    def __plot(self):
        light_ids = []

        for i in range(self.df.shape[0]):
            light_ids.append(i+1)

        avgs = []

        for _, row in self.df.iterrows():
            avgs.append(row['AVG(cd)'])

        x_ticks = []

        for i in range(0,self.df.shape[0],5):
            x_ticks.append(i)

        plt.xticks(ticks=x_ticks)
        plt.xlabel('Light ID')
        plt.ylabel('Average Candela (in cd)')
        plt.bar( light_ids , avgs )

        #config = configparser.ConfigParser()
        #config.read('config.ini')
        plot_path = os.path.join( self.config['Locations']['imagelocation'] , '{0}.png'.format(self.reportFileName) )
        
        #save the plot
        plt.savefig( plot_path , dpi=400 )
        #plt.show()

    def __transformDF(self):

       #Initialize values for new three columns
       data = [0 for i in range(self.df.shape[0])]

       #Insert three new columns 'AVG(cd)', 'Max(cd)' and '%ICAO'
       self.df.insert(1, 'AVG(cd)', data)
       self.df.insert(2, 'Max(cd)', data)
       self.df.insert(3, '%ICAO',data)

       #Drop column 'Timestamp'
       self.df.drop('Timestamp', inplace=True, axis=1) 

       #Compute the average and max across the Vs columns for each row
       self.df['AVG(cd)'] = self.df[['V1', 'V2','V3','V4','V5','V6','V7','V8']].mean(axis=1)
       self.df['Max(cd)'] = self.df[['V1', 'V2','V3','V4','V5','V6','V7','V8']].max(axis=1)

       #Drop the Vs columns
       self.df.drop(['V1', 'V2','V3','V4','V5','V6','V7','V8'], inplace=True, axis=1) 

       #Plot the barchart
       self.__plot()

    def __oneHTML( self , page_num , start_row , end_row ):
        #Get the entries for the current page
        cur_df = self.df.iloc[start_row:end_row+1] #end_row exclusive
        m_table = cur_df.to_html(index=False) 

        #config = configparser.ConfigParser()
        #config.read('config.ini')
        
        #Render each page 
        each_page =  self.template.render(
                                    m_table=m_table,
                                    page_no=page_num, 
                                    report_file_name=self.reportFileName,
                                    air_port_name=self.airportName,
                                    way_name=self.wayName,
                                    agent_name=self.agentName,
                                    date_of_report=self.dateOfReport,
                                    time_of_report=self.timeOfReport,
                                    plot_path='{0}.png'.format(self.reportFileName)
                                )
        #Export as HTML to the tmp folder specified by tempLocation in the config.ini file
        
        #Compute the name of the current HTML
        new_HTML_path = os.path.join( self.config['Locations']['templocation'] , '{0}-{1}.html'.format(self.reportFileName,page_num) )
        
        with open( new_HTML_path , "w" ) as html_file: 
            html_file.write(each_page)

        QtUtils.displayInfo('{0} was made...'.format(new_HTML_path))

        self.__onePDF(html_page=each_page,report_file_name=self.reportFileName,page_num=page_num)

    def __onePDF(self,*,html_page,report_file_name,page_num):
        #config = configparser.ConfigParser()
        #config.read('config.ini')
        
        new_PDF_path = os.path.join( self.config['Locations']['templocation'] , '{0}-{1}.pdf'.format(report_file_name,page_num) )

        HTML(string=html_page,base_url='.').write_pdf( new_PDF_path ) 

        QtUtils.displayInfo('{0} was made...'.format(new_PDF_path))

    def __mergePDFs(self):

        input_dir = self.config['Locations']['templocation']
        output_dir = self.config['Locations']['reportlocation']

        merge_list = []

        for file in os.listdir(input_dir):
            if file.endswith('.pdf') and file.startswith(self.reportFileName):
                merge_list.append(input_dir+os.sep+file)

        sorted(merge_list)

        merger = PyPDF2.PdfFileMerger()

        for pdf in merge_list:
            merger.append(pdf)

        merger.write(output_dir+os.sep+'{0}.pdf'.format(self.reportFileName)) 
        merger.close()

    def generate( self ):
        #config = configparser.ConfigParser()
        #config.read('config.ini')

        file_loader = FileSystemLoader(self.config['Locations']['templatelocation']) 
        env = Environment(loader=file_loader,trim_blocks=True)
        self.template = env.get_template('template.html') 

        #Get the total number of entries
        num_of_rows  = self.df.shape[0]
        #Calculate the number of pages based on the config where the number of entries per page is set
        num_of_pages = math.ceil(num_of_rows/int(self.config['ReportFormat']['numberofrowsperpage']))
        
        row = 0
        for page_num in range(1,num_of_pages+1):
            start_row = row
            end_row = start_row + int(self.config['ReportFormat']['numberofrowsperpage']) -1

            if end_row > num_of_rows:
                end_row = num_of_rows

            #Export the current page as HTML
            self.__oneHTML( page_num , start_row , end_row )

            row = end_row+1
            page_num += 1
        
        #Merge PDFs
        self.__mergePDFs()

#Test the module
if __name__ == '__main__':

    import datetime
    
    datetime_of_report = datetime.datetime.today()

    headerData = {  
                    'report_file_name':'07000178.pac',
                    'airport_name':'Betong International Airport',
                    'way_name':'RUNWAY EDGE - 07L',
                    'agent_name':'FBT_Sp',
                    'date_of_report': QtUtils.getDate(datetime_of_report),
                    'time_of_report': QtUtils.getTime(datetime_of_report)
                 }

    report = QtReport( 'C:\Workspace\Quintus\data\m_data.csv' , **headerData )
    report.generate()