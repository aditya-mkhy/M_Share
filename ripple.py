from tkinter import *
import ctypes , os , sys , socket
from random import choice , randint
from tkinter.filedialog import  askopenfilenames , askdirectory 
import tkinter.ttk as ttk
from threading import Thread
import time
from functools import partial as functools_partial
from time import sleep
from PIL import Image, ImageTk
import random
from recvwin import Recieve
from search import SearchSender
from util import log, resource_path
from client import Client
from tkinter import messagebox
# from Mshare import App 
import rsa



##=====PROTOCOL==========##
"""
Search IP Range 1-<Given Range>
"""

class RippleLabel(Label):
    def play(self, path):
        self.pause = False
        img = Image.open(path)
        self.indx = 0
        self.frames = []

        for i in range(31):
            self.frames.append(ImageTk.PhotoImage(img.copy()))
            img.seek(i)

        try:
            self.delay = img.info['duration']
            self.delayDefault = img.info['duration']
        except:
            self.delay = 100

        self.next_frame()


    def next_frame(self):
        self.indx += 1
        self.indx %= len(self.frames)

        if not self.pause:
            self.config(image=self.frames[self.indx])
            self.after(self.delay, self.next_frame)

class Cbutton(Label):
    def setCommand(self, command = None):
        self.cmd = command
        self.bind("<Button-1>", self.callCommand)

    def callCommand(self, event):
        self.cmd()


class popUpButton():#self, name, userId, DevId, img, avt, IP , cmd
    def __init__(self, parent, name=None, userId=None, DevId=None, img=None, avt=None, IP=None , cmd=None) -> None:
        self.parent = parent

        self.userName = name
        self.userId = userId
        self.devId = DevId
        self.IP = [IP]
        self.avt = avt


        self.parent.PopupWinObg.append(self)
        self.img = img
        self.scrn = Toplevel(self.parent.parent.root_mshare)
        
        self.bg = "pink4"
        self.UserIcon = Button(self.scrn, highlightbackground=self.bg, image=self.img,fg=self.bg,
                        bd=0,compound='right',activebackground=self.bg, cursor='hand2', bg=self.bg,
                        command=lambda : cmd(self))
        
        self.UserIcon.pack(side='top')

        if self.userName != None:
            self.name = Label(self.scrn, text=userId, font=("yu gothic ui", 10, "bold"),bg=self.bg , fg="white",bd=0, relief="flat",justify="left")
            self.name.pack(side='top')
        # self.scrn.wm_attributes('-alpha',0.8)

        self.scrn.wm_attributes('-transparentcolor', self.bg)
        self.scrn.config(bg=self.bg, bd=0, relief='raised')
        # self.scrn.attributes("-topmost", 1)

        self.scrn.overrideredirect(True)

    def getData(self) -> list:
        return [self.userName, self.userId, self.devId, self.avt, self.IP]

    def mainwindowGeo(self):
        pass
    def hide(self):
        self.scrn.withdraw()

    def configure_place(self):
        try:
            xx = self.parent.parent.root_mshare.winfo_x()
            yy = self.parent.parent.root_mshare.winfo_y()
            self.scrn.geometry(f'+{xx + self.x}+{yy + self.y}')   

            self.scrn.deiconify()
        except Exception as e:
            print(e)

    def getPlaceInfo(self):

        root_x = self.parent.parent.root_mshare.winfo_x()
        root_y = self.parent.parent.root_mshare.winfo_y()

        x = (self.scrn.winfo_x() - root_x) 
        y = (self.scrn.winfo_y() - root_y) 

        x1 = x - 20
        y1 = (y + self.scrn.winfo_height()) + 20

        x2 = (x + self.scrn.winfo_width()) + 20
        y2 = y - 20
        return [x1, y1, x2 , y2]

    def place(self, x, y):
        self.x = x
        self.y = y
        xx = self.parent.parent.root_mshare.winfo_x()
        yy = self.parent.parent.root_mshare.winfo_y()

        self.scrn.geometry(f'+{xx + x}+{yy + y}')
        

    def place_forget(self):
        self.scrn.destroy()

    def destroy(self):
        self.scrn.destroy()



