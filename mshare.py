from tkinter import *
import ctypes , os , sys
import tkinter.ttk as ttk
from threading import Thread
from functools import partial as functools_partial
from login import LoginPage
from ripple import FindSenderWin
from sendwin import Send
from util import resource_path
from popup_win import menuPopUp


class App():
    def __init__(self):        
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        
        self.loginwindow = LoginPage()
        # self.loginwindow.writeData("dkjflk")

        if self.loginwindow.authenticate():
            print("Authencated.....")
        else:
            sys.exit(1)

        self.bg="grey3"
        bg = self.bg
        self.root_mshare = Tk()
        self.root_mshare.wm_resizable(False, False)
        self.root_mshare.tk.call('tk', 'scaling', 2.0)
        self.icon=PhotoImage(file = resource_path("data/share64.png"), master=self.root_mshare )
        self.root_mshare.iconphoto(True,self.icon)
        self.root_mshare.title('M_share ..')
        self.root_mshare.geometry('1200x634+200+100')

        self.start_frame=Frame(self.root_mshare,bg=bg)
        self.start_frame.pack(fill='both', expand=True)

        self.receive_img= PhotoImage(file = resource_path("data/rec.png"),master=self.root_mshare)
        self.receive_but=Button(self.start_frame,highlightbackground=bg, image=self.receive_img,
                        bd=0,compound='right',activebackground='grey6',cursor='hand2', bg=bg,
                        command=self.receive_but_command)
        self.receive_but.pack(side='left', ipadx=20, expand=True)

        self.send_img= PhotoImage(file = resource_path("data/send2.png"),master=self.root_mshare)
        self.send_but=Button(self.start_frame,highlightbackground=bg,image=self.send_img,bd=0,
                        compound='right',activebackground='grey6',cursor='hand2',bg=bg,
                         command=self.send_but_command)
        self.send_but.pack(side='right', ipadx=20, expand=True)
        

        self.root_mshare.protocol("WM_DELETE_WINDOW", self.on_closing_root)
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("black.Horizontal.TProgressbar", background='royalblue',thickness=4)

        #____User__Account__________
        self.frameUser = Frame(self.root_mshare,bg=bg, width=700, height=70)
        self.saveInfo = self.loginwindow.getData()
        self.userImg = PhotoImage(file = resource_path(f"data/avatar/{self.saveInfo['user']['avt']}"),master=self.root_mshare)
        self.userLab = Button(self.frameUser, highlightbackground=bg, image=self.userImg,
                        bd=0,compound='right',activebackground='grey8',cursor='hand2', bg=bg,
                        command=self.userCommand)
        self.userLab.place(x=0, y=0)

        self.userID = Label(self.frameUser, text= self.saveInfo['user']['email'], bg=bg, fg="grey80",compound='right', bd=0, anchor="w", 
                            justify='left', font=("yu gothic ui", 13, "bold"))
        self.userID.place(x=80, y=0)

        self.userName = Label(self.frameUser, text=self.saveInfo['user']['name'], bg=bg, fg="grey40",compound='right', bd=0, anchor="w", 
                            justify='left', font=("Helvetica", 9, "bold"))
        self.userName.place(x=85, y=37)

        self.menuButtonImg= PhotoImage(file = resource_path("data/menu2.png"), master=self.root_mshare)

        self.menuButton = Button(self.start_frame, highlightbackground=bg, image=self.menuButtonImg,
                        bd=0,compound='right', activebackground='grey8',cursor='hand2', bg=self.bg,
                        command = self.menuButCommand)
        self.menuButton.place(x=1155, y=15)



        self.avatars = {}
        self.avatarsFileList = []

        self.isAvatarWinhide = True
        self.root_mshare.bind_all("<Control-l>", self.loginwindow.logout)

        self.frameUser.place(x=30, y=20, bordermode = 'outside')
        dark_title_bar(self.root_mshare)
        self.root_mshare.mainloop()



    def menuButCommand(self, ):
        print("MoreButton....")
        x = self.root_mshare.winfo_x()
        y = self.root_mshare.winfo_y()

        x1 = self.menuButton.winfo_x() + self.menuButton.winfo_width() -  30
        y1 = self.menuButton.winfo_y() + self.menuButton.winfo_height() + 20

        pop = menuPopUp(x+x1, y+y1, 330, 350, self)

    def backCommand(self):
        self.start_frame.pack(fill='both', expand=True)

    def userCommand(self):
        if self.avatars == {}:
            self.createAvaterSelector()
        
        if self.isAvatarWinhide:
            self.avatarWin.place_configure(x=110, y=55, bordermode = 'outside')
            self.isAvatarWinhide = False
        else:
            self.avatarWin.place_forget()
            self.isAvatarWinhide = True

    def createAvaterSelector(self):
        bg = "white"
        self.avatarWin = Frame(self.root_mshare, bg=bg, width=500, height=300)

        path = resource_path("data/avatar/")
        n=0
        c=18
        side = "left"
        row = 0
        column = 0
        for file in os.listdir(path):
            fullPath = path+file
            self.avatars[file] = PhotoImage(file = fullPath, master=self.root_mshare) 
            self.avatarsFileList.append(file)       

            Button(self.avatarWin, highlightbackground = bg, image = self.avatars[file],
                            bd=0,activebackground=bg,cursor='hand2', bg=bg,
                            command = functools_partial (self.chooseImg , file)).grid(row=row, column=column,padx=10,pady=10)
            n += 1
            column += 1
            if column == 6:
                column = 0
                row += 1



    def chooseImg(self, fileName):
        self.userImg = self.avatars[fileName]
        self.userLab.configure(image=self.userImg)
        data = self.loginwindow.getData()
        data["user"]["avt"] = fileName
        self.loginwindow.writeData(data)
        self.avatarWin.place_forget()
        self.isAvatarWinhide = True
        Thread(target=self.loginwindow.updateIcon, args=(fileName,), daemon = True).start()


    def send_but_command(self):
        print('send_but_command')
        self.start_frame.pack_forget()
        send = Send(self)


    def receive_but_command(self):
        print("Recv button")
        self.start_frame.pack_forget()
        win = FindSenderWin(self)
        # data = ['Aditya Mukhiya', 'mahadevadityamukhiya@', 'mshare94984jhshjw93423', '001.png', ['192.168.56.1']]
        # recvWin = Recieve(self, data, "")



    def on_closing_root(self):
        self.root_mshare.destroy()
        sys.exit(1)
    

def dark_title_bar(window):
    window.update()
    
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ctypes.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ctypes.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ctypes.byref(value),
                         ctypes.sizeof(value))


if __name__ == "__main__":
    app = App()

