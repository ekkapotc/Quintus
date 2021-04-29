import os
import configparser 
import PyPDF2

config = configparser.ConfigParser()
config.read('config.ini')

input_dir = config['Locations']['templocation']
output_dir = config['Locations']['reportlocation']

merge_list = []

for x in os.listdir(input_dir):
    if not x.endswith('.pdf'):
        continue
    merge_list.append(input_dir +os.sep+x)

sorted(merge_list)

merger = PyPDF2.PdfFileMerger()

for pdf in merge_list:
    merger.append(pdf)

merger.write(output_dir+os.sep+"FinalReport.pdf") #your output directory
merger.close()