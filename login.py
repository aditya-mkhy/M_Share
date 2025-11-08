from tkinter import *
from tkinter import messagebox
from json import loads
from requests import get as requests_get
import os ,sys,subprocess

from webbrowser import open as open_file
from PIL import ImageTk, Image

import io as io_import
from cryptography.fernet import Fernet
import socket
from threading import Thread
from time import time, sleep
from util import log, resource_path

from random import choice
import rsa

#======================  LoginPage  ==================================
#=====================================================================
class LoginPage:
    def __init__(self):
        self.app = "mshare"
        self.key = b'I22SNTKzZ_6Jpp1SDqRr_rBDxDISvc66VX0FtdLSog4='
        self.fileKey = b'cyWZoMAFZAEdugp_KjO-ODmnIwTfVvt9jGdJF0xB3oc='
        self.uuid = self.GetUUID()
        self.dataFile = resource_path("data/logs.mpl")
        self.keyFile = resource_path("data/logs2.mpl")
        self.authState = False
        self.version = "3.0.0"
        self.icon = "data/share64.png"
        self.host = "https://mahadevadity8080.pythonanywhere.com"

    def createWindow(self):
        self.window = Tk()
        self.window.title('Login Page.')
        self.window.resizable(False, False)

        self.window.geometry(f"{1166}x{718}+{int((self.window.winfo_screenwidth()/2)-(1166/2))}+{int((self.window.winfo_screenheight()/2) - (850/2))}")

        self.phototitle = PhotoImage(file =resource_path(self.icon),master=self.window)
        self.window.iconphoto(True, self.phototitle)
        # ============================background image============================
        self.bg_frame = Image.open( resource_path('data/back.png'))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.window, bg='#040405',width=950, height=600)
        self.lgn_frame.place(x=200, y=70)

    
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief="flat")
        self.heading.place(x=80, y=30, height=50)

        # ============ Left Side Image ================================================
        self.side_image = Image.open(resource_path('data/vector.png'))
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ============ Sign In Image =============================================
        self.sign_in_image = Image.open(resource_path('data/desk.png'))
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405', fg="#040405")
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=640, y=110)

        # ============ Sign In label =============================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="grey90",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

        # ============================username====================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.userVar = StringVar()
        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief="flat", bg="#040405", fg="white",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground="grey75", textvariable=self.userVar)
        self.username_entry.place(x=580, y=335, width=280)

        self.username_line = Canvas(self.lgn_frame, width=310, height=2.0, bg="goldenrod", highlightthickness=0)
        self.username_line.place(x=550, y=363)
        # ===== Username icon =========
        self.username_icon = Image.open(resource_path('data/username_icon.png'))
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=336)
        # # ============================Forgot password=============================
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password?",
                                    font=("yu gothic ui", 10, "bold underline"), fg="#064097", relief="flat",
                                    activebackground="#040405"
                                    , borderwidth=0, background="#040405", cursor="hand2", command=self.forgotPassword)
        self.forgot_button.place(x=705, y=441)
        self.forgot_button.bind("<Enter>", lambda event: self.forgot_button.configure(fg="#3380f3"))
        self.forgot_button.bind("<Leave>", lambda event: self.forgot_button.configure(fg="#064097"))

        # ============================password====================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=385)

        self.passwdVar = StringVar()
        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief="flat", bg="#040405", fg="white",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground="grey75", textvariable=self.passwdVar)
        self.password_entry.place(x=580, y=416, width=265)

        self.password_line = Canvas(self.lgn_frame, width=310, height=2.0, bg="goldenrod", highlightthickness=0)
        self.password_line.place(x=550, y=447)
        # ======== Password icon ================
        self.password_icon = Image.open(resource_path('data/password_icon.png'))
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405', fg="#040405")
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=420)
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage(file=resource_path('data/show.png'))

        self.hide_image = ImageTk.PhotoImage(file=resource_path('data/hide.png'))

        self.show_button = Button(self.lgn_frame, image=self.hide_image, command=self.show, relief="flat",
                                  activebackground="#040405", fg="#040405"
                                  , borderwidth=0, background="#040405", cursor="hand2")
        self.show_button.place(x=835, y=420)

        # ============================login button================================
        self.photoLogin = ImageTk.PhotoImage(file=resource_path("data/login.png"))

        self.login_label = Label(self.lgn_frame, image=self.photoLogin, relief="flat",
                                  activebackground="#040405", fg="#040405"
                                  , borderwidth=0, background="#040405")
        self.login_label.place(x=573, y=480)

        self.login_button = Button(self.lgn_frame, text="Login", bg="#0065ff", fg="white",bd=0, relief="flat",cursor="hand2",
                                    font=( "", 14, 'bold'), height=0, width=13, pady=0, command=self.login,
                                    activebackground="#0065ff",)
        self.login_button.place(x=605, y=484)

        self.login_button.bind("<Enter>", lambda event: self.changeColor(fg="#bfbfbf"))
        self.login_button.bind("<Leave>", lambda event: self.changeColor(fg="white"))
        # =========== Sign Up ==================================================
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=("yu gothic ui", 10, "bold"), justify="center",
                                relief="flat", borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=580, y=552)


        self.signup_button = Button(self.lgn_frame, text="Sign Up Now",
                                    font=("yu gothic ui", 10, "bold underline"), fg="#120fc2", relief="flat",
                                    activebackground="#040405", command=self.signUp
                                    , borderwidth=0, background="#040405", cursor="hand2")
        self.signup_button.place(x=720, y=545)
        self.signup_button.bind("<Enter>", lambda event: self.signup_button.configure(fg="#0b099b"))
        self.signup_button.bind("<Leave>", lambda event: self.signup_button.configure(fg="#120fc2"))

        self.window.mainloop()

    def autor(self, event=None, dosleep=False):
        if dosleep:
            sleep(10)
        r=Tk()
        r.config(bg='grey15')
        r.title('Aditya_Mukhiya_@Author_email- Mahadevadityamukhiya@gmail.com')
        t='''@ Commands\n
    1) To Download a video :
        
        cmd==> --v--[video_url]
        eg. => --v--https://www.youtube.com/watch?v=KgIdiHMlcM4

    2) TO Dowload a playlist :

        cmd==> [playlisturl]---[resolution]---[ video_list ]

        Examples:
        
            i) To download all video in playlist in highest resolution:

                    cmd==> [playlisturl]
                    Eg. ==> https://www.youtube.com/playlist?list=PL15uBSlY9G2wFiInO9eJvB0dqfSCvhRXa
                
            ii) To dowload all video in playlist in specific resolution:
                    cmd==> [playlisturl]---[resolution]
                    Eg. ==> https://www.youtube.com/playlist?list=PL15uBSlY9G2wFiInO9eJvB0dqfSCvhRXa---720p

            iii)To dowload selected video in playlist in specific resolution:
                    cmd==> [playlisturl]---[resolution]---[ video_list ]
                    Eg. ==> https://www.youtube.com/playlist?list=PL15uBSlY9G2wFiInO9eJvB0dqfSCvhRXa---720p---[ 2,4,5,7 ]    

    '''
        l=Label(r,text=t,bg='grey15',fg='white',font=('',12), anchor="e", justify='left').pack()
        r.mainloop()

    def changeColor(self, fg):
        if self.login_button["fg"] == "#bfbfbf" or self.login_button["fg"] == "white":
            self.login_button.configure(fg=fg)


    def GetUUID(self):
        try:
            # Run the PowerShell command to get UUID
            result = subprocess.run(
                ["powershell", "-Command", "(Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            uuid = result.stdout.strip()
            return uuid
        except Exception as e:
            print(f"Error retrieving UUID: {e}")
            return None



    def decrypt(self, key, data) -> str:
        f = Fernet(key)
        decrypted = f.decrypt(data)
        return decrypted.decode()

    def encrypt(self, key, data) -> str:
        f = Fernet(key)
        encrypted = f.encrypt(data.encode())
        return encrypted.decode()

    def urlParse(self, passwd):
        np=""
        for w in passwd:
            if w== " ":
                np+="%20"
            else:
                np+=w
        return passwd

    def color_change_enter_leave(event=None,bg=None,fg=None):
        print("event==>", event)
        if event==None:
            pass
        else:
            try:
                if bg != None:
                    event.widget['bg']=bg
                if fg!= None:
                    event.widget['fg']=fg
            except Exception as e:
                print(e)

    def show(self):
        self.show_button.place_forget()
        self.hide_button = Button(self.lgn_frame, image=self.show_image, command=self.hide, relief="flat",
                                  activebackground="#040405", fg="#040405"
                                  , borderwidth=0, background="#040405", cursor="hand2")
        self.hide_button.place(x=835, y=420)
        self.password_entry.config(show='')
        

    def hide(self):
        self.hide_button.place_forget()
        self.show_button = Button(self.lgn_frame, image=self.hide_image, command=self.show, relief="flat",
                                  activebackground="#040405", fg="#040405"
                                  , borderwidth=0, background="#040405", cursor="hand2")
        self.show_button.place(x=835, y=420)
        self.password_entry.config(show='*')

    def validateEmail(self, mail) -> bool:
        data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_@."
        #Step__1
        if "." in mail and "@" in mail:
            d=0
            a=0
            for w in mail:
                if w not in data:
                    return False
                if w == ".":
                    d+=1
                if w == "@":
                    a+=1
            if d == 1 and a == 1 and mail.find(".") > mail.find("@"):
                return True
            return False      
        return False


    def isOnline(self):
        try:
            s  = socket.socket()
            # we = socket.gethostbyname("pythonanywhere.com")
            # print(f"name==> {we}")
            s.settimeout(0.5)
            s.connect(("pythonanywhere.com",443))
            s.close()
            return True
        except:
            return False
    
    def sendFeedBack(self, msg):
        msg = self.encrypt(self.key, msg)
        user = self.encrypt(self.key, self.getData()["user"])
        try:
            req = requests_get(f"{self.host}/authapp?action=feed&user={user}&app={self.app}&msg={msg}", timeout=2)
            print("Req==>", req.text)
            if req.text == "True":
                return 58
            else:
                return 53
        except Exception as e:
            s=self.isOnline()
            print("Online-====:",s )
            if s:
                print("Connected")
                return 54
            print("Disconnedt")
            return 55  

    def login(self, event=None):
        email = self.userVar.get().strip()
        passwd = self.passwdVar.get().strip()

        if self.validateEmail(email):
            if passwd != "":

                self.login_button.configure(text="Processing..", fg="goldenrod")
                self.window.update()
                print("=======================================")
                print("================  LOGIN  ==============")
                print("  Email ==> ", email)
                print("  Passwd==> ", passwd)
                print("=======================================")
                uud = self.GetUUID()
                uud = uud[len(uud)-10:]
                ud = self.encrypt(self.key, uud)
                email = self.encrypt(self.key, email)
                passwd = self.encrypt(self.key, passwd)

                try:
                    print(f"{self.host}/mshare?action=login&user={email}&pwd={passwd}&ud={ud}&app={self.app}")
                    req = requests_get(f"{self.host}/mshare?action=login&user={email}&pwd={passwd}&ud={ud}&app={self.app}")
                    print("Req==>", req.text)
                except Exception as e:
                    print("e==>",e)
                    if self.isOnline():
                        self.passwdVar.set("")
                        self.login_button.configure(text="Login", fg="white")
                        self.window.update()
                        messagebox.showinfo("Server Message", "     Unfortunately the site is down for a bit of maintenance right\n     now.  But soon we'll be up and the sun will shine again.")
                        return 0

                    self.login_button.configure(text="TryAgain", fg="red")
                    self.window.update()
                    messagebox.showinfo("Login", "     Computer not connected. Make sure your computer has an\n     active Internet Connection")
                    return 0
                try:
                    conf = self.decrypt(self.key, req.text.encode()).split("---")
                    #status---user---id--name
                    name = conf[3].split(' ')[0]
                    err0r = False
                    try:
                        sessionId = conf[4]
                        devId = conf[5]
                        avt = conf[6]
                    except:
                        if conf[0] == "8080":
                            err0r = True

                    if conf[1] != email and conf[2] !="89087777766877" or err0r:
                        self.login_button.configure(text="TryAgain", fg="red")
                        self.passwdVar.set("")
                        messagebox.showerror("Login", "     PROTOCOL ERROR   \n     Please Try Agan After Some time.   ")

                    elif conf[0] =="2054":
                        self.login_button.configure(text="Login", fg="white")
                        self.passwdVar.set("")
                        messagebox.showinfo("Login", f"     Hey! {name}, your email is not verified.\n     Please verify your email first.  ")

                    elif conf[0] =="4020":
                        self.login_button.configure(text="Login", fg="white")
                        messagebox.showinfo("Login", f"     Sorry! {name}, your password was incorrect.\n     Please double-check your password and try again. \n                              OR \n\n     Click the Forgot Password link to reset password.")

                    elif conf[0] =="4080":
                        self.login_button.configure(text="Login", fg="white")
                        self.passwdVar.set("")
                        messagebox.showinfo("Login", "     The username you entered doesn't belong to an account.   \n     Please check your username and try again,  ")

                    elif conf[0] == "8080":

                        self.passwdVar.set("")
                        self.login_button.configure(text="Authenticated", fg="#80f80f", command="")
                        self.heading.configure(text=f"Welcome {conf[3]}", fg="goldenrod")
                        userId = conf[1][:conf[1].find("@")+1]

                        data = {
                            "uuid" : self.uuid,
                            "user" :
                            {
                                        "name" : conf[3],
                                        "userId" : userId,
                                        "email" : conf[1],
                                        "devId" : devId,
                                        "sessionId" : sessionId,
                                        "avt" : avt,
                                    },

                            "servSetting" : {
                                        "glenc" : 0,
                                        "lcenc" : 0,
                                        "sendFileOnAdd" : 0,
                                        "parSend" : 1,
                                        "unAuthAcss" : 0,
                                        "showHistry" : 1,
                                    },

                            "clintSetting" : {
                                        "glenc" : 1,
                                        "lcenc" : 0,
                                        "askLoc" : 0,
                                        "parRecv" : 1,
                                        "showHistry" : 1,
                                        "path" : "",

                                    },

                            "sendHist" : {
                                    },

                            "recvHist" : {
                                    },

                            "access" : {},
                            "actions" : [],
                            }
                        
                        self.login_button.configure(text="initializing", fg="#80f80f", command="")
                        self.window.update()
                        print("Generating...pucblic keys.....")
                        if self.create_Public_Private_Key(data):
                            self.writeData(data)
                            self.login_button.configure(text="Login Success", fg="#80f80f", command="")
                            self.window.update()
                            self.authState = True
                            Thread(target=self.close, daemon=True).start()
                        else:
                            messagebox.showerror("Login Error","     Something went wrong.   \n    Please Try Agan After Some time.   ")

                        # Thread(target=self.autor, args=(None,True), daemon=True).start()

                except Exception as e:
                    print(e)
                    self.passwdVar.set("")
                    self.login_button.configure(text="TryAgain", fg="red")
                    messagebox.showerror("Login Error","     Something went wrong.   \n    Please Try Agan After Some time.   ")
    
            else:
                messagebox.showerror("Password Error","   Please enter password....   ")
        else:
            if email == "":
                messagebox.showinfo("Email","     Please enter Email address  \n     Email Address is required to sign in   ")
            else:
                messagebox.showerror("Email Error","     Sorry, we don't recognise this email address.   \n     Please enter a valid Email address")

    def create_Public_Private_Key(self, saveData : dict = None):
        public_key, private_key = rsa.newkeys(1205)
        public_key2, private_key2 = rsa.newkeys(1200)

        public_key = public_key._save_pkcs1_pem().decode()
        public_key2 = public_key2._save_pkcs1_pem().decode()

        data = f"{saveData['user']['sessionId']}===={public_key}===={public_key2}"

        req = requests_get(f"{self.host}/mshare?action=login&key={self.encrypt(self.key, data)}&app={self.app}")
        print("Req==>", req.text)

        if req.text == "True":

            saveData = {
                "mylpk" : private_key._save_pkcs1_pem().decode(),
                "mygpk" : private_key2._save_pkcs1_pem().decode(),
                "local" : {},
                "global" : {},
            }
            self.saveKeys(saveData)
            return True

        return False


    def signUp(self, event=None):
        print("signUp")
        open_file("https://mahadevadity8080.pythonanywhere.com/signup")

    def forgotPassword(self, event=None):
        email = self.userVar.get().strip()
        print("forgotPassword")
        if self.validateEmail(email):
            open_file(f"https://mahadevadity8080.pythonanywhere.com/passwordReset?email={email}")
        else:
            open_file(f"https://mahadevadity8080.pythonanywhere.com/passwordReset")

    def getData(self) -> dict:
        with open(self.dataFile, "rb") as ff:
            return loads((str(self.decrypt(self.fileKey, ff.read()))).replace("'",'"'))
        
        

    def writeData(self, data) -> bool:
        with open(self.dataFile, "wb") as tf:
            tf.write(self.encrypt(self.fileKey, str(data)).encode())
        return 1
    
    def getKeys(self) -> dict:
        with open(self.keyFile, "rb") as ff:
            return loads((str(self.decrypt(self.fileKey, ff.read()))).replace("'",'"'))

    def saveKeys(self, data) -> bool:
        with open(self.keyFile, "wb") as tf:
            tf.write(self.encrypt(self.fileKey, str(data)).encode())
        return 1
    

    def getKeysUsingDevID(self, devId, fromWeb = False):
        print(f"SearchDevId==> {devId}")
        key = None
        if not fromWeb:
            try:
                key = self.getKeys()["local"]["devId"].encode()
            except:
                key = None

        if self.isOnline():
            data = f"{genSessionId()}---{devId}---{genSessionId()}"
            try:
                r = requests_get(f"{self.host}/mshare?action=getPublicKey&data={self.encrypt(self.key, data)}&app={self.app}")
                txt = self.decrypt(self.key, r.text.encode())
                if "--Key--" in txt:
                    key = txt.replace("--Key--", "").encode()
                    print(f"Key====> {key}")
                    return key

                elif "notExists":
                    print("User is Not Exists......")
                    return False

            except:
                return False
        else:
            messagebox.showinfo("Public Key", "     Computer not connected. Make sure your computer has an\n     active Internet Connection to get Public Key")
            return False

        


        

    def logout(self, event=None):

        data = {"uuid" : "None",
                "user" :{}}
        self.writeData(data)
        self.saveKeys({})
        print("Logout......")
        path = sys.executable
        open_file(path)
        sys.exit(1)

    def close(self):
        sleep(3)
        self.window.destroy()
    

    def authenticate(self) -> bool:
        data = self.getData()
        if data['user'] != {}:
            if data["uuid"] == self.uuid:
                Thread(target=self.checkVersion, daemon=True).start()
                return True
        self.createWindow()
        if self.authState:
            path = sys.executable
            open_file(path)
        sys.exit(1)
    
    def actions(self):
        print("Performing Actions......")
        data = self.getData()
        performAct = data["actions"]
        for action in performAct:
            if action == "icon":
                self.updateIcon(data["user"]["avt"], action=True)


    
    def updateIcon(self, icon, action=False):
        print("Updating  icon....................")
        dataInfo = self.getData()["user"]
        data = f"{dataInfo['sessionId']}---{icon}---jhuiheuh748928ufhryhhehhhehdfhjdyf48778u7757932798577hfrhhhjhryhheyhhre"
        try:
            r = requests_get(f"{self.host}/mshare?action=updateIcon&data={self.encrypt(self.key, data)}&app={self.app}")
            if r.text == "True":
                if action:
                    data = self.getData()
                    data["actions"].remove("icon")
                    self.writeData(data)
                print("Icon Updated.....")
                return True
        
        except Exception as e:
            print("Error[90] Icon updating", e)
            if not action:
                data = self.getData()
                if "icon" not in data["actions"]:
                    log(f"Icon not found in actions list")
                    data["actions"].append("icon")
                    self.writeData(data)
            return False
        
    def genSessionId(self, len_ = 50, idList= []):
        data = "zxcvbnmasdfghjklqwertyuiop1234567890@ZXCVBNMASDFGHJKLQWERTYUIOP&&&&"
        id_ = ""
        for i in range(len_):
            id_ += choice(data)
        
        if id_ in idList:
            genSessionId(len_, idList)
        else:
            return id_


    def checkVersion(self):
        sleep(2)
        try:
            print("Checking version....")
            data = self.getData()["user"]
            r = requests_get(f"{self.host}/mshare?action=version&user={self.encrypt(self.key, data['email'])}&app={self.app}")
            ver = self.decrypt(self.key, r.text.encode()).replace("hghjhg67gjhgh67ygjhgiy6gyyhgyttdserdversion====>", "")
            if self.version == ver:
                print("------------->UPDATED")
            else:
                print(f"------------->Latest Verion={ver} , Please UpDate {self.app}")
                r = messagebox.askyesno("Update Required...",  f"  Hey! {data['name'].split(' ')[0]}, a new version of {self.app} is available.\n  Version={ver} is now available  and You have Version={self.version}\n\n  Would you like to update it now?")
                print("r==>", r)
                if r == True:
                    print("Updating....")
                    open_file("https://mahadevadity8080.pythonanywhere.com/apps")

        except Exception as e:

            print("Error[90]", e)

        self.actions()


    def feedback(self, parent):
        def close(event=None):
            nonlocal feed_wind
            feed_wind.destroy()
                            

        def sent():
            def x():
                nonlocal feed
                feed_wind.destroy()
            nonlocal text_box ,but ,but_close,feed
            print(" calledd....")
            text=text_box.get('1.0','end')
            but.config(text='Sending........................', command="")
            feed.update()
            st = self.sendFeedBack(text)
            but.config( command = thr_sent)
            if st== 55:
                but.config(text='Please, connect to internet and then try again')
                feed_wind.update()
                return 0
            elif st == 58: 
                but.config(text='“Thank You for Your Feedback”')
            elif st == 54:
                but.config(text='Server under maintenance. Please try after some time.', fg="green")
            elif st == 53:
                but.config(text='Something went wrong. Please Try Agan After Some time.")', fg="red")
            else:
                print("Error--FeedBack-unknown-result", st)
            feed_wind.update()
            but.config(command=x)
            

        def thr_sent(event=None):
            th_sent=Thread(target=sent,daemon = True)
            th_sent.start()

        def bouble_click_lab_wid(event=None):
            nonlocal lab_x,lab_y
            lab_x=event.x
            lab_y=event.y
            
        def move_feedback_win(event=None):
            nonlocal feed_wind , lab_x,lab_y
            w=(feed_wind.winfo_geometry()).split('+')
            feed_wind.geometry(('+'+str((int(w[1])+event.x-lab_x))+'+'+str((int(w[2])+event.y)-lab_y)))

        try:

            parent.attributes('-disabled', 1)                      
            feed_wind=Toplevel()
            feed_wind.overrideredirect(True)
            lab_x=0
            lab_y=0
            feed_wind.geometry('+'+str(parent.winfo_width()//4)+'+'+str(parent.winfo_height()//4))
            feed=Frame(feed_wind,relief='solid',width=1)
            lab=Label(feed,text='Feedback__M_A_/-Music Player',bg='grey50',fg='black',font=('',15),height=1,anchor='w')
            lab.pack(fill='x',side='top')
            lab.bind('<B1-Motion>',move_feedback_win)
            lab.bind('<Button-1>', bouble_click_lab_wid)
            but_close=Button(lab,text='X',font=('',13),command=close,bg='white',fg='red',activebackground='red',
                            activeforeground='black',bd=0,relief='flat')
            but_close.pack(side='right')
            text_box=Text(feed,bg='white',fg='black',font=('',15),bd=10,height=7,relief='sunken',width=60)
            text_box.pack(expand=True,fill='both',side='top')
            but=Button(feed,text='Send feedback',font=('',20),command=thr_sent,bg='skyblue',fg='dark green')
            but.pack(fill='x',side='bottom')
            feed.pack(fill='both',expand=True)
    ##        feed_wind.transient(root)
            feed_wind.grab_set()
            
    ##        root.wait_window(feed_wind)
        finally:
            parent.attributes('-disabled', 0)
            
        


def genSessionId(len_ = 50, idList= []):
    data = "zxcvbnmasdfghjklqwertyuiop1234567890@ZXCVBNMASDFGHJKLQWERTYUIOP&&&&"
    id_ = ""
    for i in range(len_):
        id_ += choice(data)
    
    if id_ in idList:
        genSessionId(len_, idList)
    else:
        return id_



if __name__ == "__main__":
   
    log = LoginPage()
    s  = log.isOnline()
    print(f"st=> {s}")
    # d = log.getData()
    # print(d)
    # log.logout()

