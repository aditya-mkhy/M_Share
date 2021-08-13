from tkinter import *
import ctypes , os , sys , socket
from random import choice , randint
from tkinter.filedialog import  askopenfilenames , askdirectory 

from threading import Thread
import time
import tkinter.ttk as ttk

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def ip_address():
        ip = socket.gethostbyname(socket.gethostname())
        return ip
    
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

    

class App():
    def __init__(self):        
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        
        self.root_mshare=Tk()
        self.icon=PhotoImage(file =resource_path("share.png"))
        self.root_mshare.iconphoto(True,self.icon)
        self.root_mshare.title('M_share ..')
        self.root_mshare.geometry('1130x530+200+100')
        self.start_frame=Frame(self.root_mshare,bg='black')
        self.start_frame.pack(fill='both',expand=True)
        self.receive_img= PhotoImage(file = resource_path("rec.png"),master=self.root_mshare)
        self.receive_but=Button(self.start_frame,highlightbackground='black',image=self.receive_img,
                        bd=0,compound='right',activebackground='grey20',cursor='hand2',bg='black',
                        command=self.receive_but_command)
        self.receive_but.pack(side='left',ipadx=100,expand=True)
        self.send_img= PhotoImage(file = resource_path("send2.png"),master=self.root_mshare)
        self.send_but=Button(self.start_frame,highlightbackground='black',image=self.send_img,bd=0,
                        compound='right',activebackground='grey20',cursor='hand2',bg='black',
                         command=self.send_but_command)
        self.send_but.pack(side='right',ipadx=100,expand=True)
        self.ip_value_for_port=StringVar()

        
        self.ip_addres_p=Entry(self.start_frame,textvariable=self.ip_value_for_port,fg='blue2'
                          ,font=('',18),bg='grey80',bd=1,width=10)
        self.ip_value_for_port.set('4092')
        self.ip_addres_p.place(x=10,y=10)
        self.root_mshare.protocol("WM_DELETE_WINDOW", self.on_closing_root)
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("black.Horizontal.TProgressbar", background='royalblue',thickness=4)

        self.root_mshare.mainloop()


    def send_but_command(self):
        print('send_but_command')
        Send(self)

    def receive_but_command(self):
        recieve(self)

    def on_closing_root(self):
        self.root_mshare.destroy()
        sys.exit(1)
    


#_____________________________________________________________________________________________________

