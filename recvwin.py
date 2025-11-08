from tkinter import *
import ctypes , os , sys , socket
from random import choice , randint
from tkinter.filedialog import  askopenfilenames , askdirectory 
import tkinter.ttk as ttk
from threading import Thread
import time
from functools import partial as functools_partial

from PIL import Image, ImageTk
import random
from tkinter.ttk import Style as ttk_Style,Progressbar,Scale as ttk_Scale

from popup_win import moreButnPopupClient
from util import log, timeCal, data_size_cal, getTime, getdate, formatPath, resource_path
from client import Client
from login import LoginPage
from pathlib import Path





class RippleLabel(Label):
    def play(self, path):
        self.pause = False
        img = Image.open(path)
        self.indx = 0
        self.frames = []

        for i in range(img.n_frames):
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


class genRippleLabel(Label):
    def play(self, path, avt, parent):
        self.pause = False
        self.parent = parent
        img = Image.open(path)
        avt = Image.open(avt)
        self.indx = 0
        self.frames = []

        for i in range(img.n_frames):
            img.seek(i)
            img.paste(avt, (24,18), mask = avt)
            self.frames.append(ImageTk.PhotoImage(img.copy()))


        try:
            self.delay = img.info['duration']
            self.delayDefault = img.info['duration']
        except:
            self.delay = 100

        self.frames.pop(0)
        self.next_frame()

    def next_frame(self):
        self.indx += 1
        self.indx %= len(self.frames)

        if not self.pause:
            self.config(image=self.frames[self.indx])
            self.after(self.delay, self.next_frame)

def genProgAvtImage(avt):
    path = resource_path("data/avtBack.png")
    img = Image.open(path)
    avt = Image.open(avt)
    avt2 = avt.resize((87,87), Image.LANCZOS )
    img.paste(avt2, (11,12), mask = avt2)
    return ImageTk.PhotoImage(img)


class createProgressBar:
    def __init__(self, parent, avt=None, name=None, value=None, maxVal=None, timeSt=None, speed=None, timeStamp=None, side="bottom"):
        self.avt = avt
        self.parent = parent
        self.maxVal = maxVal
        self.name = name
        self.progContBg = "#2d2121"
        self.timeStamp = timeStamp

        
    
        self.progFrame = Frame(self.parent.scrollFrame, bg=self.parent.bg2, bd=0)
        self.progFrame.pack(side=side, padx=0, pady=5)
        

        self.progCont = Canvas(self.progFrame,  bd=0, bg=self.progContBg, closeenough=0, highlightthickness=0, confine=1,
                    width=689, height=130)
        self.progCont.create_image(0, 0, anchor=NW, image=self.parent.progBgImg)
        self.progCont.pack(side="left", padx=0)

        try:
            self.parent.progAvtrStore[self.avt]
        except:
            self.parent.progAvtrStore[avt] = genProgAvtImage(self.avt)

        self.progAvtCont = Label(self.progFrame, image=self.parent.progAvtrStore[self.avt], bd=0, compound='left', bg=self.progContBg)
        self.progAvtCont.pack(side="right", padx=0)

        ##===== Items of porgressbar =====
        print("Self.Name==>", self.name)

        self.video_name=Label(self.progCont, text=self.name, bg=self.progContBg, fg='white', font=('yu gothic ui',10,"bold"), anchor="w",
                        width=56, bd=0, justify="left")

        self.video_name.place(x=34,y=18)

        self.progress_bar = Progressbar(self.progCont, length=612, style="black.Horizontal.TProgressbar",
                          maximum=self.maxVal, value=value, mode="determinate", orient="horizontal")            
        self.progress_bar['value'] = value
        self.progress_bar.place(x=36, y=54)
        

        self.time_left=Label(self.progCont, text=timeSt, bg=self.progContBg, fg='white',font=('',9), anchor="w", justify="left")
        self.time_left.place(x=34,y=64)

            
                
        self.down_status=Label(self.progCont, text=speed, bg=self.progContBg, fg='white', font=('',9), anchor="e",
                            width=35, justify="right",)
        self.down_status.place(x=294,y=64)

        #Binding Scroll 
        self.progFrame.bind("<MouseWheel>", lambda event : self.parent.scroll(event))
        self.progCont.bind("<MouseWheel>", lambda event : self.parent.scroll(event))
        self.progAvtCont.bind("<MouseWheel>", lambda event : self.parent.scroll(event))

        self.video_name.bind("<MouseWheel>", lambda event : self.parent.scroll(event))
        self.progress_bar.bind("<MouseWheel>", lambda event : self.parent.scroll(event))
        self.time_left.bind("<MouseWheel>", lambda event : self.parent.scroll(event))
        self.down_status.bind("<MouseWheel>", lambda event : self.parent.scroll(event))

        self.update(name=self.name)
        self.parent.progressBarList.append(self)

    def update(self, name=None, value=None, timeSt=None, speed=None, timeStamp=None, avtSide=None):
        if name:
            basename = os.path.basename(name)
            if len(basename) > 55:
                name = f"{basename[:52]}....{basename[len(basename) -3:]}"
            else:
                name = basename
            self.video_name.config(text=name)

        if value:
            self.progress_bar['value'] = value
        if timeSt:
            self.time_left.config(text=timeSt)
        if speed:
            self.down_status.config(text=speed)
        if self.timeStamp:
            self.timeStamp = timeStamp

        if avtSide:
            if avtSide == "left":
                self.progAvtCont.pack_configure(side="left", padx=0)
                self.progCont.pack_configure(side="right", padx=0)
            elif avtSide == "right":
                self.progAvtCont.pack_configure(side="right", padx=0)
                self.progCont.pack_configure(side="left", padx=0)
            else:
                log("Erorr :902> Invalid Side...")

    def getPos(self):
        return (self.progFrame.winfo_y(), self)
    
