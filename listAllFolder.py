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

datetimenow = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
ftpserver = settings.ftpserver
ftplogin =  settings.ftplogin
ftppassword = settings.ftppassword
pricefile = settings.pricefile #path to the file with price (price-list)
archpath = settings.archpath #archive folder for uploaded prices
ftppath = settings.ftppath #path on ftpserver to folder where need upload price
sleep = settings.sleep
sourceFolder = settings.sourceFolder
targetFolder = settings.targetFolder


def main():
    #print("ftpserver = "+ftpserver+",user = "+ftplogin)

    # folders, files = listAllFolder(sourceFolder)
    folders, files = listAllFolder("C:\RPAShare")
    #print(files)
    print(folders)


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

        if len(files): #ifnot empty
            listFile = genFileformDict(root,files,"\\") # Generate full file path (C:\\xxx + yyy.txt)
            # print(listFile)
            allFiles.append(listFile)


    #printDictDir(folderStructureAll,"dir")
    #print(allFolder)
    return allFolders,allFiles

def genFileformDict(base,files,seperator):
    resultfiles = []
    for f in files:
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
