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
    listAllFolder(sourceFolder)


def listAllFolder(path):
    folderStructureAll = []
    allFolder =[]
    for root, dirs, files in os.walk(path):
        mydict = {
            "dir": root,
            "subdir":dirs,
            "file":files
        }
        print(root)
        print(dirs)
        # print("subdir =".join(dirs))
        # print("file = ".join(files))
        folderStructureAll.append(mydict) # all folder structure

        allFolder.append(root)  # Root folder


    #printDictDir(folderStructureAll,"dir")
    #print(allFolder)
    return allFolder


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
