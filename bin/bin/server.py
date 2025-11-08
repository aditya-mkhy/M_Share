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


class Server:
    def __init__(self, parent=None):
        
        self.parent = parent
        self.host = "0.0.0.0" 
        self.port = 8888

        # data 
        self.prevData = ""
        self.chunk  = 1048576
        self.filesIdd = {} #fileId : FilePath
        self.stoptimer = False
        self.stopBroadcast  = False

        # recv and write Variable Def
        self.dataList1 = []
        self.dataList2 = []

        self.read1St = False
        self.read2St = False

        self.processed1 = False
        self.processed2 = False

        self.threadSend1 = None
        self.threadSend2 = None
        self.threadRead1 = None
        self.threadRead2 = None


        self.sizeSendByConn1 = 0
        self.sizeSendByConn2 = 0
        self.sizeOfCurrentFile = 0
        self.prevSize = 0

        # Connections.....
        self.mainConn = None
        self.conn1 = None
        self.conn2 = None

        #User Data
        self.userName = "Lakshay Saini"
        self.userId = "lakshaySaini12@"
        self.icon = "002"
        self.devID = "98420njd98sudnw98kjdwn4HJNEWIU3982"

        #Certificate Path
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

        self.fileList = [
            "C:/Users/mahad/Downloads/Black.Panther.Wakanda.Forever.2022.Bluray.1080p.x264.Hindi.English.Esubs.MoviesMod.org.mkv"
            # "D:/Movies/English/Covenant.(2017).mkv",
            # "C:/Users/mahad/Downloads/life.mkv",
            # "C:/Users/mahad/Downloads/Lockout.mkv",
            # "C:/Users/mahad/Downloads/JusticeLeague2017.mkv"

        ]

        self.blockUserList = []

    def runTh(self):
        Thread(target=self.run, daemon=False).start()

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
                    # log("----@--> Time OUT")
                    pass
                    
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
            # log("SSL established. Peer: {}".format(sslconn.getpeercert()))
            sslconn.settimeout(0.5)
            self.verifyConnection(sslconn, addr)
  

        except Exception as e:
            print("Error in Cerificate verification Process" , e)
            print("Closing connection==>",addr[0])

        finally:
            log("Finally i love my mahadev")
            # try:
            #     sslconn.close()
            # except:
            #     pass
            # try:
            #     conn.close()
            # except:
            #     pass



    def verifyConnection(self, conn: socket.socket, addr: tuple):
        data = conn.recv(200)
        print("Data898==>", data)

        if data == b"--sendUserInfo--mshare":
            data = f"||{self.userName}||{self.userId}||{self.devID}||{self.icon}||"
            conn.sendall(data.encode())


        elif data == b"--handshake--mshare":
            conn.sendall(b"200-ok")
            data = conn.recv(1024).decode()

            try:
                data = data.split("||")

                userName = data[1]
                userId   = data[2]
                devId    = data[3]
                icon     = data[4]

                conn.sendall(b"")


                data2 = [userName, userId, devId, icon]
                
                self.parent.connected(data2)

            except Exception as e:
                log(f"---[{e}]8000 is the eerror")
                

        elif b"---ID--" in data:
            data = data.decode()
            idd = int(data.replace("---ID--", ""))
            print("idd==>", idd)

            if idd == 805:
                if not self.mainConn:
                    self.mainConn = conn
                    self.mainConn.sendall(b"--ok-805")
                    data = self.recv()

                    print("DataRecv==>", data)

                    if "--handShake--" in data:
                        data = data.replace("--handShake--","").split("||")

                        if data[1] not in self.blockUserList:
                            self.send(f"ok--{data[1]}")
                            log("Send Conf Data...")
                            self.parent.connected(data)
                        
                else:
                    self.mainConn = conn
                    self.mainConn.sendall(b"--ok-805")

            elif idd == 705:
                self.conn1 = conn
                self.conn1.sendall(b"--ok-705")

            elif idd == 706:
                self.conn2 = conn
                self.conn2.sendall(b"--ok-706")



    def sendFile(self, path):

        siz=os.stat(path).st_size
        self.size = siz

        fileIDD = self.genFileIDD()
        self.filesIdd[fileIDD] = path
        
        self.stoptimer = False
        self.prevSize = 0
        self.sizeOfCurrentFile = siz
        self.sizeSendByConn1 = 0
        self.sizeSendByConn2 = 0
        self.read1St = False
        self.read2St = False
        self.processed1 = False
        self.processed2 = False


        self.send(f"--file{os.path.basename(path)}||{siz}||{fileIDD}")



    def send(self, data: str):
        try:
            self.mainConn.sendall(f"{data}~".encode())
        except Exception as e:
            print(f"Error[401] send :- {e}")

    def shutdownServer(self):
        self.disconnect()
        log(" Stoping Server main Server....")
        try:
            self.network.shutdown(1)
        except:
            pass

        try:
            self.network.close()
        except:
            pass


    def disconnect(self):
        print("Disconnected...890")

        try:
            self.mainConn.shutdown(1)
        except:
            pass
        try:
            self.mainConn.close()
        except:
            pass

        try:
            self.conn1.close()
        except:
            pass
        try:
            self.conn2.close()
        except:
            pass

        self.parent.disconnectCall()

    def recv(self, bufSize=1024):
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

                except Exception as e:
                    print(f"Error[400] Recv :-{e}")
                    self.disconnect()
                    break


    def recvWhile(self):
        while True:
            data = self.recv()
            if data == "Disconnected":
                break

            self.ActOnData(data)
        
        self.disconnect()


    def ActOnData(self, data): # Action Ferformed on the data
        print("DataAction :-", data)

        if "--sendNewFile" in data:
            log("SendFileRequest")
            if self.fileList != []:
                path = self.fileList.pop(0)
                self.sendFile(path)

        if "--parall" in data:
           
            # info = f"--parall{fileIdd}||{fromm}||{oneSize}||{idd}".encode()
            fileIdd, fromm, oneSize, ConnectionIdd = data.replace("--parall","").split("||")
            fileIdd = int(fileIdd)
            fromm = int(fromm)
            oneSize = int(oneSize)
            ConnectionIdd = int(ConnectionIdd)
            self.send(f"--okS-{ConnectionIdd}") #Sending Confermation message
            

            if ConnectionIdd == 705:
                self.speed()

                self.threadRead1 = Thread(target=self.readDataForConn1, args=(fileIdd, fromm, oneSize, ConnectionIdd), daemon=True)
                self.threadRead1.start()

                self.threadSend1 = Thread(target=self.sendataforConn1, args=(fileIdd, ConnectionIdd), daemon=True)
                self.threadSend1.start()
            
            
            elif ConnectionIdd == 706:
                self.threadRead2 = Thread(target=self.readDataForConn2, args=(fileIdd, fromm, oneSize, ConnectionIdd), daemon=True)
                self.threadRead2.start()

                self.threadSend2 = Thread(target=self.sendataforConn2, args=(fileIdd, ConnectionIdd), daemon=True)
                self.threadSend2.start()




    def sendataforConn1(self, fileIdd: int, ConnectionIdd: int):
        log(f"Sending Data From COnnections 1 and {fileIdd}, {ConnectionIdd}")
        self.processed1 = False

        while True:
            try:
                da = self.dataList1.pop(0)
                self.conn1.sendall(da)
                self.sizeSendByConn1 += len(da)

            except IndexError:
                # log(f"List is empty......")
                if self.read1St:
                    log(f"&&&&&&&&&&   Send Data Success==COnnection 1 &&&&&&&&&&&&")
                    break
                time.sleep(0.01)
            
            except Exception as e:
                print(f"Error[409] sendatafromConn1 :- {e}")

        log("Done......sendatafromConn1 ")
        self.processed1 = True
        self.doneOneFile()

    def sendataforConn2(self, fileIdd: int, ConnectionIdd: int):
        log(f"Sending Data From COnnections 2 and {fileIdd}, {ConnectionIdd}")
        self.processed2 = False


        while True:
            try:
                da = self.dataList2.pop(0)
                self.conn2.sendall(da)
                self.sizeSendByConn2 += len(da)

            except IndexError:
                # log(f"List is empty......")
                if self.read2St:
                    log(f"&&&&&&&&&&   Send Data Success==COnnection 2 &&&&&&&&&&&&")
                    break
                time.sleep(0.1)
            
            except Exception as e:
                print(f"Error[408] sendatafromConn2 :- {e}")

        log("Done......sendatafromConn2 ")
        self.processed2 = True
        self.doneOneFile()

    def readDataForConn1(self, fileIdd: int, fromm: int, oneSize: int, ConnectionIdd: int):
        self.read1St = False
        log("Reading Data for COnnection 1 ")
        log(f"********Conn1 fileIdd={fileIdd} | fromm={fromm} | oneSize={oneSize} | ConnectionIdd={ConnectionIdd}")
        path = self.filesIdd[fileIdd]

        ff = open(path, "rb")
        ff.seek(fromm)
        readSize = 0
        
        if oneSize  >= self.chunk:# chunk should be greater than send size
    
            while True:
                if readSize == oneSize:
                    log(f"ReadingDone.........{path} and from={fromm} COnnection 1")
                    break

                if len(self.dataList1) > 300:
                    time.sleep(0.0001)
                else:
                    if (oneSize - readSize) >= self.chunk:
                        data = ff.read(self.chunk)
                    else:
                        data = ff.read(oneSize - readSize)

                    if data:
                        self.dataList1.append(data)
                        readSize += len(data)
                    else:
                        log("Error[908] : Nothing remain to read......")
                        break
        else:
            data = ff.read(oneSize)
            self.dataList1.append(data)
            log("Conne1 Mahadev")

        log(f"^^^^^^^^^Conn1 fileIdd={fileIdd} | fromm={fromm} | readSize={readSize} | oneSize={oneSize} ")
        log(f"%%%%%%%  Reading Done..== Connection 1 %%%%%%%%")
        self.read1St = True
        ff.close()

    def readDataForConn2(self, fileIdd: int, fromm: int, oneSize: int, ConnectionIdd: int):
        self.read2St = False
        log("Reading Data for COnnection 2")
        log(f"********Conn2 fileIdd={fileIdd} | fromm={fromm} | oneSize={oneSize}")

        path = self.filesIdd[fileIdd]

        ff = open(path, "rb")
        ff.seek(fromm)
        readSize = 0
        
        if oneSize  >= self.chunk:# chunk should be greater than send size
    
            while True:
                if readSize == oneSize:
                    log(f"ReadingDone.........{path} and from={fromm} COnnection 2")
                    break

                if len(self.dataList2) > 300:
                    time.sleep(0.0002)
                else:
                    if (oneSize - readSize) >= self.chunk:
                        data = ff.read(self.chunk)
                    else:
                        data = ff.read(oneSize - readSize)

                    if data:
                        self.dataList2.append(data)
                        readSize += len(data)
                    else:
                        log("Error[908] : Nothing remain to read......")
                        break
        else:
            data = ff.read(oneSize)
            self.dataList2.append(data)
            log("COnn2 Mahadev..")

        log(f"^^^^^^^^^Conn2 fileIdd={fileIdd} | fromm={fromm} | readSize={readSize} | oneSize={oneSize} ")
        log(f"%%%%%%%  Reading Done..== Connection 2 %%%%%%%%")
        self.read2St = True
        ff.close()

    def doneOneFile(self):
        if self.processed1 and self.processed2:
            self.processed2 = False
            self.processed2 = False
            self.stoptimer = True
            print("........................Sending Done.....................")
            

    def speed(self, fun=None):
        if not self.stoptimer:

            pr = self.prevSize
            sz= self.sizeSendByConn1 + self.sizeSendByConn2
            self.prevSize = sz

            

            print(f"({data_size_cal(sz)} of {data_size_cal(self.sizeOfCurrentFile)} , {data_size_cal(sz-pr)}/Sec)")

            threading.Timer(1.0, self.speed, (fun,)).start()


    def genFileIDD(self) -> int:
        d = randint(10000, 999999)

        while d in self.filesIdd:
            d = randint(10000, 999999)

        return d



if __name__ == "__main__":
    serv = Server()
    serv.run()