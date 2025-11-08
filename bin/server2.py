import socket
from threading import Thread
from json import loads
import time 
from util import log
import ssl
import random

class BroadCast:
    def __init__(self, parent=None):
        
        self.parent = parent
        self.host = "0.0.0.0" 
        self.port = 8888

        self.userName = "Lakshay Saini"
        self.userId = "lakshaySaini12@"
        self.icon = "002"

        self.devID = "98420njd98sudnw98kjdwn4HJNEWIU3982"

        self.server_cert  = './data/cert/server.pem'
        self.server_key   = './data/cert/server.key'
        self.client_certs = './data/cert/client.pem'



        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
        self.context.load_verify_locations(cafile=self.client_certs)


        #__initializing_server
        self.network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.network.bind((self.host, self.port))
            self.network.listen(100)
            self.network.settimeout(3)
        except Exception as e:
            log(f"Error[234] : {e}")

    def runTh(self):
        Thread(target=self.run, daemon=True).start()


    def run(self):
        log("BroadCasrt is Accepting Connections......")
        log("***** Quit the server with CTRL-BREAK. *****")
        try:
            while True:
                try:
                    conn, addr = self.network.accept()
                    log(f'---> Got_connection_from ->{addr}')
                    Thread(target=self.createSslConn,  args=(conn, addr), daemon=True).start()

                except socket.timeout:
                    log("----@--> Time OUT")
                    
                except KeyboardInterrupt:
                    log("--KeyboardInterrupt Deceted.. Stoping Server---")
                    try:
                        self.network.shutdown(1)
                    except:
                        pass
                    self.network.close()
                    exit()
                    
        except KeyboardInterrupt:
            log("KeyboardInterrupt Deceted.. Stoping Server")
            try:
                self.network.shutdown(1)
            except:
                pass
            self.network.close()
            exit()

    def createSslConn(self, conn, addr):
        try:

            sslconn = self.context.wrap_socket(conn, server_side=True)
            log("SSL established. Peer: {}".format(sslconn.getpeercert()))
            sslconn.settimeout(0.5)
  

            data = sslconn.recv(200)
            log(f"Data recv==> {data}")
            if data == b"--sendUserInfo--mshare":
                data = f"||{self.userName}||{self.userId}||{self.devID}||{self.icon}||"
                sslconn.sendall(data.encode())

            elif data == b"--handshake--mshare":
                sslconn.sendall(b"200-ok")
                data = sslconn.recv(1024).decode()

                try:
                    data = data.split("||")

                    userName = data[1]
                    userId   = data[2]
                    devId    = data[3]
                    icon     = data[4]

                    data2 = [userName, userId, devId, icon]
                    
                    self.parent.connected(data2)

                except Exception as e:
                    log(f"---[{e}]8000 is the eerror")

            else:
                log("CLient is connected to recv DATA....")

        except Exception as e:
            print("Error in Cerificate verification Process" , e)
            print("Closing connection==>",addr[0])

        finally:
            try:
                sslconn.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass

    def verifying(self, conn, addr):
        try:
            data  = conn.recv(1024)
            log(f"DataRecvBefSll==> {data.decode()}")
            if data == b'--ping-Mshare':
                data = f"--ok--2002"
                conn.sendall(data.encode())
                self.createSslConn(conn, addr)

        except socket.timeout:
            log("----@--> Time OUT>> recving data..")

        except Exception as e:
            log(f"Error[2034] : {e}")
        finally:
            try:
                # conn.close()
                pass
            except:
                pass


if __name__ == "__main__":
    serv = BroadCast()
    serv.run()