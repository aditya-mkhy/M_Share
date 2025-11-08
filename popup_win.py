from tkinter import *
import os, sys
from time import sleep
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
from threading import Thread
from tkinter.filedialog import   askdirectory 
from util import log, formatPath, resource_path


def custom_shape_canvas(parent=None,width=300,height=100,rad=50,padding=3,bg='red'):
    color=bg
    cornerradius=rad
    rad = 2*cornerradius
    parent.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,
                           padding+cornerradius,padding,width-padding-cornerradius,padding,
                           width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,
                           width-padding-cornerradius,height-padding,padding+cornerradius,height-padding),
                          fill=color, outline=color)

    parent.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color,
                      outline=color)
    parent.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90,
                      fill=color, outline=color)
    parent.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270,
                      extent=90, fill=color, outline=color)
    parent.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90,
                      fill=color, outline=color)
    

class Toogle():
    def __init__(self,parent, cmd, idd=None) -> None:
        self.parent = parent
        self.bg = "#252323"
        self.onImg = []
        self.offImg = []
        self.cmd = cmd
        self.idd = idd
        self.state = False
        for i in range(2, 10):
            self.onImg.append( PhotoImage(file =resource_path(f"data/switch{i}.png"), master=self.parent) )

        for i in range(10, 16):
            self.offImg.append( PhotoImage(file =resource_path(f"data/switch{i}.png"), master=self.parent) )


        self.lab = Label(self.parent, bd=0, image=self.offImg[5], compound='left', bg=self.bg)
        self.lab.bind("<Button-1>", self.click)

    def place(self, x=None, y=None):
        self.lab.place(x=x, y=y)

    def on(self, ac=None):
        Thread(target=self.onTh, args=(ac,), daemon=True).start()

    def onTh(self, ac=None):
        for img in self.onImg:
            self.lab.config(image=img)
            self.parent.update()
            sleep(0.04)
        self.state = True
        if ac:
            self.cmd(self.idd, 1)

    def off(self, ac=None):
        Thread(target=self.offTh, args=(ac,), daemon=True).start()

    def offTh(self, ac=None):
        for img in self.offImg:
            self.lab.config(image=img)
            self.parent.update()
            sleep(0.04)
        self.state = False
        if ac:
            self.cmd(self.idd, 0)

    def click(self, event=None):
        if self.state:
            self.off(1)
        else:
            self.on(1)


class  popWind:
    def __init__(self, x, y, width, height,  bg):
        self.width = width
        self.height = height
        self.bg = bg

        self.win = Toplevel()
        self.win.config(bg="red")
        self.win.overrideredirect(True)
        self.win.geometry(f"+{x}+{y}")
        self.win.tk.call('tk', 'scaling', 1.7)

        self.win.wm_attributes('-transparentcolor', 'red')

        self.frame = Canvas(self.win,bg='red',bd=0,  width=self.width, height=self.height, highlightthickness=0)  
        self.frame.pack(fill='both',expand=True, padx=1, pady=1)
        custom_shape_canvas(parent=self.frame,width=self.width, height=self.height, rad=12,padding=0,bg=self.bg)


    
        self.win.bind("<FocusOut>" , self.destroy)
        self.win.focus_force()
        


    def destroy(self, event=None):
        self.win.destroy()
        # exit()

