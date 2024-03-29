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
archpath = settings.archpath #archive folder for uploaded prices
ftppath = settings.ftppath #path on ftpserver to folder where need upload price
sleep = settings.sleep
sourceFolder = settings.sourceFolder
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

    currentFolders, currentFiles, allNewFolders, rootNewFolders = findFolder2Backup(sourceFolder)
   
    writeLogHeader(logAll,getLogFilename(logpath),rootNewFolders,createZipFolder())

    # Process Backup only found new Folder (diff folder)
    if rootNewFolders: 
        saveList2PickleFile(currentFolders,currentFiles)
        # Zip list files
        zipBackupFiles = processZipFolders(rootNewFolders)
        # FTP 
        result = uploadList2FTP(zipBackupFiles,datetimenow)
        writeLogAll(result)
    else : 
        writeLogAll("No Folder to Backup\n\n")
    
    #uploadFile2FTP(zipBackupFiles[0],datetimenow)
    #pprint(zipBackupFiles)

def saveList2PickleFile(currentFolders,currentFiles):
    #get backup name
    backupPickleFolders = os.path.join(settings.backupProcessPath,datetimenow+"."+settings.pickleFolders)
    #backupPickleFiles  = os.path.join(settings.backupProcessPath,datetimenow+"."+settings.pickleFiles)
    try:    
        os.rename(pickleFolders,backupPickleFolders) # backup 
    except:
        writeLogAll("Pickle Not found :"+pickleFolders+"\n")
    dumpList2File(currentFolders,pickleFolders) # save folders.pickle

    # os.rename(pickleFiles,backupPickleFiles)    
    # dumpList2File(currentFiles,pickleFiles) # files.pickle




def writeLogAll(text):
    writeText2File(getLogFilename(logpath),text)
    writeText2File(logAll,text)

def connectFTP(ftpserver,ftpport,ftplogin,ftppassword):
    try:
        session = ftp.FTP()
        session.connect(ftpserver,int(ftpport))
        session.login(ftplogin,ftppassword)
        session.encoding = "utf-8"
        print("FTP Connect => Success")
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
    print("Upload zip to FTP...")
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


def writeLogHeader(logAll,filename,myList,header="Header"):    
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
    #print(text)



def getLogFilename(logpath):
    createFolder(logpath)
    return os.path.join(logpath,datetimenow+".log")


def processZipFolders(folders):
    print("Process zip folder ..")
    zipRootFolder = createZipFolder()
    zipFiles = []
    for f in folders:
        new_f = getZipFileName(f)
        print(new_f)
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
    zipArchFolder = os.path.join(archpath,datetimenow)
    createFolder(zipArchFolder)
    print(zipFolder)
    return zipArchFolder

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

def findFolder2Backup(sourceFolder):
    #print("ftpserver = "+ftpserver+",user = "+ftplogin)
    print("Looking for Folder to Backup....")
    currentFolders, currentFiles = listAllFolder(sourceFolder)
    #folders, files = listAllFolder("C:\RPAShare")
    #print(files)
    #print(folders)  
    oldFolders, oldFiles= LoadList()  # load from pickle
    #print(foldersPrev)

    # all diff folder ie.  C\C , C\D , C\D\E , A\
    newCreatedFolders = diffList(currentFolders,oldFolders)
    #print(newCreatedFolders)
    
    # Folder that contain diff root only  i,e, C , A
    rootNewCreatedFolders = removeChildFolder(newCreatedFolders) 
    #print(rootNewCreatedFolders)
    return currentFolders,currentFiles,newCreatedFolders,rootNewCreatedFolders

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
    files = []
    try:
        folders = loadFile2List(pickleFolders)
        #files = loadFile2List(pickleFiles)
    except:
        folders = []
    return folders,files

def loadFile2List(myFilename):
    try:
        with open(myFilename, 'rb') as f:
            return pickle.load(f)
    except:
        raise Exception('File not found')
        
#Dump list to Pickle File
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
        #print(listFile)
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
