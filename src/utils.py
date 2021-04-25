import os

def getPath(path):
    res = ''
    for c in path:
        res = res + c + os.sep
    return res 

def getDate(datetime):
    date = datetime.date().strftime('%d/%m/%Y')
    return date

def getTime(datetime):
    time = datetime.time().strftime('%H:%M:%S')
    return time

if __name__ == '__main__':

    #Test getPath()
    path = 'C:\\Workspace\\Quintus\\'
    print('\tPath: ',path)
    print('\tFull Path: ',os.path.join(path,__file__))