class CButton(Label):
    def __init__(self, master, text="", backGroundLabel=None, bg=None, compound=None, cursor="hand2", fg="grey45", font=("", 20), image=None, justify="left", 
                 padx=0, pady=0,  fbg=None, ffg=None, command=None) -> None:
        
        super().__init__(master, bd=0, bg=bg, compound=compound, cursor=cursor, fg=fg, font=font, image=image, justify=justify,  padx=padx, pady=pady, relief="flat", text=text)
        self.command = command
        self.bind("<Enter>", self.butEnter)
        self.bind("<Leave>", self.butLeave)
        self.bg = bg
        self.fg = fg
        self.ffg = ffg
        self.fbg = fbg

        if backGroundLabel:
            backGroundLabel.bind("<Button-1>", self.commandCall)
        self.bind("<Button-1>", self.commandCall)

    def commandCall(self, event=None):
        self.command()
    
    def butLeave(self, event=None):
        if self.ffg:
            self.config(fg=self.fg)
      
    def butEnter(self, event=None):
        if self.ffg:
            self.config(fg=self.ffg)

    
class Recieve():
    def __init__(self, parent, data, client: Client):

        print('recive')
        self.parent=parent
        self.Sendrdata = data
        self.client = client
        self.client.parent = self
        print("DATA======>",self.Sendrdata)
        self.loginwindow = LoginPage()
        self.saveData = self.loginwindow.getData()

        


    def createRecvWin(self):
        self.bg = "#060606"
        self.bg2 = "#171313"
        self.bg3 = "#282727"
        self.ButtonFrameBg = "#090808"
        self.recvAnimationGif = resource_path("data/arrow.gif")

        self.recvFrame=Frame(self.parent.root_mshare,bg=self.bg)
        self.recvFrame.pack(expand=True,fill='both')


        self.frame3=Frame(self.recvFrame, bg=self.bg2)
        self.frame3.pack(expand=True, fill='both', side='right')

        self.menu=Frame(self.recvFrame, bg=self.bg)
        self.menu.pack(fill='both', side='left', ipadx=200)

        self.HistoryFrame = Frame(self.frame3, bg=self.bg2)
        self.HistoryFrame.pack(expand=True, fill='both', side='top')

        self.infoFrame = Frame(self.HistoryFrame, bg=self.bg3)
        self.infoFrame.pack(fill='both', side='top', ipady=25)

        self.timeImg = PhotoImage(file = resource_path("data/time.png"), master=self.parent.root_mshare)

        self.timeInfoCan = Canvas(self.infoFrame,  bd=0, bg="red", closeenough=0, highlightthickness=0, confine=1,
                    width=168, height=47)
        self.timeInfoCan.create_image(0, 0, anchor=NW, image=self.timeImg)
        self.timeInfoCan.place(x=280, y=0)

        self.timeInfo = Label(self.timeInfoCan, text="Today" , bd=0, justify='center', bg="#353333", fg="grey85",
                                font=("Helvetica", 10, ""), width=11)
        self.timeInfo.place(x=24, y=12)
        
        #======Speedd  label
        self.speedLab = Label(self.infoFrame, text="Speed : 20GB/s",bd=0, bg=self.bg3, fg="#e2470f",##e2470f 
                                font=("yu gothic ui", 9, "bold"), justify="right", width=19, compound="right", anchor="e")
        self.speedLab.place(x=595, y=12)

        self.fileHistoryFrame = Frame(self.HistoryFrame, bg=self.bg2)
        self.fileHistoryFrame.pack(expand=True, fill='both', side='bottom', pady=0)

        self.ButtonFrame = Frame(self.frame3, bg=self.ButtonFrameBg)
        self.ButtonFrame.pack(fill='both', side='bottom', ipady=30)

        #======= User Information =========
        
        self.moreImg = PhotoImage(file = resource_path("data/more.png"), master=self.parent.root_mshare)
        self.moreBut = Button(self.menu, highlightbackground=self.bg, image=self.moreImg,
                        bd=0,compound='right', activebackground='grey20',cursor='hand2', bg=self.bg,
                        command=self.menuCommand)
        self.moreBut.place(x=355, y=5)

        self.backImg = PhotoImage(file = resource_path("data/backward.png"), master=self.parent.root_mshare)
        self.back = Button(self.menu, highlightbackground=self.bg, image=self.backImg,
                        bd=0,compound='right', activebackground='grey20',cursor='hand2', bg=self.bg,
                        command=self.backRecvWinCmd)
        self.back.place(x=5, y=5)




        ### ======  Sender Avtar =========##
        self.Senderavt = resource_path(f"data/avatar2/{self.Sendrdata[3]}")

        self.senderImg = PhotoImage(file=self.Senderavt, master=self.parent.root_mshare)

        self.senderLab = Button(self.menu, highlightbackground=self.bg, image=self.senderImg,
                        bd=0,compound='right', activebackground='grey20',cursor='hand2', bg=self.bg,
                        command=self.userButtonCommand)
        self.senderLab.place(x=130, y=15)


        self.senderName = Label(self.menu, text=self.Sendrdata[0], bg=self.bg, fg="grey60",compound='right', bd=0,
                            justify='center', font=("Helvetica", 11, "bold"), width=29)
        self.senderName.place(x=5, y=150)

        #=== Recieve Animation Repel  ======#

        self.recvAnimi = RippleLabel(self.menu, bg=self.bg, fg=self.bg, bd=0)
        self.recvAnimi.play(self.recvAnimationGif)
        self.recvAnimi.place(x=140, y=178)

        RippleGIF = resource_path("data/backRipple.gif")

        #===== Reciever Avtar ==========#

        # self.senderImg = PhotoImage(file=resource_path("data/avatar2/001.png"), master=self.parent.root_mshare)

        self.recvAvt = resource_path(f"data/avatar2/{self.saveData['user']['avt']}")
        self.recvImg = PhotoImage(file = self.recvAvt, master=self.parent.root_mshare)

        self.recvLab = genRippleLabel(self.menu, highlightbackground=self.bg, image=self.recvImg,
                        bd=0,compound='right',cursor='hand2', bg="green")
        self.recvLab.play(RippleGIF, self.recvAvt, self.parent.root_mshare)
        self.recvLab.place(x=105, y=332)


        self.recvrName = Label(self.menu, text=self.saveData['user']['name'], bg=self.bg, fg="grey60",compound='right', bd=0,
                            justify='center', font=("Helvetica", 11, "bold"), width=29)
        self.recvrName.place(x=5, y=505)


        #===//////// Button Frame  ======##
      
        self.ButBgLabImg = PhotoImage(file =resource_path("data/buttonBackOpenFile.png"), master=self.parent.root_mshare)

        # === Disconnect  Button
        self.disconnectButLab = Label(self.ButtonFrame, image=self.ButBgLabImg,
                        bd=0,compound='right', cursor='hand2', bg=self.ButtonFrameBg)
        self.disconnectButLab.place(x=20, y=3)

        self.disconnectButImg = PhotoImage(file = "data/no-internet.png", master=self.parent.root_mshare)
        self.disconnectBut = Button(self.ButtonFrame, text="Disconnect", highlightbackground="#252020", image=self.disconnectButImg,
                        bd=0,compound='left', activebackground="#252020", cursor='hand2', bg="#252020", fg="white",
                        command=self.disconnectButCmd, font=("yu gothic ui", 10, "bold"), padx=3, activeforeground="grey60")
        self.disconnectBut.place(x=40, y=8)#filesimg


        # self.totalLab = Label(self.ButtonFrame, text="Reciev : 2000GB",bd=0, bg=self.ButtonFrameBg, fg="grey70", 
        #                         font=("yu gothic ui", 9, "bold"), justify="left", width=19, compound="left", anchor="w")
        # self.totalLab.place(x=590, y=40)


        ##========  scroll window ==============

        self.scrollWinCanvas = Canvas(self.fileHistoryFrame, bg=self.bg2, bd=0, closeenough=0, highlightthickness=0, confine=1)
        self.scrollWinCanvas.pack(fill="both", expand=True, side="top")
                               
        self.scrollFrame =Frame(self.scrollWinCanvas, bg=self.bg2)


        self.scrollFrame.bind("<Configure>",lambda e: self.scrollWinCanvas.configure(
            scrollregion=self.scrollWinCanvas.bbox("all")))

        self.scrollWinCanvas.create_window((0, 0), window=self.scrollFrame, anchor="nw")

        self.scrollWinCanvas.bind("<MouseWheel>", lambda event : self.scroll(event))
        self.fileHistoryFrame.bind("<MouseWheel>", lambda event : self.scroll(event))
        self.scrollFrame.bind("<MouseWheel>", lambda event : self.scroll(event))


        ## ==== ProgrressBar ===========
        self.style_Scale = ttk_Style(self.parent.root_mshare)
        self.style_Scale.theme_use('alt')
        self.style_Scale.configure("black.Horizontal.TProgressbar", background='royalblue', thickness=5, foreground="black")

        self.progBgImg = PhotoImage(file = resource_path("data/backprog.png"), master=self.parent.root_mshare)
        self.progAvtrStore = {}


        ####  Path
        self.basePath = self.saveData["clintSetting"]["path"]

        if not os.path.exists(self.basePath):
            self.basePath = f"{Path.home()}\\Downloads"
        log(f"Paths===> {self.basePath}")



        self.SerderAvtrForProg = resource_path(f"data/avatar2/{self.Sendrdata[3]}")
        self.progressBarList = []
        self.recvFrame.after(10, self.addHistoryToWindow)
        
        self.client.recvWhileThr()
    


    def disconnectButCmd(self, event=None):
        log("Disconnect........")
        self.client.disconnect()
        self.disconnectBut.config(text="Re-Connect", command=self.reConnect)

    def reConnect(self):
        print("Reconnecting.....")

        
        
    def addToHistory(self, filePath, timeStamp):
        userId = self.Sendrdata[1]
        self.saveData = self.loginwindow.getData()
        try:
            self.saveData["recvHist"][userId].append([filePath,timeStamp])#Adding filePath& timestamp in histroy
        except Exception as e:
            print("Eroor[09023] :-", e)
            self.saveData["recvHist"][userId] = [[filePath,timeStamp]]
        self.loginwindow.writeData(self.saveData)
        print("data saved.......")

    def addHistoryToWindow(self):
        if self.saveData["clintSetting"]["showHistry"]:

            userId = self.Sendrdata[1]
            try:
                files = self.saveData["recvHist"][userId]
            except:
                files = []
                
            for file in files:
                print(f"File==>{file}")
                basename = os.path.basename(file[0])
                if len(basename) > 55:
                    name = f"{basename[:52]}....{basename[len(basename) -3:]}"
                else:
                    name = basename

                timest = f"Done..."
                status = f"{getdate(float(file[1]))} at {getTime(float(file[1]))}"
                timestamp = file[1]
                obj = createProgressBar(self, avt=self.Senderavt, name=name, value=10, maxVal=10, timeSt=timest, speed=status, timeStamp=timestamp, side="bottom")
        else:
            print("Show history is turned off")
           


    def createProgBar(self, name, value, maxVal, timest, speed, timestamp):

        print(name, value, maxVal, timest, speed, timestamp)
        return createProgressBar(self, self.SerderAvtrForProg, name, value, maxVal, timest, speed, timestamp)

    def scroll(self, event):
        self.scrollWinCanvas.yview("scroll",-1*int(event.delta/120),"units")
        y0 = int(self.scrollWinCanvas.canvasy(0))-100
        height = 150

        for prog in self.progressBarList:
            y , obj = prog.getPos()
            y2 = y+height

            if y > y0 and y2 < y0+300:
                t = obj.timeStamp
                self.timeInfo.config(text=getdate(t))


    def disconnectButLeave(self, event):
        self.disconnectLab.config(image=self.disconnectImg)

    def disconnectButEnter(self, event):
        self.disconnectLab.config(image=self.disconnectImgHover)


    def backRecvWinCmd(self):
        print("BackWard...............")
        self.client.disconnect()
        self.recvFrame.place_forget()
        self.parent.backCommand()
        self.recvFrame.destroy()

    
    def menuCommand(self, ):
        x = self.parent.root_mshare.winfo_x()
        y = self.parent.root_mshare.winfo_y()

        x1 = self.moreBut.winfo_x() + self.moreBut.winfo_width()
        y1 = self.moreBut.winfo_y() + self.moreBut.winfo_height()+40

        pop = moreButnPopupClient(x+x1, y+y1, 330, 500, self)
        

    def userButtonCommand(self, obj):
        data = obj.getData()
        print("Data==>", data)
