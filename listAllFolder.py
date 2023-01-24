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

now = datetime.now()
datetimenow = now.strftime("%Y-%m-%d_%H-%M")

ftpserver = settings.ftpserver
ftplogin =  settings.ftplogin
ftppassword = settings.ftppassword
pricefile = settings.pricefile #path to the file with price (price-list)
archpath = settings.archpath #archive folder for uploaded prices
ftppath = settings.ftppath #path on ftpserver to folder where need upload price
sleep = settings.sleep
sourceFolder = settings.sourceFolder
targetFolder = settings.targetFolder
logpath = settings.logpath
logAll = settings.logFile



def main():

    allFolders, rootFolders = findFolder2Backup()
    writeLog(logAll,getLogFilename(logpath),rootFolders,createZipFolder())
    processZipFolders(rootFolders)


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
    return logpath+"\\"+datetimenow+".log"


def processZipFolders(folders):
    zipRootFolder = createZipFolder()
    for f in folders:
        new_f = getZipFileName(f)
        print(new_f)
        zipFolderAndSub(f,zipRootFolder+new_f+".zip")

def getZipFileName(zipFile):
    f = zipFile.replace("_", "-" )
    f = f.replace("\\", "_" )
    f = f.replace("C:", "" )
    f = f.replace("_", "",1 )
    return f

def createZipFolder():
    zipFolder = archpath + "\\"+ datetimenow + "\\"
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
    folders = loadFile2List("folders.pickle")
    files = loadFile2List("files.pickle")
    return folders,files

def dumpList(folders,files):
    dumpList2File(folders,"folders.pickle")
    dumpList2File(files,"files.pickle")

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
