import socket
from  threading import Thread
import time
import os



#pip install pyftpdlib < this should be installed

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}

is_dir_exists = os.path.isdir('shared_files')
if(not is_dir_exists):
    os.makedirs('shared_files')

def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER

    banner1 = "Welcome, You are now connected!"
    client.send(banner1.encode())



def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
                "client"         : client,
                "address"        : addr,
                "connected_with" : "",
                "file_name"      : "",
                "file_size"      : 4096
            }

        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target = handleClient, args=(client,client_name,))
        thread.start()

            
def setup():
    print("\n\t\t\t\t\t\tIP Music Sharing\n")

    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


def ftp():
    global IP_ADDRESS

    authoriser = DummyAuthorizer()
    authoriser.add_user("lftpd","lftpd",".",perm="elradfmw") 
    handler = FTPHandler
    handler.authorizer = authoriser
    ftp_server = FTPServer((IP_ADDRESS, 21), handler)
    ftp_server.serve_forever()
 
 
setup_thread = Thread(target=setup)           
setup_thread.start()

ftp_thread = Thread(target=ftp)               
ftp_thread.start()