class moreButnPopupClient(popWind):
    def __init__(self, x, y, width, height, parent, align="left"):
        self.parent = parent
        self.bg = "#252323"
        self.bdbg = "grey30"
        self.popUpData = [x, y, width, height, parent]
        if align == "left":
            x= (x-width)+5
        super().__init__(x, y, width, height, self.bg)

        self.data = self.parent.saveData["clintSetting"]


        # self.toogle = Toogle(self.frame)
        # self.toogle.place(x=100, y=100)
        self.secrty = Label(self.frame, text="Data Security", bg=self.bg, fg="#0065ff", font=("Helvetica", 14, "bold italic"), bd=0)
        self.secrty.place(x=20, y=14)

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=46)

        #====Global
        self.globalenc = Label(self.frame, text="Global Encryption", bg=self.bg, fg="snow", font=("Helvetica", 13, ""), bd=0)
        self.globalenc.place(x=20, y=56)

        self.globaltgl = Toogle(self.frame, self.action, "glenc")
        self.globaltgl.place(x=230, y=50)
        if self.data['glenc']:
            self.globaltgl.on()

        #=== Local===
        # self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        # self.bord.place(x=0, y=95)

        self.localenc = Label(self.frame, text="Local Encryption", bg=self.bg, fg="snow", font=("Helvetica", 13, ""), bd=0)
        self.localenc.place(x=20, y=94)

        self.localtgl = Toogle(self.frame, self.action, "lcenc")
        self.localtgl.place(x=230, y=90)
        if self.data['lcenc']:
            self.localtgl.on()

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=135)

        #  ask file location ===
        self.path = Label(self.frame, text="Ask Location", bg=self.bg, fg="snow", font=("Helvetica", 13, ""), bd=0)
        self.path.place(x=20, y=150)
        info = "(Ask where to save each \n file before downloading)"
        self.pathInfo = Label(self.frame, text=info, bg=self.bg, fg="grey60", font=("yu gothic ui",9, ""), bd=0, justify="left")
        self.pathInfo.place(x=18, y=175)

        self.pathtgl = Toogle(self.frame, self.action, "askLoc")
        self.pathtgl.place(x=230, y=145)
        if self.data['askLoc']:
            self.pathtgl.on()

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=222)

        #=== Parallel DOwnloading......

        self.parallel = Label(self.frame, text="Parallel Recieving", bg=self.bg, fg="snow2", font=("Helvetica", 13, ""), bd=0)
        self.parallel.place(x=20, y=237)

        self.paralleltgl = Toogle(self.frame, self.action, "parRecv")
        self.paralleltgl.place(x=230, y=233)
        if self.data['parRecv']:
            self.paralleltgl.on()

        info = "(Use multiple connections to\n download a single file in parts)"
        self.parallelInfo = Label(self.frame, text=info, bg=self.bg, fg="grey60", font=("yu gothic ui",9, ""), bd=0, justify="left")
        self.parallelInfo.place(x=18, y=262)

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=310)

       
        # Show Histroy........

        self.history = Label(self.frame, text="Show History", bg=self.bg, fg="snow2", font=("Helvetica", 13, ""), bd=0)
        self.history.place(x=20, y=322)

        self.historytgl = Toogle(self.frame, self.action, "showHistry")
        self.historytgl.place(x=230, y=316)
        if self.data['showHistry']:
            self.historytgl.on()

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=365)

        ####  Path
        self.basePath = formatPath(self.parent.basePath)


        self.history = Label(self.frame, text=f"            {self.basePath}", bg=self.bg, fg="white", font=("Helvetica", 11, ""), bd=0,
                            justify="left", anchor="w", wraplength=300)
        self.history.place(x=24, y=382)

        self.pathBut = Button(self.frame, text="Path :", highlightbackground=self.bg,
                        bd=0,compound='left', activebackground="#252020", cursor='hand2', bg=self.bg, fg="#0065ff",
                        command=self.choosePath, font=("Helvetica", 12, "bold"), activeforeground="grey60", highlightthickness=0,padx=0,pady=0, relief="flat")
        self.pathBut.place(x=20, y=375)#filesimg

        self.pathBut.bind("<Enter>", self.butEnter)
        self.pathBut.bind("<Leave>", self.butLeave)
        
        self.win.mainloop()

    def butLeave(self, event=None):
        self.pathBut.config(fg="#0065ff")

    def butEnter(self, event=None):
        self.pathBut.config(fg="blue2")

    def choosePath(self):
        path=askdirectory(title='Choose path <where to save file when downloaded>')
        log(f"paths==> {path}")
        self.parent.basePath = path
        self.action("path", path)
        moreButnPopupClient(self.popUpData[0], self.popUpData[1], self.popUpData[2], self.popUpData[3], self.popUpData[4])


    def action(self, idd, value):
        self.parent.saveData = self.parent.loginwindow.getData()
        self.parent.saveData["clintSetting"][idd] = value
        self.parent.loginwindow.writeData(self.parent.saveData)
        print("Status saved")




