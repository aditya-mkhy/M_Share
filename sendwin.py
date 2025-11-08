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
from popup_win import  moreButnPopupServerSide
from server import Server
from util import log, timeCal, data_size_cal, getTime, getdate, resource_path
from tkinter import messagebox
from login import LoginPage


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
    def play(self, path, avt, parent, loc=None):
        if loc ==None:
            loc = (24,18)
        self.pause = False
        self.parent = parent
        img = Image.open(path)
        avt = Image.open(avt)
        self.indx = 0
        self.frames = []

        for i in range(img.n_frames):
            img.seek(i)
            img.paste(avt, loc, mask = avt)
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
        self.progContBg = "#2d2121"
        self.timeStamp = timeStamp
        self.maxVal = maxVal

        name = name

        print("time==>",timeSt)
    
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

        self.video_name=Label(self.progCont, text=name, bg=self.progContBg, fg='white', font=('yu gothic ui',10,"bold"), anchor="w",
                        width=56, bd=0, justify="left")

        self.video_name.place(x=34,y=18)

        self.progress_bar = Progressbar(self.progCont, length=612, style="black.Horizontal.TProgressbar",
                          maximum=self.maxVal, value=0, mode="determinate", orient="horizontal")            
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



class Send:
    def __init__(self,parent):

        print('recive')
        self.parent=parent
        self.winMode = False

        self.bg = "#060606"
        self.bg2 = "#171313"
        self.bg3 = "#282727"
        self.ButtonFrameBg = "#090808"
        self.recvAnimationGif = resource_path("data/arrow.gif")

        self.sendFrame=Frame(self.parent.root_mshare, bg=self.bg)
        self.sendFrame.pack(expand=True,fill='both')


        self.frame3=Frame(self.sendFrame, bg=self.bg2)
        self.frame3.pack(expand=True, fill='both', side='right')

        self.menu=Frame(self.sendFrame, bg=self.bg)

        self.menu.pack(fill='both', side='left', ipadx=600)



        #======= User Information =========
        
        self.moreImg = PhotoImage(file = resource_path("data/more.png"), master=self.parent.root_mshare)
        self.moreBut = Button(self.menu, highlightbackground=self.bg, image=self.moreImg,
                        bd=0,compound='right', activebackground='grey20',cursor='hand2', bg=self.bg,
                        command=self.menuCommand)
        self.moreBut.place(x=1155, y=5)

        self.backImg = PhotoImage(file = resource_path("data/backward.png"), master=self.parent.root_mshare)
        self.back = Button(self.menu, highlightbackground=self.bg, image=self.backImg,
                        bd=0,compound='right', activebackground='grey20',cursor='hand2', bg=self.bg,
                        command=self.backRecvWinCmd)
        self.back.place(x=5, y=5)

        self.loginwindow = LoginPage()
        self.saveData = self.loginwindow.getData()
        


        ### ======  Sender Avtar  =========##
        self.sendAvt = resource_path(f"data/avatar2/{self.saveData['user']['avt']}")

        self.senderImg = PhotoImage(file=self.sendAvt, master=self.parent.root_mshare)


        self.RippleGIF = resource_path("data/senderRipple.gif")

        self.senderIcon = genRippleLabel(self.menu, highlightbackground=self.bg, image=self.senderImg,
                        bd=0,compound='right',cursor='hand2', bg=self.bg,)
        
        self.senderIcon.play(self.RippleGIF, self.sendAvt, self.parent.root_mshare, loc=(194,177))
        self.senderIcon.place(x=336, y=38)

        self.senderName = Label(self.menu, text="Waiting For Reciever", bg=self.bg, fg="cyan3",compound='right', bd=0,
                            justify='center', font=("freeserif", 13, "bold italic"), width=29)
        self.senderName.place(x=360, y=560)

        
        self.server = Server(self)
        self.startServer()

        # self.sendFrame.after(10, self.connected, data)

        #FilesData
        self.sendFilesObj = {}
        self.sendFilesList = []

    def addToHistory(self, filePath, timeStamp):
        userId = self.recvData[1]
        self.saveData = self.loginwindow.getData()
        self.saveData["sendHist"][userId].append([filePath,timeStamp])#Adding filePath& timestamp in histroy
        self.loginwindow.writeData(self.saveData)

    def addHistoryToWindow(self):
        if self.saveData["servSetting"]["showHistry"]:
            userId = self.recvData[1]
            files = self.saveData["sendHist"][userId]
            for file in files:
                log(f"File==>{file}")
                basename = os.path.basename(file[0])
                if len(basename) > 55:
                    name = f"{basename[:52]}....{basename[len(basename) -3:]}"
                else:
                    name = basename

                timest = f"Done..."
                status = f"{getdate(float(file[1]))} at {getTime(float(file[1]))}"
                timestamp = file[1]
                obj = createProgressBar(self, avt=self.recvAvt, name=name, value=10, maxVal=10, timeSt=timest, speed=status, timeStamp=timestamp, side="bottom")
        else:
            print("Show history is turned off.....")
           


    def askIsAllowedToConnect(self, data):
        # [userName, userId, devId, icon]
        print(f"DRAR==> {data}")
        self.recvData = data
        userId = self.recvData[1]
        if userId in self.saveData["access"]:
            log(f"{userId}  have access to connect automatically")
            if userId in self.saveData["sendHist"]:
                log("Hostory Found")
            else:
                self.saveData = self.loginwindow.getData()
                self.saveData["sendHist"][userId] = []
                self.loginwindow.writeData(self.saveData)
            return True

        else:

            q = messagebox.askyesno("Incomming Connection...",  f"   hey! {data[0]} wants to connect with you, to recieve files.\n   userId = {data[1]}. \n   Would you like to allow?")
            if q:
                self.saveData = self.loginwindow.getData()
                self.saveData["access"][userId]=data[3]
                self.saveData["sendHist"][userId] = []
                self.loginwindow.writeData(self.saveData)

            return q
        
    def startServer(self):
        self.server.stopBroadcast = False
        self.server.runTh()

    def connected(self, data):
        log(f"++++++++++++++++++++Data=893==>{data}")
        self.recvData = data
        # [userName, userId, devId, icon]

        self.createRestObjcetAfterConnecting()
        self.menuFrameAnimation(0)
        
       

    def afterCreatingObjects(self):
        Thread(target=self.server.recvWhile, daemon=True).start()
        print("Server is receiving data")

    def disconnectCall(self): # This function is called by server whenever connection is disconnected
        print("Send win disconnect function is called")
        self.menuToSenderFrameAnimation(0)


    def disconnectButPressed(self, event=None):
        print("Imam worling....")
        self.server.disconnect(action=100)
        

    def destroyRestObjectAfterDisconnecting(self):
        self.HistoryFrame.destroy()
        self.infoFrame.destroy()
        self.ButtonFrame.destroy()

    def menuFrameAnimation(self, num):
        y = self.senderIcon.winfo_y()
        x = self.senderIcon.winfo_x()

        if num < 50:
            self.senderIcon.place_configure(x=x-2, y=y-1)

        elif num == 50:
            self.senderName.config(text= self.saveData['user']['name'], font=("Helvetica", 11, "bold"), fg="grey60")

            self.senderName.place_configure(x =((x+192)-125), y=(y+176)+135)
            self.senderIcon.destroy()

            self.senderIcon = Label(self.menu, highlightbackground=self.bg, image=self.senderImg,
                        bd=0,compound='right', bg=self.bg)
            
            self.senderIcon.place(x=x+192, y=y+176)
            
        else:

            self.senderIcon.place_configure(x=x-2, y=y-1)
            self.senderName.place_configure(x =((x-2)-125), y=(y-1)+135)

            if num == 190:

                #=== Recieve Animation Repel  ======#
                self.recvAnimi = RippleLabel(self.menu, bg=self.bg, fg=self.bg, bd=0)
                self.recvAnimi.play(self.recvAnimationGif)
                self.recvAnimi.place(x=140, y=178)

            if num == 160:
                #===== Reciever Avtar ==========#

                # self.senderImg = PhotoImage(file=resource_path("data/avatar2/001.png"), master=self.parent.root_mshare)

                self.recvAvt = resource_path(f"data/avatar2/{self.recvData[3]}")
                self.recvImg = PhotoImage(file = self.recvAvt, master=self.parent.root_mshare)

                RippleGIF = resource_path("data/backRipple.gif")
                self.recvIcon = genRippleLabel(self.menu, highlightbackground=self.bg, image=self.recvImg,
                                bd=0,compound='right',cursor='hand2', bg="green")
                self.recvIcon.play(RippleGIF, self.recvAvt, self.parent.root_mshare)
                self.recvIcon.place(x=105, y=338)


                self.recvrName = Label(self.menu, text=self.recvData[0], bg=self.bg, fg="grey60",compound='right', bd=0,
                                    justify='center', font=("Helvetica", 11, "bold"), width=29)
                self.recvrName.place(x=5, y=512)




        self.moreBut.place_configure(x=(1155 - (4*num)), y=5)
        self.menu.pack_configure(ipadx=(600 - (2*num)))

        self.parent.root_mshare.update()

        num += 1

        if num != 200:
            self.menu.after(0, self.menuFrameAnimation,num)

        else:
            self.afterCreatingObjects()
            self.sendFrame.after(10, self.addHistoryToWindow)



    def menuToSenderFrameAnimation(self, num):

        y = self.senderIcon.winfo_y()
        x = self.senderIcon.winfo_x()

        if num < 150:

            self.senderIcon.place_configure(x=x+2, y=y+1)
            self.senderName.place_configure(x =((x+2)-125), y=(y+1)+135)
            #=== Recieve Animation Repel  ======#

            if num == 8:
                try:
                    self.recvAnimi.destroy()
                except:
                    pass
            elif num == 60:
                try:
                    self.recvrName.destroy()
                except:
                    pass
            elif num == 70:
                try:
                    self.recvIcon.destroy()
                except:
                    pass



        elif num == 150:

            self.senderName.place_configure(x =340, y=560)
            self.senderName.config(text= "Waiting For Reciever", font=("freeserif", 13, "bold italic"))
            self.senderIcon.destroy()

            self.senderIcon = genRippleLabel(self.menu, highlightbackground=self.bg, image=self.senderImg,
                            bd=0,compound='right',cursor='hand2', bg=self.bg,)
            
            self.senderIcon.play(self.RippleGIF, self.sendAvt, self.parent.root_mshare, loc=(194,177))

            # self.senderIcon.place(x=336, y=38)
            
            self.senderIcon.place(x=x-192, y=y-176)
            # self.menu.after(300, self.createRestObjcetAfterConnecting)

            
        else:            
            self.senderIcon.place_configure(x=x+2, y=y+1)


        self.moreBut.place_configure(x=((4*num)+355), y=5)
        self.menu.pack_configure(ipadx=((2*num)+200))

        self.parent.root_mshare.update()

        num += 1

        if num != 200:
            self.menu.after(0, self.menuToSenderFrameAnimation,num)
        else:
            self.destroyRestObjectAfterDisconnecting()
          


    def createRestObjcetAfterConnecting(self):

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
                               font =("yu gothic ui", 9, "bold"), justify="right", width=19, compound="right", anchor="e")
        self.speedLab.place(x=595, y=12)
        

        self.fileHistoryFrame = Frame(self.HistoryFrame, bg=self.bg2)
        self.fileHistoryFrame.pack(expand=True, fill='both', side='bottom', pady=0)

        self.ButtonFrame = Frame(self.frame3, bg=self.ButtonFrameBg)
        self.ButtonFrame.pack(fill='both', side='bottom', ipady=30)

        #=== Button Frame  ======##
        # self.disconnectImg = PhotoImage(file =resource_path("data/disconnect.png"), master=self.parent.root_mshare)
        # self.disconnectImgHover = PhotoImage(file =resource_path("data/disconnecthover.png"), master=self.parent.root_mshare)

        # self.disconnectLab = Label(self.ButtonFrame, image=self.disconnectImg,
        #                 bd=0,compound='right', cursor='hand2', bg=self.ButtonFrameBg)
        # self.disconnectLab.place(x=10, y=5)

        # self.disconnectBut = Button(self.ButtonFrame, text="Disconnect", highlightbackground="#0E0EDB",
        #                 bd=0, activebackground="#0E0EDB",cursor='hand2', bg="#0E0EDB",activeforeground="#e2470f", fg="white",relief="flat",
        #                 command= self.disconnectButPressed, font=("ui-sans-serif", 13, "bold"), height=1, width=10)
        # self.disconnectBut.place(x=38, y=14)

        # self.disconnectBut.bind("<Enter>", self.disconnectButEnter)
        # self.disconnectBut.bind("<Leave>", self.disconnectButLeave)





        # self.totalLab = Label(self.ButtonFrame, text="Reciev : 2000GB",bd=0, bg=self.ButtonFrameBg, fg="grey70", 
        #                         font=("yu gothic ui", 9, "bold"), justify="left", width=19, compound="left", anchor="w")
        # self.totalLab.place(x=590, y=30)


        #======   Buttons in ButtonFrame  ===============
        self.openFileButLabImg = PhotoImage(file =resource_path("data/buttonBackOpenFile.png"), master=self.parent.root_mshare)

        # === Select Files Button
        self.openFileButLab = Label(self.ButtonFrame, image=self.openFileButLabImg,
                        bd=0,compound='right', cursor='hand2', bg=self.ButtonFrameBg)
        self.openFileButLab.place(x=20, y=3)

        self.openFileButImg = PhotoImage(file = "data/filesimg.png", master=self.parent.root_mshare)
        self.openFileBut = Button(self.ButtonFrame, text="Select Files", highlightbackground="#252020", image=self.openFileButImg,
                        bd=0,compound='left', activebackground="#252020", cursor='hand2', bg="#252020", fg="white",
                        command=self.selectFiles, font=("yu gothic ui", 10, "bold"), padx=5, activeforeground="grey60")
        self.openFileBut.place(x=40, y=8)#filesimg


        # Select Folder Button
        self.openFolderButLab = Label(self.ButtonFrame, image=self.openFileButLabImg,
                        bd=0,compound='right', cursor='hand2', bg=self.ButtonFrameBg)
        self.openFolderButLab.place(x=220, y=3)

        self.openFolderButImg = PhotoImage(file = "data/open.png", master=self.parent.root_mshare)
        self.openFolderBut = Button(self.ButtonFrame, text="  Folder", highlightbackground="#252020", image=self.openFolderButImg,
                        bd=0,compound='left', activebackground="#252020", cursor='hand2', bg="#252020", fg="white",
                        command=self.selectFolder, font=("yu gothic ui", 10, "bold"), padx=5, activeforeground="grey60")
        self.openFolderBut.place(x=242, y=8)#filesimg


        # Send Button
        self.sendFileButLab = Label(self.ButtonFrame, image=self.openFileButLabImg,
                        bd=0,compound='right', cursor='hand2', bg=self.ButtonFrameBg)
        self.sendFileButLab.place(x=590, y=3)

        self.sendFileButImg = PhotoImage(file = "data/file-transfer.png", master=self.parent.root_mshare)
        self.sendFileBut = Button(self.ButtonFrame, text="Send Files", highlightbackground="#252020", image=self.sendFileButImg,
                        bd=0,compound='left', activebackground="#252020", cursor='hand2', bg="#252020", fg="white",
                        command=self.sendFilesCmd, font=("yu gothic ui", 10, "bold"), padx=5, activeforeground="grey60")
        self.sendFileBut.place(x=612, y=8)


        # self.disconnectFileButLab = Label(self.ButtonFrame, image=self.openFileButLabImg,
        #                 bd=0,compound='right', cursor='hand2', bg=self.ButtonFrameBg)
        # self.disconnectFileButLab.place(x=420, y=3)

        # self.disconnectFileButImg = PhotoImage(file = "data/file-transfer.png", master=self.parent.root_mshare)
        # self.disconnectFileBut = Button(self.ButtonFrame, text="Diconnect", highlightbackground="#252020", image=self.disconnectFileButImg,
        #                 bd=0,compound='left', activebackground="#252020", cursor='hand2', bg="#252020", fg="white",
        #                 command="", font=("yu gothic ui", 10, "bold"), padx=5, activeforeground="grey60")
        # self.disconnectFileBut.place(x=444, y=8)


        ##========  scroll window ==============

        self.scrollWinCanvas = Canvas(self.fileHistoryFrame, bg=self.bg2, bd=0, closeenough=0, highlightthickness=0, confine=1, width=0)
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


        name = "Neerja.720p.theMoviesmod.in.mkv........"
        download_status = "(0 KB of 0 MB , 50.7 KB/s)"
        timest = "2:20 Mint"
 
        avrt = resource_path(f"data/avatar2/001.png")

        self.progressBarList = []

        
        ct = time.time()

        # for i in range(10):
        #     createProgressBar(self, avrt, "Mahadev....mkv", 80, timest, download_status, ct-(86400*i), side="bottom")

        # createProgressBar(self, avrt, "Aditya Mukhiya.mkv", 20, timest, download_status, ct-(86400*10), side="bottom")

        # for i in range(10):
        #     createProgressBar(self, avrt, name, 40, timest, download_status, ct-(86400*(i*80)), side="bottom")

        # Opening Files............
        self.frame3.bind_all("<Control-o>", self.selectFiles)
        self.frame3.bind_all("<Control-f>", self.selectFolder)



    def sendFilesCmd(self, event=None):
        if self.sendFilesList != []:
            self.sendFileBut.config(command="", fg="cyan2", text="Sending...")
            path = self.sendFilesList.pop()
            self.server.sendFile(path)
        else:
            messagebox.showinfo("Mshare", "     Please select some files to send.\n     ( using [select file] button or Ctrl+o)")


    
    def selectFolder(self, event=None):
        folder=askdirectory(title='Select Folder')
        print(folder)

        paths = self.all_file_in_folder(folder)
        self.AddFiles(paths)

    def selectFiles(self, event=None):
        paths=askopenfilenames(title = "Select Files")
        print(paths)
        self.AddFiles(paths)

    def AddFiles(self, paths):
        timestamp = time.time()
        timest = "Waiting..."


        for path in paths:
            basename = os.path.basename(path)
            if len(basename) > 55:
                name = f"{basename[:52]}....{basename[len(basename) -3:]}"
            else:
                name = basename

            timestamp = time.time()
            size = os.stat(path).st_size

            download_status = f"Files Size : {data_size_cal(size)}"

            obj = createProgressBar(self, avt=self.recvAvt, name=name, value=0, maxVal=size, timeSt=timest, speed=download_status, timeStamp=timestamp, side="bottom")
            self.sendFilesObj[path] = obj
            self.sendFilesList.append(path)

        if not self.server.stillSending:
            log("stillSending===> False")
            if self.saveData['servSetting']['sendFileOnAdd']:
                log("SendOnAdd  is running")
                self.sendFilesCmd()
                
        else:
            log("stillSending===> True")


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


  
    def backRecvWinCmd(self):
        print("BackWard...............")
        self.server.shutdownServer()
        self.sendFrame.place_forget()
        self.parent.backCommand()
        self.sendFrame.destroy()


    
    def menuCommand(self, ):
        x = self.parent.root_mshare.winfo_x()
        y = self.parent.root_mshare.winfo_y()

        x1 = self.moreBut.winfo_x() + self.moreBut.winfo_width()
        y1 = self.moreBut.winfo_y() + self.moreBut.winfo_height()+40

        pop = moreButnPopupServerSide(x+x1, y+y1, 330, 500, self)
        

    def userButtonCommand(self):
        print("UseButtonCOmmand is pressed.....")

    def all_file_in_folder(self,folder_name):
        all_file_list=[]        
        def folder_dec(folder_name):
            if os.path.exists(folder_name):
                try:
                    folder_content=os.listdir(folder_name)
                    for file in folder_content:
                        file=folder_name+'/'+file
                        if os.path.isfile(file):
                            nonlocal all_file_list
                            all_file_list.append(file)
                        elif os.path.isdir(file):
                            folder_dec(file)
                        else:
                            pass
                except:
                    pass
            else:
                pass
        folder_dec(folder_name)
        return all_file_list