import os
import math
import configparser
import datetime
from numpy import average

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
        
        #Configure the DLL searc path the weasyprint module depends on 
        QtUtils.setDLLSearchPath()

        #Configure the underlying settings
        QtConfigure.QtConfig()

        self.config = configparser.ConfigParser();
        self.config.read("QtConfig.ini")
        
        self.reportFileName = report_file_name
        self.agentName = agent_name
        self.airportName = airport_name
        self.wayName = way_name
        
        #Initialze a list for keeping track of the individual pdf files generated 
        self.pdfNames = []
        #Store dataframe
        self.df = df
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

    def __plot(self , cur_df , page_no , start_row , end_row ):
        
        light_ids = list(range(start_row+1,end_row+2))

        average_values = []
        ICAOs = []

        for _ , row in cur_df.iterrows():
            average_values.append(row['AVG(cd)'])
            ICAOs.append(row['%ICAO'])

        colors = []

        for _ , row in cur_df.iterrows():
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
                average_values.append(0.0)
                ICAOs.append(0.0)

        red_values = []
        edge_colors = []
        line_widths = []

        for row , val in enumerate(ICAOs):
            if row < cur_df.shape[0]:
                if val < 50.0:
                    red_values.append(average_values[row]+500)
                    edge_colors.append('red')
                    line_widths.append(1.0)
                else:
                    red_values.append(0.0)
                    edge_colors.append('white')
                    line_widths.append(0.0)
            else:
                red_values.append(0.0)  
                edge_colors.append('white')
                line_widths.append(0.0)
           
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

        width = float(self.config['BarChartFormat']['widthofonebar'])
        
        plt.bar( x=light_ids , height=red_values  , width=width, color='#9d9d9e' , edgecolor=edge_colors , linewidth=line_widths )
        plt.bar( x=light_ids , height=average_values , width=width*0.50, color=colors  )

        save_as = os.path.join( self.config['Locations']['templocation'] , '{0}-{1}.png'.format(self.reportFileName,page_no))

        #save the plot
        plt.savefig( save_as , dpi=400  )
        plt.close()

    def __generateOnePDF( self , page_no , start_row , end_row ):

        #Get the entries for the current page
        cur_df = self.df.iloc[start_row:end_row+1] #end_row exclusive

        #Draw a bar chart
        self.__plot(cur_df, page_no, start_row, end_row)

        #Convert the dataframe into an HTML table, excluding the index column
        m_table = cur_df.to_html(index=False) 

        datetime_of_report = datetime.datetime.today()

        #Render each page 
        html_page =  self.template.render(
                                    m_table=m_table,
                                    page_no=page_no, 
                                    report_file_name=self.reportFileName,  
                                    air_port_name=self.airportName,
                                    way_name=self.wayName,
                                    agent_name=self.agentName,  
                                    date_of_report=QtUtils.getDate(datetime_of_report),
                                    time_of_report=QtUtils.getTime(datetime_of_report),
                                    plot_path='{0}-{1}.png'.format(self.reportFileName,page_no)   
                                )
        
        self.pdfNames.append('{0}-{1}.pdf'.format(self.reportFileName,page_no))

        #Compute the name of the current HTML
        save_as = os.path.join( self.config['Locations']['templocation'] , '{0}-{1}.html'.format(self.reportFileName,page_no) ) 
        
        with open( save_as , 'w' , encoding='utf-8') as html_file: 
            html_file.write(html_page)

        QtUtils.displayInfo('{0} was made...'.format(save_as))

        self.__onePDF( html_page=html_page , page_no=page_no )

    def __onePDF(self,*,html_page,page_no):
      
        save_as = os.path.join( self.config['Locations']['templocation'] , '{0}-{1}.pdf'.format(self.reportFileName,page_no) )

        #Set base url to img folder
        HTML(string=html_page,base_url='img').write_pdf(save_as) 

        QtUtils.displayInfo('{0} was made...'.format(save_as))

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

        save_as = os.path.join(output_dir,'{0}.pdf'.format(self.reportFileName))
        merger.write(save_as) 
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
        for page_no in range(1,num_of_pages+1):
            start_row = row
            end_row = start_row + self.num_rows_per_page -1

            if end_row > num_of_rows-1:
                end_row = num_of_rows-1

            #Export the current page 
            self.__generateOnePDF( page_no , start_row , end_row )

            row = end_row+1

        #Merge PDFs
        self.__mergePDFs()

        #Delete temp files
        dir = self.config['Locations']['templocation']
        for f in os.listdir(dir):
           os.remove(os.path.join(dir,f))

      
    
