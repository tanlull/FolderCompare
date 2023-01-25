import os.path
import shutil
from ftplib import FTP
import datetime
import time
import settings
import os
import json
import numpy as np
from collections import Counter
import pickle
import zipfile
from datetime import datetime
from pprint import pprint
import ftplib as ftp


now = datetime.now()
datetimenow = now.strftime("%Y-%m-%d_%H-%M")

ftpserver = settings.ftpserver
ftplogin =  settings.ftplogin
ftppassword = settings.ftppassword
ftpport = settings.ftpport
pricefile = settings.pricefile #path to the file with price (price-list)
archpath = settings.archpath #archive folder for uploaded prices
ftppath = settings.ftppath #path on ftpserver to folder where need upload price
sleep = settings.sleep
sourceFolder = settings.sourceFolder
targetFolder = settings.targetFolder
logpath = settings.logPath
logAll = os.path.join(logpath,settings.logFile)
backupProcessPath = settings.backupProcessPath
pickleFiles = os.path.join(backupProcessPath,settings.pickleFiles)
pickleFolders = os.path.join(backupProcessPath,settings.pickleFolders)


def initial():
    createFolder(backupProcessPath)

def main():
    initial()
    # Find diff
    allFolders, rootFolders = findFolder2Backup()
    writeLog(logAll,getLogFilename(logpath),rootFolders,createZipFolder())

    # Zip list files
    zipBackupFiles = processZipFolders(rootFolders)
    
    # FTP 
    result = uploadList2FTP(zipBackupFiles,datetimenow)
    writeLogAll(result)
    #uploadFile2FTP(zipBackupFiles[0],datetimenow)
    #pprint(zipBackupFiles)

def writeLogAll(text):
    writeText2File(getLogFilename(logpath),text)
    writeText2File(logAll,text)

def connectFTP(ftpserver,ftpport,ftplogin,ftppassword):
    try:
        session = ftp.FTP()
        session.connect(ftpserver,int(ftpport))
        session.login(ftplogin,ftppassword)
        session.encoding = "utf-8"
        return session
    except IOError as e:
        import sys
        error_msg = "I/O error({0}): {1}".format(e.errno, e.strerror)
        writeLogAll(error_msg)
        print(error_msg)        
        sys.exit("Exit FTP Error")  



def closeFTP(session):
    session.quit()

def uploadList2FTP(myList,datetimenow):
    text = ""
    session = connectFTP(ftpserver,ftpport,ftplogin,ftppassword)
    ftpRemoteFolder = datetimenow

    try:
        session.mkd(ftpRemoteFolder)
    except ftp.error_perm:
        print("Directory "+ftpRemoteFolder+" already exists")
    
    for f in myList:
        text += uploadFile2FTP(session,f,ftpRemoteFolder)
    closeFTP(session)
    return text


def uploadFile2FTP(session,file2Upload,ftpRemoteFolder):
    file = open(file2Upload,'rb')                  # file to send
    text = ""
    fileNameOnly = getFileNamefromFullPath(file2Upload)
    session.storbinary('STOR '+os.path.join(ftpRemoteFolder,fileNameOnly), file)     # send the file
    file.close()                                    # close file and FTP
    result = "FTP: "+fileNameOnly+" => OK\n"
    text += result
    print(result)
    return text

def getFileNamefromFullPath(fullpath):
    file_name = os.path.basename(fullpath)
    #print(file_name)
    return file_name


def writeLog(logAll,filename,myList,header="Header"):    
    text = writeList2File(filename,myList,header)
    writeText2File(logAll,text)


def writeList2File(filename,myList,header="Header"):
    txt1 = "*****"
    text = txt1+header+txt1+"\n"
    for item in myList:
        text +=item+"\n"
    text += "\n"
    #text += txt1*15+"\n\n"
    writeText2File(filename,text)
    return text


def writeText2File(filename,text):
    f = open(filename,"a+")
    f.write(text)
    f.close()



def getLogFilename(logpath):
    createFolder(logpath)
    return os.path.join(logpath,datetimenow+".log")


