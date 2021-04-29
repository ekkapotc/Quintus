import configparser 
from PyPDF2 import PdfFileMerger
from os import listdir

config = configparser.ConfigParser()
config.read('config.ini')

input_dir = config['Locations']['reportlocation']

merge_list = []

for x in listdir(input_dir):
    if not x.endswith('.pdf'):
        continue
    merge_list.append(input_dir + x)

merger = PdfFileMerger()

for pdf in merge_list:
    merger.append(pdf)

merger.write(input_dir+"merged_pdf.pdf") #your output directory
merger.close()