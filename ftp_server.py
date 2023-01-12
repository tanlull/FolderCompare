from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import settings

ftpserver = settings.ftp_server_address
ftpport = settings.ftpport
ftplogin =  settings.ftplogin
ftppassword = settings.ftppassword
ftppath = settings.ftppath 


authorizer = DummyAuthorizer()
authorizer.add_user(ftplogin, ftppassword, ftppath ,perm="elradfmw") # สร้าง user ชื่อ user รหัส 12345 ที่ตั้ง ftp คือ /home/giampaolo
#authorizer.add_anonymous("/home/nobody") # สร้างสิทธิ์ให้เข้าถึงโฟลเลอร์ /home/nobody ให้ user คนทั่วไป

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((ftpserver, ftpport), handler) # กำหนดค่า Server คือ 127.0.0.1 port 21
server.serve_forever() # ทำงาน