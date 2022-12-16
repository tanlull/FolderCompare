import os.path
import shutil
from ftplib import FTP
import datetime
import time
import settings
import os

datetimenow = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
ftpserver = settings.ftpserver
ftplogin =  settings.ftplogin
ftppassword = settings.ftppassword
pricefile = settings.pricefile #path to the file with price (price-list)
archpath = settings.archpath #archive folder for uploaded prices
ftppath = settings.ftppath #path on ftpserver to folder where need upload price
sleep = settings.sleep


def main():
    print("ftpserver = "+ftpserver+",user = "+ftplogin)
    listAllFolder(pricefile)

    # WaitForFileExists(pricefile)
    # DoUploadToFtp(ftpserver, ftplogin, ftppassword, pricefile, ftppath)
    # FileToArchive(pricefile, archpath)
    # FileDelete(pricefile)

    # List all files and subfolders in the directory tree
def listAllFolder(path):

    for root, dirs, files in os.walk(path):
        print(f'Root: {root}')
        print(f'Directories: {dirs}')
        print(f'Files: {files}')



def FileExists(pricefile, after_delete=False): # флаг after_delete нужен для проверки существования файла после удаления
    if os.path.isfile(pricefile): #check is file exists?
        if after_delete:
            print('Прайс не был удалён')
            raise PriceNotDeleted
        print('Прайс найден')
        return True
    else:
        print('Прайс не найден')
        if after_delete:
            return
        return False

def WaitForFileExists(pricefile):
    while not os.path.isfile(pricefile):
        print('not exists')
        time.sleep(sleep)
    FileExists(pricefile)


def DoUploadToFtp(ftpserver, ftplogin, ftppassword, pricefile, ftppath):
    ftp = FTP(ftpserver)
    ftp.login(ftplogin, ftppassword)
    with open(pricefile, 'rb') as fobj:
        ftp.storbinary('STOR ' + ftppath, fobj, 1024)
    print('Прайс загружен')
    ftp.quit()


def ArchNewNameGenerator(pricefile, archpath):
    price_splitname = os.path.splitext(os.path.split(pricefile)[1])
    archfullfilename = os.path.join(archpath, price_splitname[0] + ' от ' + datetimenow + price_splitname[1])
    return archfullfilename

def IsArchived(archfullfilename):
    if os.path.isfile(archfullfilename):
        print('Прайс архивирован')
    else:
        raise NotArchived('Файл не удалось отправить в архив')

def FileToArchive(pricefile, archpath):
    archfullfilename = ArchNewNameGenerator(pricefile, archpath)
    shutil.copy(pricefile, archfullfilename)
    IsArchived(archfullfilename)


def FileDelete(pricefile):
    os.remove(pricefile)
    FileExists(pricefile, after_delete=True)



if __name__ == '__main__':
    # while True:
    #     main()
    #     time.sleep(sleep)
    main()