def processZipFolders(folders):
    zipRootFolder = createZipFolder()
    zipFiles = []
    for f in folders:
        new_f = getZipFileName(f)
        #print(new_f)
        zipFileName=os.path.join(zipRootFolder,new_f+".zip")
        zipFolderAndSub(f,zipFileName)
        zipFiles.append(zipFileName)
    return zipFiles

def getZipFileName(zipFile):
    f = zipFile.replace("_", "-" )
    f = f.replace("\\", "_" )
    f = f.replace("C:", "" )
    f = f.replace("_", "",1 )
    return f

def createZipFolder():
    zipFolder = os.path.join(archpath,datetimenow)
    createFolder(zipFolder)
    #print(zipFolder)
    return zipFolder

def createFolder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def zipFolderAndSub(folder2Zip,zipfileName):
    zipf = zipfile.ZipFile(zipfileName, 'w', zipfile.ZIP_DEFLATED)
    zipdir(folder2Zip, zipf)
    zipf.close()

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def zipFolder(fileName2Zip,folder2Zip):
    with zipfile.ZipFile(fileName2Zip, 'w') as zipMe:        
        for file in folder2Zip:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

def findFolder2Backup():
    #print("ftpserver = "+ftpserver+",user = "+ftplogin)
    currentFolders, currentFiles = listAllFolder(sourceFolder)
    #folders, files = listAllFolder("C:\RPAShare")
    #print(files)
    #print(folders)  
    #dumpList(folders,files)
    oldFolders, oldFiles= LoadList()  # load from pickle
    #print(foldersPrev)
    newCreatedFolders = diffList(currentFolders,oldFolders)
    #print(newCreatedFolders)
    rootNewCreatedFolders = removeChildFolder(newCreatedFolders)
    #print(rootNewCreatedFolders)
    return newCreatedFolders,rootNewCreatedFolders

def removeChildFolder(folderList):
    folderListNew = folderList.copy()
    folder2Remove = []
    for dir1 in folderList:
        for dir2 in folderListNew:
            if dir1!=dir2 and dir1 in dir2:
                folder2Remove.append(dir2)    
    return diffList(folderList,folder2Remove) 
    

def diffList(newFolders,oldFolders):
    diff = list(set(newFolders) - set(oldFolders))
    diff_sorted = sorted(diff)
    return diff_sorted


def LoadList():
    folders = loadFile2List(pickleFolders)
    files = loadFile2List(pickleFiles)
    return folders,files

def dumpList(folders,files):
    dumpList2File(folders,pickleFolders)
    dumpList2File(files,pickleFiles)

def loadFile2List(myFilename):
    with open(myFilename, 'rb') as f:
        return pickle.load(f)
        

def dumpList2File(myList,myFilename):
    with open(myFilename, 'wb') as f:
        pickle.dump(myList, f)


def listAllFolder(path):
    folderStructureAll = []
    allFolders =[]
    allFiles = []
    for root, dirs, files in os.walk(path):
        mydict = {
            "dir": root,
            "subdir":dirs,
            "file":files
        }
        #print(root)

        # print(dirs)
        # print("subdir =".join(dirs))
        # print(files)

        folderStructureAll.append(mydict) # all folder structure

        allFolders.append(root)  # Root folder

        listFile = genFileformDict(root,files,"\\") # Generate full file path (C:\\xxx + yyy.txt)
        # print(listFile)
        allFiles.extend(listFile)


    #printDictDir(folderStructureAll,"dir")
    #print(allFolder)
    return allFolders,allFiles

def genFileformDict(base,files,seperator):
    resultfiles = []
    for f in files:
        if len(f): #ifnot empty
            resultfiles.append(base+seperator+f)    
    return resultfiles

def printDictDir(dict,key):
    for data in dict:
        print(data[key])

def printDict(dict):
    print(json.dumps(dict,sort_keys=False, indent=4))



if __name__ == '__main__':
    # while True:
    #     main()
    #     time.sleep(sleep)
    main()
