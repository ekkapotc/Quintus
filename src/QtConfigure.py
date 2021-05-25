import os
import configparser
import QtUtils

class QtConfig:

    __directories = {
                        'img':'img',
                        'data':'data',
                        'tmp':'tmp',
                        'report':'report',
                        'templates':'templates',
                     } 

    def __initPaths(self):
        #Get path components of the current path
        pathComponents = os.path.realpath(__file__).split(os.sep) 
        #Compute path info
        self.fileName  = pathComponents.pop()
        self.curFolder = pathComponents.pop()
        self.rootPath = pathComponents
        
        for directory in QtConfig.__directories:
            #Compute target directory
            target = os.path.join(QtUtils.getPath(self.rootPath),directory)
            #Check if the tmp folder  already exists
            if not os.path.exists(target):
                os.makedirs(target)
                QtUtils.displayInfo('{0} was made...'.format(directory))
            else:
                QtUtils.displayInfo('{0} already exists so nothing was done...'.format(directory))

    def __createConfigFile(self):
        #Get path components of the current path
        self.__initPaths()
        #Create a QtConfig.ini file if one does not exist
        if not os.path.exists('QtConfig.ini'):
            #Instantiate a config parser
            config = configparser.ConfigParser()
            #Intialize key paths
            img_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['img'])
            data_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['data'])
            tmp_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['tmp'])
            report_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['report'])
            template_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['templates'])

            #Define sections in the config file
            config['Locations'] = {
                                'imageLocation': img_folder,
                                'dataLocation':  data_folder,
                                'tempLocation':  tmp_folder,
                                'reportLocation': report_folder,
                                'templateLocation': template_folder,
                            }
            config['DataFrame']    = {'indexColumn':'LightID'}
            config['ReportFormat'] = {'numberOfRowsPerPage':15}
            config['BarChartFormat'] = {'widthOfOneBar':1.0}

            with open('QtConfig.ini', 'w') as config_file:
                config.write(config_file)

            QtUtils.displayInfo('QtConfig.ini was made...')
        else:
            QtUtils.displayInfo('QtConfig.ini already exists so nothing was done...')

    def __init__(self):
        #Initialize config file
        self.__createConfigFile()

#Test QtConfig 
if __name__ == '__main__':
    
    QtConfig()
        