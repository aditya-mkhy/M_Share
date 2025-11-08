import time
from datetime import datetime
import os, sys
import requests

def resource_path(relative_path):
    path=os.path.dirname(sys.executable)    
    return path+'/'+relative_path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def timeCal(sec):
    if sec < 60:
        return f"{sec} Sec"
    elif sec < 3600:
        return f"{sec//60}:{ str(sec%60)[:2]} Mint"
    elif sec < 216000:
        return f"{sec//3600}:{ str(sec%3600)[:2]} Hrs"
    elif sec < 12960000:
        return f"{sec//216000}:{ str(sec%216000)[:2]} Days"
    else:
        return "CE"

   
def data_size_cal(size):
    if size < 1024:
        return f'{size} Bytes'
        
    elif size < 1022976 :
        return f"{size / 1024:.0f} KB"

    elif size < 1048576 :
        return f"{size / 1048576:.2f} MB"

    elif size < 1047527424:
        return f"{size / 1048576:.1f} MB"
        
    elif size < 1073741824:
        return f"{size / 1073741824:.2f} GB"
        
    elif size >= 1073741824:
        return f"{size / 1073741824:.1f} GB"
    else:
        return "Calculation Error"


def log(*args, **kwargs):
    print(f" INFO [{datetime.now().strftime('%d-%m-%Y  %H:%M:%S')}] ", *args, **kwargs)


def getdate(pt=None):
    if pt == None:
        pt = time.time()
    ct  = time.time()
    dayDif = ct-pt
    dayNum =  dayDif//86400

    if dayNum < 1:
        return "Today"

    elif dayNum < 2:
        return "Yesterday" 

    elif dayNum < 7:
        return datetime.fromtimestamp(pt).strftime("%A")# return week days like sunday, monday

    else: 
        return f'{datetime.fromtimestamp(pt).strftime("%d %b %Y")}'


def getTime(t=None):
    if t == None:
        return datetime.now().strftime("%I:%M %p").lower()
    return datetime.fromtimestamp(t).strftime("%I:%M %p").lower()
    
def formatPath(path):
    tPath = ""
    for w in path:
        if w == "\\":
            tPath += "/"
        else:
            tPath += w
    return tPath


if __name__ == "__main__":
    tim = getTime()
    day = getdate()
    print("TIme==> ", tim)
    print("Day==>", day)