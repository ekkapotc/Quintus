import os
import configparser
import QtUtils

class QtConfig:

    __SUCCESS = 1           #TO-DO
    __FAILURE = (1 << 2)    #TO-DO  

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
        #Create a config.ini file if one does not exist
        if not os.path.exists('config.ini'):
            #Instantiate a config parser
            config = configparser.ConfigParser()
            #Intialize key paths
            img_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['img'])
            data_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['data'])
            tmp_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['tmp'])
            report_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['report'])
            template_folder = os.path.join(QtUtils.getPath(self.rootPath), QtConfig.__directories['templates'])

            #Define sections in the config file
            config['Locations'] = {'imageLocation': img_folder,
                             'dataLocation':  data_folder,
                             'tempLocation':  tmp_folder,
                             'reportLocation': report_folder,
                             'templateLocation': template_folder,
                            }
            config['DataFrame']    = {'indexColumn':'LightID'}
            config['ReportFormat'] = {'numberOfRowsPerPage':15}

            with open('config.ini', 'w') as config_file:
                config.write(config_file)

            QtUtils.displayInfo('config.ini was made...')
        else:
            QtUtils.displayInfo('config.ini already exists so nothing was done...')

    def __init__(self):
        #Initialize config file
        self.__createConfigFile()
        