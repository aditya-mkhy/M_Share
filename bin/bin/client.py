import socket, os
from threading import Thread
import threading
from json import loads
import time 
from util import log
from random import randint
import ssl

def data_size_cal(size):
    st=None
    if size < 1024:
        st=f'{size} Bytes'
        
    elif size < 1022976 :
        size=str(size/1024).split('.')
        size=size[0]+'.'+(size[1])[:1]
        st=f'{size} KB'

    elif size < 1048576 :
        size=str(size/1048576).split('.')
        size=size[0]+'.'+(size[1])[:2]
        st=f'{size} MB'

    elif size < 1047527424:
        
        size=str(size/1048576).split('.')
        size=size[0]+'.'+(size[1])[:1]
        st=f'{size} MB'
        
    elif size < 1073741824:
        
        size=str(size/1073741824).split('.')
        size=size[0]+'.'+(size[1])[:2]
        st=f'{size} GB'
        
    elif size >= 1073741824:
        size=str(size/1073741824).split('.')
        size=size[0]+'.'+(size[1])[:1]
        st=f'{size} GB'
    else:
        st='Error_in_cal'
    return st


class Client:
    def __init__(self, parent=None, ip=[]):
    
        self.parent = parent
        self.hosts = ip
        self.port = 8888

        # data defination
        self.prevData = ""
        self.chunk = 10485760
        self.filesIdd = {} #fileId : []
        self.stoptimer = False

        self.basePath = "C:/Users/mahad/Pictures/File/" # Path where all recieved files stored


        # recv and write Variable Def
        self.dataList1 = []
        self.dataList2 = []

        self.recv1St = False
        self.recv2St = False

        self.processed1 = False
        self.processed2 = False

        self.threadRecv1 = None
        self.threadRecv2 = None
        self.threadWrite1 = None
        self.threadWrite2 = None


        self.sizeRecvByConn1 = 0
        self.sizeRecvByConn2 = 0
        self.sizeOfCurrentFile = 0
        self.prevSize = 0


        # Connections.....
        self.mainConn = None
        self.conn1 = None
        self.conn2 = None


    
        #SLLL
        self.server_cert = './data/cert/server.pem'
        self.client_key = './data/cert/client.key'
        self.client_cert = './data/cert/client.pem'

        self.server_sni_hostname = "darkstartechserver@MahadevDevlopers"

        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.server_cert)
        self.context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)

        self.useEncryption = True



    def connectToServer(self):
        try:
            #__initializing_server
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.hosts[0], self.port))

            if self.useEncryption:
                try:
                    connSll = self.context.wrap_socket(conn, server_side=False, server_hostname=self.server_sni_hostname)
                    connSll.settimeout(2)
                    self.mainConn = connSll

                except Exception as e:
                    try:
                        conn.close()
                        connSll.close()
                    except:
                        log("ClosingConnection Error")
                    log(f"Error[384] connectToServer : {e}")
            else:
                self.mainConn = conn

            log(f"ConnectedFrom==>{self.hosts[0]}")
            self.mainConn.sendall(b"---ID--805")
            conf = self.mainConn.recv(100)
            if conf == b"--ok-805":
                log(f">>>>> 805 is connected")
            else:
                print(f"Error[388] connectToServer Conf :- {e}")


        except Exception as hj:
            print(f"Error[400] connectToServ :- {hj}")



    def conn1Connect(self):
        try:
            #__initializing_server
            conn1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn1.connect((self.hosts[0], self.port))

            if self.useEncryption:
                try:
                    connSll = self.context.wrap_socket(conn1, server_side=False, server_hostname=self.server_sni_hostname)
                    connSll.settimeout(1)
                    self.conn1 = connSll

                except Exception as e:
                    try:
                        conn1.close()
                        connSll.close()
                    except:
                        log("ClosingConnection Error")
                    log(f"Error[385] conn1Connect : {e}")
            else:
                self.conn1 = conn1

            log(f"ConnectedFrom==>{self.hosts[0]}")
            self.conn1.sendall(b"---ID--705")
            conf = self.conn1.recv(100)
            if conf == b"--ok-705":
                log(f">>>>> 705 is connected")
            else:
                print(f"Error[401] conn1Connect Conf :- {e}")

        except Exception as e:
            print(f"Error[401] conn1Connect :- {e}")


    def conn2Connect(self):
        try:
            #__initializing_server
            conn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if len(self.hosts) > 1:
                host = self.hosts[1]
            else:
                host = self.hosts[0]
                
            conn2.connect((host, self.port))

            if self.useEncryption:
                try:
                    connSll = self.context.wrap_socket(conn2, server_side=False, server_hostname=self.server_sni_hostname)
                    connSll.settimeout(1)
                    self.conn2 = connSll

                except Exception as e:
                    try:
                        conn2.close()
                        connSll.close()
                    except:
                        log("ClosingConnection Error")
                    log(f"Error[385] conn1Connect : {e}")
            else:
                self.conn2 = conn2

            log(f"ConnectedFrom==>{host}")
            self.conn2.sendall(b"---ID--706")
            conf = self.conn2.recv(100)
            if conf == b"--ok-706":
                log(f">>>>> 706 is connected")
            else:
                print(f"Error[403] conn2Connect Conf :- {e}")

        except Exception as e:
            print(f"Error[403] conn2Connect :- {e}")
    

    def send(self, data: str):
        try:
            self.mainConn.sendall(f"{data}~".encode())
        except Exception as e:
            print(f"Error[401] send :- {e}")
            self.disconnect()


    def disconnect(self):
        print("Disconnected...")
        try:
            self.mainConn.shutdown(1)
        except:
            pass
        try:
            self.mainConn.close()
        except:
            pass

    def recv(self, bufSize=1024) -> str:
        if "~" in self.prevData:
            i = self.prevData.find("~")
            rdata = self.prevData[:i]
            self.prevData = self.prevData[i+1:]
            return rdata
        else:
            rdata = self.prevData
            while True:
                try:
                    data = self.mainConn.recv(bufSize)
                    log( f"dataRecv == {data}")
                    if not data:
                        return "Disconnected"
                    
                    rdata += data.decode()
                    if "~" in rdata:
                        l = rdata.find("~")
                        self.prevData = rdata[l+1:]
                        return rdata[:l]

                    print(f"~ in not in data=={rdata}")

                except Exception as e:
                    print(f"Error[400] Recv :-{e}")
                    self.disconnect()
                    break


    def run(self):
        self.connectToServer()
        self.recvWhile()

    def recvWhileThr(self):
        Thread(target=self.recvWhile, daemon=False).start()

    def recvWhile(self):
        time.sleep(2)
        # self.send("--sendNewFile")
        while True:
            data = self.recv()
            if data == "Disconnected":
                break


            self.ActOnData(data)
        
        self.disconnect()


    def ActOnData(self, data: str): # Action Ferformed on the data
            
        if "--file" in data:
            path, size, fileIdd = data.replace("--file","").split("||")
            size = int(size)
            fileIdd = int(fileIdd)

            self.parallelRecvFile(path, size, fileIdd)

    def parallelRecvFile(self, path: str, size: int, fileIdd: int):
        log(f"parallelRecvFile  :: path={path} :: size={size} :: fileIdd={fileIdd} ::")

        if not self.conn1:
            self.conn1Connect()
        if not self.conn2:
            self.conn2Connect()

        sendSize1 = size//2
        sendSize2 = size-sendSize1

        fromm1 = 0
        fromm2 = fromm1+sendSize1

        fullPath1 = f"{self.basePath}{path}.0_{fileIdd}.mshare"
        fullPath2 = f"{self.basePath}{path}.1_{fileIdd}.mshare"

        self.filesIdd[fileIdd] = [fullPath1, fullPath2]

        # COnnection 1
        info = f"--parall{fileIdd}||{fromm1}||{sendSize1}||{705}"
        self.send(info)
        
        conf = self.recv()
        if conf == f"--okS-705":
            print("Conferms satatus  705")

        self.stoptimer = False
        self.prevSize = 0
        self.sizeOfCurrentFile = size
        self.sizeRecvByConn1 = 0
        self.sizeRecvByConn2 = 0
        self.speed()
        
        log(info)
        
        self.threadRecv1 = Thread(target=self.getdatafromConn1, args=(sendSize1, fullPath1), daemon=True)
        self.threadRecv1.start()

        self.threadWrite1 = Thread(target=self.writeDataFromConn1, args=(fullPath1, fileIdd), daemon=True)
        self.threadWrite1.start()



        #Connection 2
        info = f"--parall{fileIdd}||{fromm2}||{sendSize2}||{706}"
        self.send(info)

        conf = self.recv()
        if conf == f"--ok-706":
            print("Conferms satatus  706")

        log(info)



        self.threadRecv2 = Thread(target=self.getdatafromConn2, args=(sendSize2, fullPath2), daemon=True)
        self.threadRecv2.start()

        self.threadWrite2 = Thread(target=self.writeDataFromConn2, args=(fullPath2, fileIdd), daemon=True)
        self.threadWrite2.start()



    def getdatafromConn1(self, oneSize: int, path: str):
        log("Recieving Data From COnnections 1")
        self.recv1St = False

        while True:
            data = self.conn1.recv(self.chunk)
            if not data:
                break

            self.dataList1.append(data)
            self.sizeRecvByConn1 += len(data)

            if self.sizeRecvByConn1 == oneSize:
                log(f"$$$$$$$ File Recv.........{path} and size={oneSize}")
                break
            
            elif self.sizeRecvByConn1 > oneSize:
                log("!!!!!  Errorro[Reveved more tha assing]")
                break

        self.recv1St = True
        log("Done Reciving from connection 1")

    def getdatafromConn2(self, oneSize: int, path: str):
        log("Recieving Data From COnnections 2")
        self.recv2St = False

        while True:
            data = self.conn2.recv(self.chunk)
            if not data:
                break

            self.dataList2.append(data)
            self.sizeRecvByConn2 += len(data)

            if self.sizeRecvByConn2 == oneSize:
                log(f"$$$$$$$ File Recv.........{path} and size={oneSize}")
                break
            
            elif self.sizeRecvByConn2 > oneSize:
                log("!!!!!  Errorro[Reveved more tha assing]")
                break

        self.recv2St = True
        log("Done Reciving from connection 2")



    def writeDataFromConn1(self, path: str, fileIdd: int):
        log("Writing data from connection 1")
        self.processed1 = False

        with open(path, "wb") as tf:
            while True:
                try:
                    tf.write(self.dataList1.pop(0))

                except IndexError:
                    # log(f"List is empty... Connection 1")
                    if self.recv1St:
                        tf.close()
                        log(f"]]]]]]]]] Writenn=Conn1={path}")
                        break

                    time.sleep(0.2)
                except Exception as e:
                    log(f"Error[405] writeDataFromConn1 : {e}")
    
        self.processed1 = True
        self.compileAllFiles(fileIdd)

    def writeDataFromConn2(self, path: str, fileIdd: int ):
        log("Writing data from connection 2")
        self.processed2 = False

        with open(path, "wb") as tf:
            while True:
                try:
                    tf.write(self.dataList2.pop(0))

                except IndexError:
                    # log(f"List is empty... Connection 2")
                    if self.recv2St:
                        tf.close()
                        log(f"Writenn=Conn2={path}")
                        break

                    time.sleep(0.2)
                except Exception as e:
                    log(f"Error[405] writeDataFromConn2 : {e}")
                    break
    
        self.processed2 = True
        self.compileAllFiles(fileIdd)


    def compileAllFiles(self, fileIdd: int):
        if self.processed1 and self.processed2:
            self.stoptimer = True

            log("File Revieving is Done")
            files = self.filesIdd[fileIdd]
            mainPath = files.pop(0)

            with open(mainPath, "ab") as tf:
                for file in files:
                    ff = open(file, "rb")
                    data = ff.read(self.chunk)
                    while data:
                        tf.write(data)
                        data = ff.read(self.chunk)
                    ff.close()
                    os.remove(file)
            tf.close()

            path, ext = os.path.splitext(mainPath)
            path, ext = os.path.splitext(path)
          
            os.rename(mainPath, path)
            log(f"Files is Compileds and ready to play")
            time.sleep(1)
            self.send("--sendNewFile")
            log("Request Send....")

    def speed(self, fun=None):
        if not self.stoptimer:

            pr = self.prevSize
            sz= self.sizeRecvByConn1 + self.sizeRecvByConn2
            self.prevSize = sz

            print(f"({data_size_cal(sz)} of {data_size_cal(self.sizeOfCurrentFile)} , {data_size_cal(sz-pr)}/Sec)")

            threading.Timer(1.0, self.speed, (fun,)).start()

  
if __name__ == "__main__":
    client = Client()
    client.run()