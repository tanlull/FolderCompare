# ---- Client Side Config 
ftpserver = '127.0.0.1' #adress of FTP server for client to connect

pricefile = 'C:\\Users\\WELCOME\\Desktop\\data_to_backup' #path to the FILE
sourceFolder = 'C:\\Users\\WELCOME\\Desktop\\data_to_backup' #path to the FILE
targetFolder = 'C:\\Users\\WELCOME\\Desktop\\data_to_backup_bak' #path to the FILE
archpath = 'C:\\Users\\WELCOME\Desktop\\data_to_backup_bak' #archive FOLDER


# --- FTP Server Side Config ----#
ftp_server_address = '0.0.0.0' #adress of FTP server to be as a Server (used by ftp_server.py)
ftpport = '2121' #adress of FTP server
ftplogin = 'tan' #login for FTP server
ftppassword = 'tan1234' #password for FTP server
ftppath = 'C:\\FTP' #path on ftpserver to FOLDER where need upload pfile


## Path to keep log and process file for backup
logPath = 'C:\\Users\\WELCOME\Desktop\\data_to_backup\\backup_process\\log' #log daily path / daily file  
logFile = 'main_log.log' #main log  
backupProcessPath = 'C:\\Users\\WELCOME\Desktop\\data_to_backup\\backup_process\\process' # Drectory to store directory structure
pickleFiles = 'files.pickle' #store file
pickleFolders = 'folders.pickle' #store folder

sleep = 5 #time to sleep between checks