class moreButnPopupServerSide(popWind):
    def __init__(self, x, y, width, height, parent, align="left"):
        self.parent = parent
        self.bg = "#252323"
        self.bdbg = "grey30"
        if align == "left":
            x= (x-width)+5
        super().__init__(x, y, width, height, self.bg)
        
        self.data = self.parent.saveData["servSetting"]

        # self.toogle = Toogle(self.frame)
        # self.toogle.place(x=100, y=100)
        self.secrty = Label(self.frame, text="Data Security", bg=self.bg, fg="#0065ff", font=("Helvetica", 14, "bold italic"), bd=0)
        self.secrty.place(x=20, y=14)

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=46)

        #====Global
        self.globalenc = Label(self.frame, text="Global Encryption", bg=self.bg, fg="snow", font=("Helvetica", 13, ""), bd=0)
        self.globalenc.place(x=20, y=56)

        self.globaltgl = Toogle(self.frame, self.action, "glenc")
        self.globaltgl.place(x=230, y=50)
        if self.data['glenc']:
            self.globaltgl.on()

        #=== Local===
        # self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        # self.bord.place(x=0, y=95)

        self.localenc = Label(self.frame, text="Local Encryption", bg=self.bg, fg="snow", font=("Helvetica", 13, ""), bd=0)
        self.localenc.place(x=20, y=94)

        self.localtgl = Toogle(self.frame, self.action, "lcenc")
        self.localtgl.place(x=230, y=90)
        if self.data['lcenc']:
            self.localtgl.on()

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=135)

        #  ask file location ===
        self.path = Label(self.frame, text="Send Files on Add", bg=self.bg, fg="snow", font=("Helvetica", 13, ""), bd=0)
        self.path.place(x=20, y=150)
        info = "(Send files automatically \n when they are added)"
        self.pathInfo = Label(self.frame, text=info, bg=self.bg, fg="grey60", font=("yu gothic ui",9, ""), bd=0, justify="left")
        self.pathInfo.place(x=18, y=175)

        self.pathtgl = Toogle(self.frame, self.action, "sendFileOnAdd")
        self.pathtgl.place(x=230, y=145)
        if self.data['sendFileOnAdd']:
            self.pathtgl.on()


        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=222)

        #=== Parallel DOwnloading......

        self.parallel = Label(self.frame, text="Parallel Sending", bg=self.bg, fg="snow2", font=("Helvetica", 13, ""), bd=0)
        self.parallel.place(x=20, y=237)

        self.paralleltgl = Toogle(self.frame, self.action, "parSend")
        self.paralleltgl.place(x=230, y=233)
        if self.data['parSend']:
            self.paralleltgl.on()

        info = "(Use multiple connections to\n Send a single file in parts)"
        self.parallelInfo = Label(self.frame, text=info, bg=self.bg, fg="grey60", font=("yu gothic ui",9, ""), bd=0, justify="left")
        self.parallelInfo.place(x=18, y=262)

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=310)

        # Show Histroy........

        self.history = Label(self.frame, text="Show History", bg=self.bg, fg="snow2", font=("Helvetica", 13, ""), bd=0)
        self.history.place(x=20, y=322)

        self.historytgl = Toogle(self.frame, self.action, "showHistry")
        self.historytgl.place(x=230, y=316)
        if self.data['showHistry']:
            self.historytgl.on()

        self.bord = Frame(self.frame, bg=self.bdbg, width=width, height=1)
        self.bord.place(x=0, y=365)



        # Disconnect Button.......

        self.bgImgDisconnect = PhotoImage(file =resource_path("data/backDisconnect.png"),master=self.frame)

        self.disconnectButLab = Label(self.frame, image=self.bgImgDisconnect,
                        bd=0,compound='right', cursor='hand2', bg=self.bg)
        self.disconnectButLab.place(x=85, y=452)

        self.disconnectBut = Label(self.frame, text="Disconnect", highlightbackground="#393434",
                        bd=0,compound='left', cursor='hand2', bg="#393434", fg="white",
                         font=("yu gothic ui", 12, "bold"))
        self.disconnectBut.place(x=115, y=456)

        self.disconnectBut.bind("<Button-1>", self.disconnect)
        self.disconnectButLab.bind("<Button-1>", self.disconnect)

        self.disconnectBut.bind("<Enter>", self.butEnter)
        self.disconnectBut.bind("<Leave>", self.butLeave)
       
        self.disconnectButLab.bind("<Enter>", self.butEnter)
        self.disconnectButLab.bind("<Leave>", self.butLeave)
       
        self.win.mainloop()


    def action(self, idd, value):
        self.parent.saveData = self.parent.loginwindow.getData()
        self.parent.saveData["servSetting"][idd] = value
        self.parent.loginwindow.writeData(self.parent.saveData)
        print("Status saved")

    def butLeave(self, event=None):
        self.disconnectBut.config(fg="white")

    def butEnter(self, event=None):
        self.disconnectBut.config(fg="grey80")


    def disconnect(self, event=None):
        print("Disconned...")


class menuPopUp(popWind):
    def __init__(self, x, y, width, height, parent, align="left"):
        self.parent = parent
        self.bg = "#252323"
        self.bdbg = "grey30"
        if align == "left":
            x= (x-width)+5
        super().__init__(x, y, width, height, self.bg)
        

        # Logout Button.......

        self.bgImgLogout = PhotoImage(file =resource_path("data/backDisconnect.png"), master=self.frame)

        self.LogoutButLab = Label(self.frame, image=self.bgImgLogout,
                        bd=0,compound='right', cursor='hand2', bg=self.bg)
        self.LogoutButLab.place(x=85, y=300)

        self.LogoutBut = Label(self.frame, text="Logout", highlightbackground="#393434",
                        bd=0,compound='center', cursor='hand2', bg="#393434", fg="#d44d1c",
                         font=("Helvetica", 13, "bold"))
        self.LogoutBut.place(x=130, y=306)

        self.LogoutBut.bind("<Button-1>", self.Logout)
        self.LogoutButLab.bind("<Button-1>", self.Logout)

        self.LogoutBut.bind("<Enter>", self.butEnter)
        self.LogoutBut.bind("<Leave>", self.butLeave)
       
        self.LogoutButLab.bind("<Enter>", self.butEnter)
        self.LogoutButLab.bind("<Leave>", self.butLeave)
       
        self.win.mainloop()


    def action(self, idd, value):
        self.parent.saveData = self.parent.loginwindow.getData()
        self.parent.saveData["servSetting"][idd] = value
        self.parent.loginwindow.writeData(self.parent.saveData)
        print("Status saved")

    def butLeave(self, event=None):
        self.LogoutBut.config(fg="#d44d1c")

    def butEnter(self, event=None):
        self.LogoutBut.config(fg="#f65920")


    def Logout(self, event=None):
        self.parent.loginwindow.logout()


if __name__ == "__main__":
    pop = moreButnPopupServerSide(900, 200, 330, 500)