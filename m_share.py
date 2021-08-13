from tkinter import * import ctypes , os , sys , socket ,netifaces
from random import choice
from tkinter.filedialog import  askopenfilenames
from threading import Thread
import time
import tkinter.ttk as ttk
def m_share(event=None):
    def _click_on_file_send(event=None):
        global send_items_list ,files_list ,cancel
        cancel=True
        index=(files_list.curselection())[0]
        path=send_items_list[index]
        print(path)
        _send_file_to(path)
    def send_all_but_command(event=None):
        global cancel
        cancel=True
        thr=Thread(target=send_multiple_files)
        thr.start()
        
    def send_multiple_files(event=None):
        global send_items_list ,files_list ,cancel
        cancel=True
        n=0
        for path in send_items_list:
            if cancel == False:
                break
            _send_file_to(path)
            files_list.delete(n,n)
            
        
    def _send_file_to(path):
        global connection ,frame3,disconnect_but ,conndvi_label,conn_label
        siz=os.stat(path).st_size
        text=f'name={os.path.basename(path)},size={siz}'
        try:
            connection.send((text.encode()))
            c=(connection.recv(100)).decode()
        except:
            c='notconnected'
            connection.close()
            conndvi_label.config(text='Waiting for connection')
            conn_label.config(fg='red',text='Connection is Closed \nby host')
            
            disconnect_but.place_forget()
            listen_devices()
            
        
        if c=='send':
            global down_status
            progress_label=Label(down_status,bg='white',width=75,height=4)
            progress_label.pack(side='bottom')
            style = ttk.Style()
            style.theme_use('default')
            style.configure("black.Horizontal.TProgressbar", background='royalblue',thickness=6)
            bar = ttk.Progressbar(progress_label, length=500,style='black.Horizontal.TProgressbar',
                              maximum=(siz//1048576), value=0,mode="determinate",orient="horizontal")
                
            bar['value'] = 0
            bar.place(x=20,y=35)
            media_name=(os.path.basename(path))
            name__=Label(progress_label,text=media_name,bg='white',fg='black',height=0,font=('',11),anchor="w")
            name__.place(x=17,y=2)
            time_left=Label(progress_label,text='2 sec',bg='white',fg='black',height=0,font=('',9),anchor="w")
            time_left.place(x=17,y=45)
            text_="(0 KB of 0 MB , 50.7 KB/s)"
            
            status__=Label(progress_label,text=text_,bg='white',fg='black',height=0,font=('',9),anchor="w")
            status__.place(x=350,y=45)
            
            file=open(path,'rb')
            data=file.read(1048576)
            connection.send(data)
            tosz=(siz//1048576)
            send_size=file.tell()
            second=0
            data_size_t=send_size
            while data:
                
                global cancel
                if cancel == False:
                    send_all_but.config(text='Send all files')
                    send_all_but.config(command=send_all_but_command)
                    print('Cancel is falling')
                    
                    break
                
                c_second=(((((time.ctime()).split())[3]).split(':'))[2])            
                if c_second ==second:
                    pass
                else:
                    second=c_second
                    send_size=file.tell()
                    st=(send_size//1048576)                

                    dat=data_size_t//1048576                
                    datk=str(data_size_t%1048576)
                    if dat == 0:
                        dat=datk[:3]+' KB/s'
                    else:
                        dat=str(dat)+'.'+datk[:2]+' MB/s'
                        
                    text_=f"({st} MB of  {tosz}MB ,  {dat})"

                    m=(((siz-send_size)//data_size_t))
                    mint=m//120
                    sec=int(str(m%120)[:2])
                    if sec >=60:
                        mint=mint+(sec//60)
                        sec=sec%60
                    if mint==0:
                        time_left_=str(sec)[:2]+' Sec'
                    else:
                        time_left_=str(mint)+':'+str(sec)[:2]+' Mint'

                            
                    data_size_t=0
                    status__.config(text=text_)
                    bar['value'] = st
                    time_left.config(text=time_left_)
                    down_status.place_forget()
                    down_status.place(x=10,y=290)
                    
                data=file.read(104857)
                try:
                    connection.send(data)
                except:
                    
                    connection.close()
                    conndvi_label.config(text='Waiting for connection')
                    conn_label.config(fg='red',text='Connection is Closed \nby host')
                    
                    disconnect_but.place_forget()
                    listen_devices()
                    status__.config(bg='red')
                    time_left.config(text='Process is Cancelled by Host')
                    time_left.config(bg='red')
                    progress_label.config(bg='red')
                    name__.config(bg='red')
                    down_status.place_forget()
                    down_status.place(x=10,y=290)
                    print('llllllllllllllllllllllll')
                    break
                data_size_t=data_size_t+104857
                
            print('done')
            
            try:
                c=(connection.recv(1024)).decode()
            except:
                c='con_closed'
            if c=='done':
                print('done')
                send_size=file.tell()
                st=(send_size//1048576)            
                text_=f"({st} MB of  {tosz}MB ,  {dat})"
                status__.config(text=text_)
                bar['value'] = st
                time_left.config(text='0 Sec')
                down_status.place_forget()
                down_status.place(x=10,y=290)
                print('done----')
            else:
                print('Error')
            file.close()
        else:
            print('Error--')
                    
    def disconnect_conn(event=None):
        global connection ,disconnect_but ,conndvi_label
        connection.close()
        conndvi_label.config(text='Waiting for connection')
        disconnect_but.place_forget()
        listen_devices()
        
    def ip_address():
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        i_p=netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        return i_p
    def open_files(event=None):
        paths=askopenfilenames(title = "Select files ")
        print(paths)
        if paths != '':
            
            global files_list ,send_items_list
            send_items_list=[]
            files_list.delete(0,END)
            n=1
            for path in paths:
                
                send_items_list.append(path)
                files_list.insert(END,(str(n)+')  '+(os.path.basename(path))))
                n+=1
            else:
                print('Cancel')
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    def create_socket(disconnect_but,conndvi_label):
        global  net
        net=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        net.bind(('',4092))
        listen_devices()
    def listen_devices():
        def listen_devices1():
            global connection ,  net
            net.listen(1)
            connection , addr=net.accept()
            conndvi_label.config(text=str(addr[0]+' : '+str(addr[1])))
            disconnect_but.place(x=210,y=260)
            conn_label.config(fg='green2',text='\nconnected device..')
        th=Thread(target=listen_devices1)
        th.start()
        
        
        
    def send_but_command(event=None):
        global open_file_img ,files_list,send_all_but ,disconnect_but ,conndvi_label ,frame4,frame3,down_status
        global frame2,conn_label
        print('send')
        start_frame.pack_forget()
        frame2=Frame(root_mshare,bg='grey50')
        frame2.pack(expand=True,fill='both')
        frame3=Frame(frame2,bg='grey80')
        frame3.pack(expand=True,fill='both',side='right')
        frame4=Frame(frame2,bg='grey90')
        frame4.pack(fill='both',side='left',ipadx=200)
        frame5=Frame(frame3,bg='grey70')
        frame5.pack(fill='x',side='top',ipady=100)
        ip_label=Label(frame4,text='Local IP : %s'%str(ip_address()),fg='white',font=('',20),bg='grey80',bd=5,highlightbackground='orange red')
        ip_label.place(x=10,y=40)
        conn_label=Label(frame4,text='\nlistening requests... ',fg='green',font=('',20),bg='grey90',bd=5,highlightbackground='orange red')
        conn_label.place(x=10,y=120)
        conndvi_label=Label(frame4,text='waiting for connection',fg='blue',font=('',20),bg='grey85',bd=5,highlightbackground='orange red')
        conndvi_label.place(x=10,y=210)
        disconnect_but=Button(frame4,text='disconnect',fg='white',font=('',15,'bold'),bg='RoyalBlue',bd=1,
                              command=disconnect_conn)
        
        open_file_img= PhotoImage(file = resource_path("folder1.png"),master=root_mshare)
        open_file=Button(frame4,image=open_file_img,text='Open Files  ',compound='right',fg='black',font=('',15,'bold'),bg='cyan',bd=2,
                              command=open_files)
        open_file.place(x=20,y=340)

    ############################################
        files_list = Listbox(frame5,bg='black',fg='white',font=('',15),activestyle='none',bd=0,
                          disabledforeground='red',highlightbackground='white',highlightcolor='blue',
                          highlightthickness=3,selectbackground='LightCyan2',
                          selectforeground='red3',selectborderwidth=0,
                          relief='ridge',height=1
                          )
        files_list.pack(expand=True,fill=BOTH)
        files_list.bind('<Double-1>',_click_on_file_send)
    ##    files_list.bind('<<ListboxSelect>>',show_youtube_video_)

        send_all_but=Button(frame5,text='Send all files',compound='right',fg='black',font=('',15,'bold')
                            ,bg='grey95',bd=2,relief='sunken',highlightthickness=2,
                            highlightbackground='cyan',cursor='hand2',command=send_all_but_command,
                            activebackground='green yellow')
        send_all_but.pack(side='bottom',fill='x')
        down_status=Label(frame3,bg='grey80')
        down_status.place(x=10,y=290)
        global back_image
        back_image=PhotoImage(file = resource_path("back.png"))
        back=Button(frame4,image=back_image,compound='right',font=('',15,'bold')
                            ,bg='black',bd=0,cursor='hand2',highlightbackground='black',command=back_button)
        back.place(x=0,y=0)


        

        create_socket(disconnect_but,conndvi_label)
        
    def cancel_pro(event=None):
        global cancel
        cancel=False
    def rec_disconnect_to_dev(event=None):
        global conn
        conn.close()
        rec_connect_but.config(text='disConnected')
        rec_connect_but.config(bg='red')
        rec_connect_but.config(command=rec_connect_to_dev)
        conn_label.config(text='Connection is closed ')
        conn_label.config(fg='red')
        
    def receive_data(conn):
        conn_label.config(text='Recieving Data....')
        conn_label.config(fg='maroon')
        while True:
            data=((conn.recv(1024)).decode())
            if not data:
                rec_connect_but.config(text='disConnected')
                rec_connect_but.config(bg='orange')
                rec_connect_but.config(command=rec_connect_to_dev)
                conn_label.config(text='Connection is closed by \nthe remote server')
                conn_label.config(fg='red')
                break

            if 'name=' in data:
                global cancel
                cancel=True
                
                name ,size=data.split(',')
                name=(name.split('='))[1]
                size=int((size.split('='))[1])
                print(name,size)
                conn.send(('send').encode())
                global down_status
                progress_label=Label(down_status,bg='white',width=75,height=4)
                progress_label.pack(side='bottom')
                style = ttk.Style()
                style.theme_use('default')
                style.configure("black.Horizontal.TProgressbar", background='royalblue',thickness=6)
                bar = ttk.Progressbar(progress_label, length=500,style='black.Horizontal.TProgressbar',
                                  maximum=(size//1048576), value=0,mode="determinate",orient="horizontal")
                    
                bar['value'] = 0
                bar.place(x=20,y=35)
                name__=Label(progress_label,text=name,bg='white',fg='black',height=0,font=('',11),anchor="w")
                name__.place(x=17,y=2)
                time_left=Label(progress_label,text='0 sec',bg='white',fg='black',height=0,font=('',9),anchor="w")
                time_left.place(x=17,y=45)
                text_="(0 KB of 0 MB , 50.7 KB/s)"
                
                status__=Label(progress_label,text=text_,bg='white',fg='black',height=0,font=('',9),anchor="w")
                status__.place(x=320,y=45)
            

                
                f=open(name,'ab')
                f.truncate(0)
                file_size=0
                tsize=(size//1048576)
                data=conn.recv(1048576)
                data_size=len(data)
                file_size=file_size+data_size
                f.write(data)
                second=0
                data_size_t=data_size
                while data:
                    if cancel == False:
                        break
                    c_second=(((((time.ctime()).split())[3]).split(':'))[2])
                    
                    if c_second ==second:
                        pass
                    else:
                        second=c_second
                        st=(file_size//1048576)
                        m=(((size-file_size)//data_size_t))
                        mint=m//120
                        sec=int(str(m%120)[:2])
                        if sec >=60:
                            mint=mint+(sec//60)
                            sec=sec%60
                        if mint==0:
                            time_left_=str(sec)[:2]+' Sec'
                        else:
                            time_left_=str(mint)+':'+str(sec)[:2]+' Mint'
                            
                        dat=data_size_t//1048576
                        
                        datk=str(data_size_t%1048576)
                        if dat == 0:
                            dat=datk[:3]+' KB/s'
                        else:
                            dat=str(dat)+'.'+datk[:2]+' MB/s'
                        
                        text_=f"({st} MB of  {tsize}MB ,   {dat})"
                        bar['value'] = st
                        time_left.config(text=time_left_)                    
                        status__.config(text=text_)
                        

                        print(c_second)
                        data_size_t=0
                        down_status.place_forget()
                        down_status.place(x=10,y=0)
                                       
                        
                        
                    
                    
                    data=conn.recv(1048576)
                    if not data:
                        time_left.config(text='Process is Cancelled by server')
                        time_left.config(bg='red')
                        progress_label.config(bg='red')
                        name__.config(bg='red')
                        status__.config(bg='red')
                        down_status.place_forget()
                        down_status.place(x=10,y=0)
                        break
                    f.write(data)
                    data_size=len(data)
                    data_size_t=data_size_t+data_size
                    file_size=file_size+data_size
                    if file_size== size:
                        st=(file_size//1048576)
                        m=(((size-file_size)//data_size_t))
                        mint=m//120
                        sec=str(m%120)[:2]
                        
                        text_=f"({st} MB of  {tsize}MB ,   {dat})"
                        bar['value'] = st
                        time_left.config(text='0 sec')                    
                        status__.config(text=text_)
                        down_status.place_forget()
                        down_status.place(x=10,y=0)
                        
                        break
                    else:
                        pass
                print('done')
                f.close()
                try:
                    conn.send(('done').encode())
                except:
                    pass
            else:
                print(data)
                        

    def rec_connect_to_dev(event=None):
        global ip_value ,rec_connect_but ,conn ,conn_label
        ip=ip_value.get()
        conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.connect((ip,4092))
            rec_connect_but.config(text='..Connected.. ')
            rec_connect_but.config(bg='green yellow')
            rec_connect_but.config(command=rec_disconnect_to_dev)
            conn_label.config(text='')
            thr=Thread(target=receive_data,args=(conn,))
            thr.start()
            
        except Exception as e:
            if 'refused' in str(e):
                conn_label.config(text='device refused connection ')
            else:
                conn_label.config(text=((str(e).split(']'))[1]))
            
        
        
        
    def receive_but_command(event=None):
        global ip_value ,rec_connect_but,conn_label ,down_status,frame2
        print('recive')
        start_frame.pack_forget()
        frame2=Frame(root_mshare,bg='grey50')
        frame2.pack(expand=True,fill='both')
        frame3=Frame(frame2,bg='grey80')
        frame3.pack(expand=True,fill='both',side='right')
        frame4=Frame(frame2,bg='grey90')
        frame4.pack(fill='both',side='left',ipadx=200)
        ip_label=Label(frame4,text='Enter IP Adddress',fg='white',font=('',20),bg='grey75',bd=0)
        ip_label.place(x=10,y=40)
        ip_value=StringVar()
        ip_ent=Entry(frame4,textvariable=ip_value,fg='blue2',font=('',20),bg='grey80',bd=1)
        ip_value.set((str(ip_address()))[:11])
        ip_ent.place(x=10,y=100)
        
        rec_connect_but=Button(frame4,text='connect',fg='black',font=('',15,'bold'),width=22,bg='cyan',bd=1,
                              command=rec_connect_to_dev)
        rec_connect_but.place(x=20,y=160)
        conn_label=Label(frame4,text='',fg='red',font=('',20),bg='grey90',bd=5,highlightbackground='orange red')
        conn_label.place(x=10,y=370)

        down_status=Label(frame3,bg='grey80')
        down_status.place(x=10,y=0)
        global back_image
        back_image=PhotoImage(file = resource_path("back.png"))    
        back=Button(frame4,image=back_image,compound='right',font=('',15,'bold')
                            ,bg='black',bd=0,cursor='hand2',highlightbackground='black',command=back_button)
        back.place(x=0,y=0)

    def back_button(event=None):
        global frame2
        try:
            frame2.destroy()
        except:
            pass
            
        start_frame.pack(fill='both',expand=True)
        global  net,connection ,conn
        try:
            connection.close()
        except:
            pass
        try:
            net.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass
            
    def on_closing_root(event=None):
        global  net,connection ,conn
        try:
            connection.close()
        except:
            pass
        try:
            net.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass
        root_mshare.destroy()
        sys.exit(1)
        


        
    send_items_list=[]    
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root_mshare=Tk()
    icon=PhotoImage(file =resource_path("share.png"))
    root_mshare.iconphoto(True,icon)
    root_mshare.title('M_share ..')
    root_mshare.geometry('1000x500+200+100')
    start_frame=Frame(root_mshare,bg='black')
    start_frame.pack(fill='both',expand=True)
    receive_img= PhotoImage(file = resource_path("rec.png"),master=root_mshare)
    receive_but=Button(start_frame,highlightbackground='black',image=receive_img,bd=0,compound='right',activebackground='grey20',cursor='hand2',bg='black',
                     command=receive_but_command)
    receive_but.pack(side='left',ipadx=100,expand=True)
    send_img= PhotoImage(file = resource_path("send2.png"),master=root_mshare)
    send_but=Button(start_frame,highlightbackground='black',image=send_img,bd=0,compound='right'
                    ,activebackground='grey20',cursor='hand2',bg='black',
                     command=send_but_command)
    send_but.pack(side='right',ipadx=100,expand=True)
    root_mshare.protocol("WM_DELETE_WINDOW", on_closing_root)
    root_mshare.mainloop()
m_share()
