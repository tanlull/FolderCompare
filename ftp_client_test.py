import ftplib as ftp
import settings

ftpserver = settings.ftpserver
ftplogin =  settings.ftplogin
ftppassword = settings.ftppassword
ftpport = settings.ftpport
ftppath = settings.ftppath


def main():
    print("Connecting to FTP Server {}:{} \n".format(ftpserver,ftpport))
    session = connectFTP(ftpserver,ftpport,ftplogin,ftppassword)


def connectFTP(ftpserver,ftpport,ftplogin,ftppassword):
    try:
        session = ftp.FTP()
        session.connect(ftpserver,int(ftpport))
        session.login(ftplogin,ftppassword)
        session.encoding = "utf-8"
        print("Result => Success")
        return session
    except IOError as e:
        import sys
        error_msg = "I/O error({0}): {1}".format(e.errno, e.strerror)
        print(error_msg)        
        sys.exit("Exit FTP Error")  

if __name__ == '__main__':
    # while True:
    #     main()
    #     time.sleep(sleep)
    main()