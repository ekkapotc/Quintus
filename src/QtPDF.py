import os
import math
import configparser
import datetime

import pandas as pd

from jinja2 import Environment, FileSystemLoader

from matplotlib import pyplot as plt

import PyPDF2
from weasyprint import HTML,CSS
from weasyprint.fonts import FontConfiguration

import QtUtils
import QtConfigure

class QtReport:

    def __init__(self , df , * , report_file_name , agent_name , airport_name , way_name ):
        #Configure the underlying settings
        QtConfigure.QtConfig()
        self.config = configparser.ConfigParser();
        self.config.read("QtConfig.ini")
        
        self.reportFileName = report_file_name
        self.agentName = agent_name
        self.airportName = airport_name
        self.wayName = way_name
        
        #Configure the DLL searc path the weasyprint module depends on 
        QtUtils.setDLLSearchPath()

        #Initialze a list for keeping track of the individual pdf files generated 
        self.pdfNames = []
        #Store dataframe
        self.df = df;
        #Transform dataframe
        self.__transformDF()

    def __transformDF(self):

        #Initialize values for new three columns
        data = [0 for i in range(self.df.shape[0])]

        #Insert three new columns 'AVG(cd)', 'Max(cd)'
        self.df.insert(1, 'AVG(cd)', data)
        self.df.insert(2, 'Max(cd)', data)

        #Drop columns 'Timestamp' , 'Airport' and 'Way Name'
        self.df.drop(['Timestamp','Airport','Way Name'], inplace=True, axis=1) 
      
        #Compute the average and max across the Vs columns for each row
        self.df['AVG(cd)'] = self.df[['v1', 'v2','v3','v4','v5','v6','v7','v8']].mean(axis=1)
        self.df['Max(cd)'] = self.df[['v1', 'v2','v3','v4','v5','v6','v7','v8']].max(axis=1)

        #Drop columns 'v1','v2',...,'v8'
        self.df.drop(['v1', 'v2','v3','v4','v5','v6','v7','v8'], inplace=True, axis=1) 

    def __plot(self , cur_df , page_num , start_row , end_row ):
        
        light_ids = list(range(start_row+1,end_row+2))

        avgs = []
        icaos = []

        for _, row in cur_df.iterrows():
            avgs.append(row['AVG(cd)'])
            icaos.append(row['%ICAO'])

        colors = []

        for i, row in cur_df.iterrows():
            if row['C'] == 'R':
                colors.append('red')
            elif row['C'] == 'Y':
                colors.append('orange')
            elif row['C'] == 'W':
                colors.append('yellow')
            elif row['C'] == 'G':
                colors.append('green')
            else:
                colors.append('grey')

        #List light ids as x-ticks on the x-axis
        xticks = range(light_ids[0],light_ids[-1]+1,2)

        diff = self.num_rows_per_page - len(light_ids)

        #Fill in hiden dummy values
        if diff > 0:
            for i in range(light_ids[-1]+1,light_ids[-1]+diff+1):
                light_ids.append(i)
                avgs.append(0.0)
                icaos.append(0.0)

        width = 1.0;

        red_bars = []

        idx = 0
        for icao in icaos:
            if idx < cur_df.shape[0]:
                if icao < 50.0:
                    red_bars.append(avgs[idx]+500)
                else:
                    red_bars.append(0.0)
            else:
                red_bars.append(0.0)
                
            idx = idx+1

        #Set outer background color
        plt.figure(facecolor='#9d9d9e')
        #Set inner background color
        plt.axes().set_facecolor('#9d9d9e')

        #Draw a horizontal grid
        plt.gca().yaxis.grid()
        plt.gca().set_axisbelow(True)

        plt.xticks(xticks)
        plt.xlabel('Light ID')
        plt.ylabel('Average Candela (Cd)')

        plt.bar( x=light_ids , height=red_bars, width=width, color='#9d9d9e' , edgecolor='red'  )
        plt.bar( x=light_ids , height=avgs , width=width*.5, color=colors  )

        plot_path = os.path.join( self.config['Locations']['templocation'] , '{0}-{1}.png'.format(self.reportFileName,page_num))

        #save the plot
        plt.savefig( plot_path , dpi=400  )
        plt.close()

    def __generateOnePDF( self , page_num , start_row , end_row ):

        #Get the entries for the current page
        cur_df = self.df.iloc[start_row:end_row+1] #end_row exclusive

        #Draw a bar chart
        self.__plot(cur_df, page_num,start_row,end_row)

        #Convert the dataframe into an HTML table, excluding the index column
        m_table = cur_df.to_html(index=False) 

        datetime_of_report = datetime.datetime.today()

        #Render each page 
        each_page =  self.template.render(
                                    m_table=m_table,
                                    page_no=page_num, 
                                    report_file_name=self.reportFileName,  
                                    air_port_name=self.airportName,
                                    way_name=self.wayName,
                                    agent_name=self.agentName,  
                                    date_of_report=QtUtils.getDate(datetime_of_report),
                                    time_of_report=QtUtils.getTime(datetime_of_report),
                                    plot_path='{0}-{1}.png'.format(self.reportFileName,page_num)   
                                )
        
        self.pdfNames.append('{0}-{1}.pdf'.format(self.reportFileName,page_num))

        #Compute the name of the current HTML
        new_HTML_path = os.path.join( self.config['Locations']['templocation'] , '{0}-{1}.html'.format(self.reportFileName,page_num) ) 
        
        with open( new_HTML_path , "w" , encoding="utf-8") as html_file: 
            html_file.write(each_page)

        QtUtils.displayInfo('{0} was made...'.format(new_HTML_path))

        self.__onePDF( html_page=each_page , page_num=page_num )

    def __onePDF(self,*,html_page,page_num):
      
        new_PDF_path = os.path.join( self.config['Locations']['templocation'] , '{0}-{1}.pdf'.format(self.reportFileName,page_num) )

        #Set base url to img folder
        HTML(string=html_page,base_url='img').write_pdf( new_PDF_path ) 

        QtUtils.displayInfo('{0} was made...'.format(new_PDF_path))

    def __mergePDFs(self):

        input_dir = self.config['Locations']['templocation']
        output_dir = self.config['Locations']['reportlocation']

        merge_list = []

        for f in os.listdir(input_dir):
            if f in self.pdfNames:
                merge_list.append(os.path.join(input_dir,f))

        sorted(merge_list)

        merger = PyPDF2.PdfFileMerger()

        for f in merge_list:
            merger.append(f)

        merger.write(os.path.join(output_dir,'{0}.pdf'.format(self.reportFileName))) 
        merger.close()

    def generate( self ):

        file_loader = FileSystemLoader(self.config['Locations']['templatelocation']) 
        env = Environment(loader=file_loader,trim_blocks=True)
        self.template = env.get_template('template.html') 

        #Get the total number of entries
        num_of_rows  = self.df.shape[0]
    
        #Get the number of rows per page
        self.num_rows_per_page = int(self.config['ReportFormat']['numberofrowsperpage'])

        #Calculate the number of pages based on the config where the number of entries per page is set
        num_of_pages = math.ceil(num_of_rows/self.num_rows_per_page)
        
        row = 0
        for page_num in range(1,num_of_pages+1):
            start_row = row
            end_row = start_row + self.num_rows_per_page -1

            if end_row > num_of_rows-1:
                end_row = num_of_rows-1

            #Export the current page as HTML
            self.__generateOnePDF( page_num , start_row , end_row )

            row = end_row+1

        #Merge PDFs
        self.__mergePDFs()

        #Delete temp files
        dir = self.config['Locations']['templocation']
        for f in os.listdir(dir):
           os.remove(os.path.join(dir, f))

      
    
