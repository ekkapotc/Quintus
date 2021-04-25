import os
import logging

def getPath(path):
    res = ''
    for c in path:
        res = res + c + os.sep
    return res 

def getDate(datetime):
    date = datetime.date().strftime('%d/%m/%Y')
    return date

def logRuntimeInfo(orig_func):
    logging.basicConfig(filename='runtime.log'.format(orig_func.__name__), level=logging.INFO)

    def logRuntimeInfoWrapper(*args, **kwargs):
        logging.info(
            'Ran with args: {}, and kwargs: {}'.format(args, kwargs)
        )
        return orig_func(*args, **kwargs)

    return logRuntimeInfoWrapper

def getTime(datetime):
    time = datetime.time().strftime('%H:%M:%S')
    return time

@logRuntimeInfo
def displayInfo(msg):
    pass

if __name__ == '__main__':

    #Test getPath()
    path = 'C:\\Workspace\\Quintus\\'
    print('\tPath: ',path)
    print('\tFull Path: ',os.path.join(path,__file__))