class FindSenderWin():
    def __init__(self, parent):
        self.parent = parent


        self.gifPath =  resource_path("data/ripple-effect-gif-7.gif")
        self.bg = "#23146B"

        self.screenHeight = self.parent.root_mshare.winfo_screenheight()

        self.playRipple = True

        self.PopupWinObg = []

        self.maxWidth = 900
        self.minwidth = 20

        self.minHeight = 35
        self.maxHeight = 500

        self.container=Frame(self.parent.root_mshare, bg=self.bg)
        self.container.pack(fill='both', expand=True)

        self.start_frame=Frame(self.container, bg=self.bg)
        self.start_frame.pack(expand=True, fill="both", side="top")

        self.infoFrame = Frame(self.container, bg=self.bg)
        self.infoFrame.pack(fill="both", side="bottom", ipady=34)


        # ========== Info Frame Items ========================

        self.status = Label(self.infoFrame, text="Scanning......", font=("yu gothic ui", 14, "bold"), bg=self.bg, fg="orange", bd=0,
                                width=20, justify="left", anchor="w")
        self.status.place(x=500, y=15)
        self.scanProgVal = 1

        self.interface = Label(self.infoFrame, text="Interface : All", font=("yu gothic ui", 9, "bold"), bg=self.bg, fg="orangered", bd=0,
                                width=37, justify="right", anchor="e")
        self.interface.place(x=820, y=25)

        self.shotsList1 = []
        self.shotsList2 = []
        for i in range(1,7):
            im = Image.open(resource_path(f"data/shot{i}.png"))
            width, height = im.size
            self.shotsList1.append( ImageTk.PhotoImage(im.crop( (0, 0, width//2, height)),     master=self.parent.root_mshare) )
            self.shotsList2.append( ImageTk.PhotoImage(im.crop( (width//2, 0, width, height)), master=self.parent.root_mshare) )

        self.modeButLeft = Cbutton(self.infoFrame, bg=self.bg,image=self.shotsList1[0], bd=0, relief="flat", cursor="hand2",
                        borderwidth=0,compound="right",highlightthickness=0)
        self.modeButLeft.setCommand(command= lambda : self.modeButCommand("local"))
        self.modeButLeft.place(x=30, y=0)

        self.modeButRight = Cbutton(self.infoFrame, bg=self.bg, image=self.shotsList2[0], bd=0, relief="flat", activebackground=self.bg, cursor="hand2",
                        borderwidth=0, compound="left", highlightthickness=0, border=0 )
        self.modeButRight.setCommand(command= lambda : self.modeButCommand("global"))
        self.modeButRight.place(x=171, y=0)
        self.modeValue = 'local'


        self.ripple = RippleLabel(self.start_frame, bg=self.bg, width=1130, height=596, fg=self.bg)#FAF7F2
        self.ripple.play(self.gifPath)
        self.ripple.place(x = 0 , y = 0)

        if self.parent.avatars == {}:
            self.parent.createAvaterSelector()

        self.userIcon = popUpButton(parent=self, img=self.parent.userImg)
        self.userIcon.place(543,306)

        self.parent.root_mshare.bind("<Configure>" , self.updatePopUpIcon)
        self.parent.root_mshare.bind("<FocusIn>" , self.updatePopUpIcon)
        self.parent.root_mshare.bind("<FocusOut>" , self.hidePopUpIcon)

        self.UserCount = 0

        self.searchSender = SearchSender(self)
        self.startScanning()



    def createAvtrOnSearch(self, name, userId, DevId, imgName, IP):
        isFound = False
        for obj in self.PopupWinObg:
            data = obj.getData()

            log("Data===;;;;=>", data)

            userId2 = data[1]
            DevId2 = data[2]
            IP2 = data[4]


            if userId2 == userId and DevId2 == DevId:
                log(f"Same users is connected UserId={userId2} and DevId2={DevId2} and PrevIP = {IP2} and New={IP}")
                obj.IP.append(IP)
                isFound = True
                break

        if not isFound:
            log("Not Found PrevsId...")
            if ".png" not in imgName:
                avt = imgName+'.png'
            else:
                avt = imgName

            if avt in self.parent.avatars:
                img = self.parent.avatars[avt]
            else:
                img = self.parent.avatars["007.png"]

            print("IP====>", IP)

            self.create_PopUpButton(name, userId, DevId, img, avt, IP, self.avtarButton )


    def avtarButton(self, butObj):
        #['Lakshay Saini', 'lakshaySaini12@', '98420njd98sudnw98kjdwn4HJNEWIU3982', '018.png', '192.168.56.1']
        data = butObj.getData()
        log(f"dataAvt==>{data}")
        ip = data[4]
        devId = data[2]
        self.searchSender.stop = True

        self.client = Client(self, ip)
        self.client.connectToServer()

        saveInfo = self.parent.saveInfo["user"]

        fData = f"--handShake--{saveInfo['name']}||{saveInfo['userId']}||{saveInfo['devId']}||{saveInfo['avt']}"
        self.client.send(fData)
        
        conf = self.client.recv(100)
        print("Conf===>", conf)
        enc = conf.split("---")[1]

        if f"ok--{saveInfo['userId']}---" in conf:
            print(f"Enc===============> {enc}")

            recvWin = Recieve(self.parent, data, self.client)#initializing recv window

            if enc == "True":
                print("Encrytion is on.....")
                key = self.parent.loginwindow.getKeysUsingDevID(devId)

                if not key:
                    print("Please Verify your id....")
                    key = None
                    return 0

                self.client.isEncryption = True
                self.client.encryptKey = rsa.PublicKey._load_pkcs1_pem(key)

                if self.client.checkEncryption():
                    print("00000000000000====>  Encryption in working on client side")

                else:
                    messagebox.showerror("Error in key pair",
                            "     Error in Verifying keyPairs...\n     Please check manually...")
                    sys.exit(0)
                
            log("+++++++++connected.........")


            self.parent.root_mshare.unbind("<Configure>")
            self.parent.root_mshare.unbind("<FocusIn>" )
            self.parent.root_mshare.unbind("<FocusOut>" )
            try:
                self.container.pack_forget()

                for obj in self.PopupWinObg:
                    obj.destroy()
            except Exception as e:
                print(e)
            ['Aditya Mukhiya', 'mahadevadityamukhiya@', 'mshare94984jhshjw93423', '001.png', ['192.168.56.1']]
            recvWin.createRecvWin()
        else:
            print("Error not foind conf..")

    def startScanning(self):
        self.searchSender.stop = False
        Thread(target=self.searchSender.run, daemon=True).start()

    def showScanProgress(self):
        self.scanProgVal += 1
        if self.scanProgVal == 7:
            self.scanProgVal = 1
        self.status.config(text=f"Scanning{ '.' * self.scanProgVal}")
    

    def enterMode(self, event):
        self.modeBut.config(image=self.local_hov)

    def leaveMode(self, event):
        self.modeBut.config(image=self.local_nor)  

    def globalButtonCmd(self):
        print("GLobal Button") 
        messagebox.showinfo("Feature Error...",
                            "     This feature is not  yet  available  for  use. This  feature is\n     currently planned or already in the development process\n     and will be available immediately when released.\n     Thanks for your patience.")
        self.modeButCommand("local")


    def modeButCommand(self, mode):
        print("Mode Button....")

        r = None
        if  mode == "global" and self.modeValue != 'global':
            r = range(0, 6)
            self.modeValue = "global"
            
        elif mode == 'local' and self.modeValue !=  'local':
            self.modeValue = "local"
            r = range(5, -1, -1)
        else:
            print(f"Already in {mode}")
        
        if r:
            for i in r:
                self.modeButLeft.config(image=self.shotsList1[i])
                self.modeButRight.config(image=self.shotsList2[i])
                self.parent.root_mshare.update()
                sleep(0.008)
            
            if self.modeValue == "global":
                self.globalButtonCmd()
            else:
                pass

 

    def hidePopUpIcon(self,event):
        print(event)
        for obj in self.PopupWinObg:
            obj.hide()

    

    def updatePopUpIcon(self, event):
        for obj in self.PopupWinObg:
            obj.configure_place()






       
    def create_PopUpButton(self, name, userId, DevId, img, avt, IP , cmd):
        allCord = []
        for obj in self.PopupWinObg:
            allCord.append( self.reverse_Y(obj.getPlaceInfo())) 

        userIcon = popUpButton( self, name, userId, DevId, img, avt, IP , cmd)
        
        cord = self.randomCodinates(allCord, None, None, userIcon)
        print(f"COrd==> {cord}")
        userIcon.place(cord[0], cord[1])
        userIcon.configure_place()


    def randomCodinates(self, allCord, w, h, userIcon):
        x = random.randrange(self.minwidth, self.maxWidth)
        y = random.randrange(self.minHeight, self.maxHeight)
        if w == None:
            userIcon.place(x,y)
            self.parent.root_mshare.update()
            w = userIcon.scrn.winfo_width()
            h = userIcon.scrn.winfo_height()
            userIcon.hide()

        cord = self.reverse_Y([ x, y+h, x+w, y])
        st = False
        for oneCord in allCord:
            if self.isOverlap(cord, oneCord):
                st = True
                break
        
        if st:
            print("overlapping.......")
            return self.randomCodinates(allCord, w, h, userIcon)
        else:
            return (x, y)


    def isOverlap(self, rect1 , rect2):
        return rect1[0] < rect2[2] and rect2[0] < rect1[2] and rect1[1] < rect2[3] and rect2[1] < rect1[3]


    def reverse_Y(self, rect):
        rect[1] = abs(rect[1]-self.screenHeight)
        rect[3] = abs(rect[3]-self.screenHeight)
        return rect
    