class Send():
    def __init__(self,parent_self):
        print('send')
        self.parent_self=parent_self
        parent_self.start_frame.pack_forget()
        
        
        self.frame2=Frame(parent_self.root_mshare,bg='grey50')
        self.frame2.pack(expand=True,fill='both')
        self.frame3=Frame(self.frame2,bg='grey50')
        self.frame3.pack(expand=True,fill='both',side='right')
        self.frame4=Frame(self.frame2,bg='grey90')
        self.frame4.pack(fill='both',side='left',ipadx=200)
        self.frame5=Frame(self.frame3,bg='grey70')
        self.frame5.pack(fill='x',side='top',ipady=100)
        self.ip_label=Label(self.frame4,text='Local IP : %s'%str(ip_address()),fg='white',font=('',20),bg='grey80',bd=5,highlightbackground='orange red')
        self.ip_label.place(x=10,y=40)
        self.conn_label=Label(self.frame4,text='\nlistening requests... ',fg='green',font=('',20),bg='grey90',bd=5,highlightbackground='orange red')
        self.conn_label.place(x=10,y=120)
        self.conndvi_label=Label(self.frame4,text='waiting for connection',fg='blue',font=('',20),bg='grey85',bd=5,highlightbackground='orange red')
        self.conndvi_label.place(x=10,y=210)
        self.disconnect_but=Button(self.frame4,text='disconnect',fg='white',font=('',15,'bold'),bg='RoyalBlue',bd=1,
                              command=self.disconnect_conn)
        
        self.open_file_img= PhotoImage(file = resource_path("folder1.png"))
        self.open_file=Button(self.frame4,image=self.open_file_img,text='Open Files  ',compound='right',
                              fg='black',font=('',15,'bold'),bg='cyan',bd=2,
                              command=self.ask_dir)
        self.open_file.place(x=20,y=340)

    ############################################
        self.files_list = Listbox(self.frame5,bg='white',fg='black',font=('',12),activestyle='none',
                                  bd=5,
                          selectbackground='LightCyan2',
                          selectforeground='red3',selectborderwidth=5,
                          relief='sunken',height=1
                          )
        self.files_list.pack(expand=True,fill=BOTH)
        
        self.send_all_but=Button(self.frame5,text='Select Files (Ctrl+O)',compound='center',fg='white',font=('',15,'bold')
                            ,bg='black',bd=8,relief='raised',highlightthickness=5,
                            highlightbackground='cyan',cursor='hand2',command=self.open_files,
                            activebackground='green yellow')
        self.send_all_but.pack(side='bottom',fill='x')


        self.canvas12 =Canvas(self.frame3,bg='grey50')
        self.canvas12.pack(side='top',anchor="nw",padx=5,expand=True,fill='both',pady=5)
        
 
        self.canvas =Canvas(self.canvas12,bg='grey50')
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = Scrollbar(self.canvas12, orient="vertical",command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame =Frame(self.canvas,bg='grey50')
        

        self.scrollable_frame.bind("<Configure>",lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.parent_self.root_mshare.bind_all("<MouseWheel>",self.scroll_window)


        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        self.back_image=PhotoImage(file = resource_path("back.png"))
        self.back=Button(self.frame4,image=self.back_image,compound='right',font=('',15,'bold')
                            ,bg='black',bd=0,cursor='hand2',highlightbackground='black',
                         command=self.back_button)
        self.back.place(x=0,y=0)

        self.send_items_list=[]
        self.parent_folder=None
        self.network=None
        self.cancel_send=False
        self.sending_process=False
        self.error=None

        #binding_fuction
        self.parent_self.start_frame.bind_all('<Control-o>',self.open_files)
        self.parent_self.start_frame.bind_all('<Control-f>',self.ask_dir )
        self.parent_self.start_frame.bind_all('<Control-d>',self.ask_dir )
        
        #Create_socket_connection
        self.create_socket()
        
    def scroll_window(self,event):
        self.canvas.yview("scroll",-1*int(event.delta/120),"units")
    def ask_dir(self,event=None):
        if self.sending_process != True:
            folder_name=askdirectory(title='Open Folder/Directory')
            if folder_name !='':                
                all_file_list=self.all_file_in_folder(folder_name)
                self.parent_folder=folder_name
                n=1
                for path in all_file_list:
                    self.send_items_list.append(path)
                    self.files_list.insert(END,(str(n)+')  '+(os.path.basename(path))))
                    n+=1
                
    
                    
                #Adding_status
                self.send_all_but.config(text='Send Selected files',state='normal',bg='black',fg='cyan',
                                     command=self.send_all_but_command)

            else:
                print('Cancel')
        else:
            print('Sending in Progess, Please wait for completion')        
        
        
        
    def open_files(self,event=None):
        if self.sending_process != True:
            self.parent_folder=None
            paths=askopenfilenames(title = "Select files ")
            if paths != '':            
                self.send_items_list=[]
                self.files_list.delete(0,END)
                n=1
                for path in paths:
                    self.send_items_list.append(path)
                    self.files_list.insert(END,(str(n)+')  '+(os.path.basename(path))))
                    n+=1
                
                    
                #Adding_status
                self.send_all_but.config(text='Send Selected files',state='normal',bg='black',fg='cyan',
                                         command=self.send_all_but_command)
                

            else:
                print('Cancel')
        else:
            print('Sending in Progess, Please wait for completion')

    def disconnect_conn(self):
        self.connection.close()
        self.conndvi_label.config(text='Waiting for connection')
        self.disconnect_but.place_forget()        
        self.listen_devices()

        
    def back_button(self):
        try:
            self.parent_self.start_frame.unbind_all('<Control-o>')
            self.parent_self.start_frame.unbind_all('<Control-f>')
            self.parent_self.start_frame.unbind_all('<Control-d>' )
        except:
            pass
        try:
            self.frame2.destroy()
        except:
            pass
            
        self.parent_self.start_frame.pack(fill='both',expand=True)
        try:
            self.connection.close()
        except:
            pass
        try:
            self.network.close()
        except:
            pass

        
    def create_socket(self):
        self.network=socket.socket()
        self.network.bind(('',int(self.parent_self.ip_value_for_port.get())))
        self.listen_devices()
        
    def listen_devices(self):            
        th=Thread(target=self.listen_devices_thread,daemon = True)
        th.start()

    def listen_devices_thread(self):
        self.send_all_but.config(state='disabled')
        self.network.listen(1)
        try:
            self.connection , addr=self.network.accept()
            passwd=(self.connection.recv(1024).decode()).split('/')
            if passwd[0]=="--@aditya_M_Share_" :
                m='Ok_'+str(passwd[1])
                self.connection.send(m.encode())
        

                self.conndvi_label.config(text=str(addr[0]+' : '+str(addr[1])))
                self.disconnect_but.place(x=210,y=260)
                self.conn_label.config(fg='green2',text='\nconnected device..')
                self.send_all_but.config(state='normal')
            else:
                self.connection.send(b'Foo')
                self.connection.close()
                self.conndvi_label.config(text='Waiting for connection')
                self.listen_devices()
        except Exception as e:
            print(e)
            pass

  
    def send_file_to_client(self,path):
        
        siz=os.stat(path).st_size
        if siz != 0:            
            if self.parent_folder==None:
                text=f'name={os.path.basename(path)},size={siz}'
            else:
                file='.'+(path.replace(self.parent_folder,''))
                print('file=',file)
                text=f'name={file},size={siz}'
                
            
            try:
                self.connection.send((text.encode()))
                cmd=(self.connection.recv(100)).decode()
                print("cccc",cmd)
                
            except :
                self.error='Disconnected'
                raise UserWarning(self.error)            
            
            if 'send' in cmd:
                progress_label=Frame(self.scrollable_frame,bg='white',width=690,height=90)
                progress_label.pack(side='bottom')
                

                bar= ttk.Progressbar(progress_label, length=650,style='black.Horizontal.TProgressbar',
                                  maximum=(siz), value=0,mode="determinate",orient="horizontal")
                    
                bar['value'] = 0
                bar.place(x=20,y=35)
                media_name=(os.path.basename(path))
                name__=Label(progress_label,text=media_name,bg='white',fg='black',height=0,font=('',11),anchor="w")
                name__.place(x=17,y=2)
                time_left=Label(progress_label,text='2 sec',bg='white',fg='black',height=0,font=('',9),anchor="w")
                time_left.place(x=17,y=45)
                text_="(0 KB of 0 MB , 50.7 KB/s)"
                
                status__=Label(progress_label,text=text_,bg='white',fg='black',height=0,font=('',9),anchor="w")
                status__.place(x=450,y=45)
                
                sep=Frame(progress_label,bg='grey50',width=700,height=3)
                sep.place(x=0,y=87)
                
                file=open(path,'rb')
                
                if "sendappend==" in cmd:
                    try:
                        s=int(cmd.replace('sendappend==',''))
                    except:
                        s="Error"
                    if s != "Error":
                        file.seek(s)
                        print('File_Seeckinf')
                        print('Alredy Exixst== ',s)
                        
                                        
                
                second=time.time()            
                tosz=data_size_cal(siz)
                send_data_in_1sec=0
                data='mkk'
                dat=False
                
                while data:
                    if self.cancel_send == True:
                        status__.config(bg='red')
                        time_left.config(text='Process Cancelled')
                        time_left.config(bg='red')
                        progress_label.config(bg='red')
                        name__.config(bg='red')
                        self.error='Disconnected'
                        file.close()
                        self.connection.close()
                        
                        raise UserWarning(self.error)
                                        
                    c_second=int(str(time.time()-second).split('.')[0])
                    
                    if c_second ==0:
                        pass
                    else:
                        second=time.time()
                        
                        
                        send_size=file.tell()
                        try:
                            st=data_size_cal(send_size)
                            dat=data_size_cal(send_data_in_1sec)                        
                            text_=f"({st} of  {tosz},  {dat}/s)"
                            status__.config(text=text_)
                            bar['value'] = send_size
                        
                            m=(((siz-send_size)//send_data_in_1sec))
                            mint=m//120
                            sec=int(str(m%120)[:2])
                            if sec >=60:
                                mint=mint+(sec//60)
                                sec=sec%60
                            if mint==0:
                                time_left_=str(sec)[:2]+' Sec'
                            else:
                                time_left_=str(mint)+':'+str(sec)[:2]+' Mint'                            
                            
                            time_left.config(text=time_left_)

                        except Exception as e:
                            print('Error: ',e)

                                
                        send_data_in_1sec=0


                    data=file.read(1048576)                
                    try:
                        self.connection.send(data)
                        send_data_in_1sec+=1048576
                    except:
                        self.error='Disconnected'
                        status__.config(bg='red')
                        time_left.config(text='Process is Cancelled by client',bg='red',fg='white')
                        progress_label.config(bg='red')
                        name__.config(bg='red')
                        
                        raise UserWarning(self.error)    

                        break
                    
                print('done____')                        
                try:
                    c=(self.connection.recv(1024)).decode()
                except:
                    file.close()
                    self.error='Disconnected'
                    raise UserWarning(self.error)
                    
                if c=='done':
                    print('Downloading_st_cli_is_done')
                    send_size=file.tell()
                    try:
                        st=data_size_cal(send_size)
                        if dat==False:
                            dat=data_size_cal(send_data_in_1sec)                    
                        text_=f"({st} of  {tosz},  {dat}/s)"
                        status__.config(text=text_,fg='green')
                        bar['value'] = send_size
                    except Exception as e:
                        print('Error : ',e)
                        
                    time_left.config(text='Done ('+time.ctime()+')',fg='cyan3')
                    file.close()

                    
            elif cmd=='--exists':
                progress_label=Frame(self.scrollable_frame,bg='khaki1',width=690,height=90)
                progress_label.pack(side='bottom')
                media_name=(os.path.basename(path))
                name__=Label(progress_label,text=media_name,bg='khaki1',fg='black',height=0,font=('',11),anchor="w")
                name__.place(x=17,y=2)
                
                time_left=Label(progress_label,text='File Already Exists on client PC',bg='khaki1',fg='blue2',
                                height=0,font=('',9),anchor="w")
                time_left.place(x=17,y=45)  
                sep=Frame(progress_label,bg='cyan2',width=700,height=3)
                sep.place(x=0,y=87)
                
            else:
                self.error='Unknown_command'

        
    def send_all_but_command(self):
        thr=Thread(target=self.send_multiple_files,daemon = True)
        thr.start()
    def cancel_send_process(self):
        self.cancel_send=True
        
    def send_multiple_files(self):
        self.cancel_send=False
        self.error=None
        self.sending_process = True
        self.send_all_but.config(command=self.cancel_send_process,text='Cancel Sending Process',bg='red'
                                 ,fg='white')
        file_send_done_list=self.send_items_list.copy()
        try:
            for path in self.send_items_list:
                if self.cancel_send == True:
                    break
                else:
                    self.send_file_to_client(path)
                    if self.cancel_send !=True:
                        self.files_list.delete(0,0)
                        file_send_done_list.remove(path)
        except Exception as e:
            print('Error : ',e)
            
        finally:
            self.sending_process = False

            if self.error=='Disconnected' or self.error=='cancelled':                
                self.send_items_list=file_send_done_list.copy()                
                if self.cancel_send==True:
                    t='Try Again ( Cancelled )'
                    
                elif self.error=='Disconnected':
                    t='Try Again ( Disconnected )'
                    
                else:
                    t='Try Again (Error occured)'
                                    
                self.send_all_but.config(command=self.send_all_but_command,text=t,
                                bg='cornflower blue',fg='red')
                
                if self.error=='Disconnected':
                    self.connection.close()
                    self.conndvi_label.config(text='Waiting for connection')
                    self.conn_label.config(fg='red',text='Connection is Closed \nby Client')            
                    self.disconnect_but.place_forget()
                    self.listen_devices()
                    
                                                
            elif file_send_done_list==[]:
                self.send_items_list=[]
                self.parent_folder==None
                self.send_all_but.config(command=self.open_files,text='Select Files (Ctrl+O)',
                                     bg='black',fg='white')                               
            else:
                print('Error : 34: ')

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

#___________________________________________________________________________________________________

class recieve():
    def __init__(self,parent_self):
        print('recive')
        self.parent_self=parent_self
        self.parent_self.start_frame.pack_forget()
        
        self.frame2=Frame(parent_self.root_mshare,bg='grey50')
        self.frame2.pack(expand=True,fill='both')
        self.frame3=Frame(self.frame2,bg='grey50')
        self.frame3.pack(expand=True,fill='both',side='right')
        self.frame4=Frame(self.frame2,bg='grey90')
        self.frame4.pack(fill='both',side='left',ipadx=200)
        self.ip_label=Label(self.frame4,text='Enter IP Adddress',fg='white',font=('',20),bg='grey75',bd=0)
        self.ip_label.place(x=10,y=40)
        
        self.ip_value=StringVar()
        self.ip_ent=Entry(self.frame4,textvariable=self.ip_value,fg='blue2',font=('',20),bg='grey80',bd=1)
        self.ip_value.set((str(ip_address())))
        self.ip_ent.place(x=10,y=100)
        
        self.rec_connect_but=Button(self.frame4,text='connect',fg='black',font=('',15,'bold'),width=22,
                                    bg='cyan',bd=1,command=self.rec_connect_to_dev)
        self.rec_connect_but.place(x=20,y=160)
        self.conn_label=Label(self.frame4,text='',fg='red',font=('',20),bg='grey90',bd=5,highlightbackground='orange red')
        self.conn_label.place(x=10,y=300)

        self.Path_lab=Label(self.frame4,text='Current Path',fg='black',font=('',15),bg='white',bd=0)
        self.Path_lab.place(x=10,y=420)

        self.Path_lab=Button(self.frame4,fg='black',font=('',10),bg='white',bd=0,
                             command=self.chdir,justify='left')
        self.Path_lab.place(x=10,y=460)
        self.chdir(event=True)

        

        
        self.canvas12 =Canvas(self.frame3,bg='grey50')
        self.canvas12.pack(side='top',anchor="nw",padx=5,expand=True,fill='both',pady=5)
        
 
        self.canvas =Canvas(self.canvas12,bg='grey50')
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = Scrollbar(self.canvas12, orient="vertical",command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame =Frame(self.canvas,bg='grey50')
        

        self.scrollable_frame.bind("<Configure>",lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        
        self.parent_self.root_mshare.bind_all("<MouseWheel>", self.scroll_window)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        
        self.back_image=PhotoImage(file = resource_path("back.png"))    
        self.back=Button(self.frame4,image=self.back_image,compound='right',font=('',15,'bold'),
                         bg='black',bd=0,cursor='hand2',highlightbackground='black',
                         command=self.back_button)
        self.back.place(x=0,y=0)

        self.conn=None
        self.cancel=False
        
    def chdir(self,event=None):
        if event!=True:
            folder_name=askdirectory(title='Open Folder/Directory')
            if folder_name != '':
                os.chdir(folder_name)

        path=os.getcwd()
        p=''
        n=0
        for i in path:
            p+=i
            n+=1
            if n >= 30:
                if i == '/' or i=='\\':
                    n=0
                    p+='\n    \\ '
            
        
        self.Path_lab.config(text=p)
        

    def scroll_window(self,event):
        self.canvas.yview("scroll",-1*int(event.delta/120),"units")


    def rec_connect_to_dev(self):
        ip=self.ip_value.get()
        self.conn=socket.socket()
        try:
            self.conn_label.config(text='Connecting....')
            self.conn.connect((ip,int(self.parent_self.ip_value_for_port.get())))
            self.conn_label.config(text='Pairing....')
            passwd=randint(100000,999999)
            b='--@aditya_M_Share_/'+str(passwd)
            self.conn.send(b.encode())
            conf=(self.conn.recv(1024)).decode()
            if conf == conf:
                
                self.rec_connect_but.config(text='..Connected.. ',bg='green yellow',
                                            command=self.rec_disconnect_to_dev)
                self.conn_label.config(text='')
                thr=Thread(target=self.receive_data,daemon = True)
                thr.start()
            else:
                self.rec_connect_but.config(text='Invalid Passwd',bg='red',
                                            command=self.rec_connect_to_dev)
                self.conn_label.config(text='')
            
        except Exception as e:
            if 'refused' in str(e):
                self.conn_label.config(text='device refused connection ')
            else:
                self.conn_label.config(text=(str(e)))
                
    def rec_disconnect_to_dev(self):
        self.conn.close()
        self.rec_connect_but.config(text='disConnected')
        self.rec_connect_but.config(bg='red')
        self.rec_connect_but.config(command=self.rec_connect_to_dev)
        self.conn_label.config(text='Connection is closed ')
        self.conn_label.config(fg='red')
                
    def back_button(self):
        try:
            self.frame2.destroy()
        except:
            pass
            
        self.parent_self.start_frame.pack(fill='both',expand=True)
        try:
            self.conn.close()
        except:
            pass
        print('back_button')
    def check_if_exist(self,file,size):
        if os.path.exists(file):
            siz=os.stat(file).st_size
            if siz == size:
                return "exists"
            elif siz <  size:
                print('append_size_check')
                return "append"
            else:
                return False
        else:
            return False

    def receive_data(self):
        self.conn_label.config(text='Recieving Data....')
        self.conn_label.config(fg='maroon')
        self.cancel=False
        dat=None
        while True:
            data=((self.conn.recv(1024)).decode())
            if not data:
                self.rec_connect_but.config(bg='orange',text='disConnected',
                                            command=self.rec_connect_to_dev)
                self.conn_label.config(text='Connection is closed by \nthe remote server',fg='red')
                break

            if 'name=' in data:                
                name ,total_file_size=data.split(',')
                name=(name.split('='))[1]
                total_file_size=int((total_file_size.split('='))[1])
                print(name,total_file_size)

                check=self.check_if_exist(name,total_file_size)
                if check=="exists":
                    print('--exists')
                    self.conn.send(b'--exists')
                    
                else:
                    if name[0]=='.':
                        print('creating_direcrory')
                        d=''
                        for i in name:
                            d+=i
                            if i=='/' or i=='\\':
                                if os.path.exists(d):
                                    pass
                                else:
                                    try:
                                        os.mkdir(d)
                                    except Exception as e:
                                        print('Error : mkdir ==',d)
                                
                            
                    
                    #Sending_request_to_send_data
                    if check =="append":
                        file_wr=open(name,'ab')
                        file_size=file_wr.tell()
                        self.conn.send(('sendappend=='+str(file_size)).encode())
                        print('APeend=file_size==',file_size)
                        
                    else:
                        self.conn.send(b'send')
                        file_wr=open(name,'wb')
                        file_size=0

                    progress_label=Frame(self.scrollable_frame,bg='white',width=690,height=90)
                    progress_label.pack(side='bottom')
                    

                    bar= ttk.Progressbar(progress_label, length=650,style='black.Horizontal.TProgressbar',
                                      maximum=(total_file_size), value=0,mode="determinate",orient="horizontal")
                        
                    bar['value'] = 0
                    bar.place(x=20,y=35)
                    name__=Label(progress_label,text=(os.path.basename(name)),bg='white',fg='black',height=0,font=('',11),anchor="w")
                    name__.place(x=17,y=2)
                    time_left=Label(progress_label,text='2 sec',bg='white',fg='black',height=0,font=('',9),anchor="w")
                    time_left.place(x=17,y=45)
                    text_="(0 KB of 0 MB , 50.7 KB/s)"
                    
                    status__=Label(progress_label,text=text_,bg='white',fg='black',height=0,font=('',9),anchor="w")
                    status__.place(x=450,y=45)
                    
                    sep=Frame(progress_label,bg='grey50',width=700,height=3)
                    sep.place(x=0,y=87)                

                    

                    second=time.time()
                    data='aditya'
                    send_data_in_1sec=0
                    file_size_in_si=data_size_cal(total_file_size)
                    while data:
                        if self.cancel == True:
                            status__.config(bg='red')
                            time_left.config(text='you Cancelled',bg='red',fg='white')
                            progress_label.config(bg='red')
                            name__.config(bg='red')
                            break
                        
                        c_second=int(str(time.time()-second).split('.')[0])
                        recv_size=file_wr.tell()
                        
                        if c_second ==0:
                            pass
                        else:
                            second=time.time()
                            try:
                                
                                st=data_size_cal(recv_size)
                                dat=data_size_cal(send_data_in_1sec)                        
                                text_=f"({st} of  {file_size_in_si},  {dat}/s)"
                                m=(((total_file_size-recv_size)//send_data_in_1sec))
                                mint=m//120
                                sec=int(str(m%120)[:2])
                                if sec >=60:
                                    mint=mint+(sec//60)
                                    sec=sec%60
                                if mint==0:
                                    time_left_=str(sec)[:2]+' Sec'
                                else:
                                    time_left_=str(mint)+':'+str(sec)[:2]+' Mint'
                                status__.config(text=text_)
                                bar['value'] = recv_size
                                time_left.config(text=time_left_)
                            except:
                                pass                        

                            send_data_in_1sec=0
                                
                        if recv_size == total_file_size:
                            if dat == None:
                                try:
                                    dat=data_size_cal(send_data_in_1sec)
                                except:
                                    pass
                            recv_size=file_wr.tell()
                            try:
                                st=data_size_cal(recv_size)
                                text_=f"({st} of  {file_size_in_si},  {dat}/s)"
                                status__.config(text=text_)
                            except:
                                passs
                            bar['value'] = recv_size
                            time_left.config(text='Done ('+time.ctime()+')',fg='cyan3')
                            break
                                
                        
                        data=self.conn.recv(1048576)
                        if not data:
                            time_left.config(text='Server Disconnected',bg='red',fg='white')
                            progress_label.config(bg='red')
                            name__.config(bg='red')
                            status__.config(bg='red')
                            break

                        #Writing_data_in_file
                        send_data_in_1sec+=file_wr.write(data)
                        
                    print('done')
                    file_wr.close()
                    
                    try:
                        self.conn.send(('done').encode())
                    except:
                        self.rec_connect_but.config(bg='orange',text='disConnected',
                                                    command=self.rec_connect_to_dev)
                        self.conn_label.config(text='Connection is closed by \nthe remote server',fg='red')
                        break

            else:
                print('Recieved_Data=={',data,'}')
            
        print('Exit___recv')



if __name__ == "__main__":
    Application=App()
    
