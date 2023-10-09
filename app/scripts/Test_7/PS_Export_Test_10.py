import logging
import sqlite3
import ctypes  # for call MessageBoxw
import sys #handle parameters
import os
import csv
import tkinter as tk # if using Python 3
from tkinter import filedialog
import uuid
import tkinter, tkinter.messagebox

MY_MACHINEID="22727983491042"

DatabasePath='C:/AIVER/Dolby.db'
LogsPath='C:/AIVER/Logs/'
testname=os.path.basename(__file__).replace(".py","").replace(".exe","")  #replace .exe and .py
logpath=LogsPath + os.path.basename(__file__).replace(".py",".log").replace(".exe","").replace('PS_','') #replace .exe and .py
ResultDirectory='C:/AIVER/Results/' + testname.replace('PS_','') + '/'
os.makedirs(os.path.dirname(ResultDirectory), exist_ok=True) #Create Result Test Directory
os.makedirs(os.path.dirname(logpath), exist_ok=True) #Create Result Logs Directory




LogsPathUpdate='C:/AIVER/Logs/Update/'
HtdocsLogsPathUpdate='C:/AIVER/Dash/AIVER/Logs/Update/'
logpathUpdate=LogsPathUpdate + os.path.basename(__file__).replace(".py",".log").replace(".exe","").replace('PS_','') #replace .exe and .py
htdocslogpathUpdate=HtdocsLogsPathUpdate + os.path.basename(__file__).replace(".py",".log").replace(".exe","").replace('PS_','') #replace .exe and .py
ResultDirectoryUpdate='C:/AIVER/Results/Update/' + testname.replace('PS_','') + '/'
os.makedirs(os.path.dirname(ResultDirectoryUpdate), exist_ok=True) #Create Result Test Directory
os.makedirs(os.path.dirname(logpathUpdate), exist_ok=True) #Create Result Logs Directory
os.makedirs(os.path.dirname(htdocslogpathUpdate), exist_ok=True) #Create Result Logs Directory




formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(message)s',datefmt='%Y/%m/%d %I:%M:%S')
handler = logging.FileHandler(filename=logpath)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info("AIVER Export Test_10 Script Started")

def msgbox_info(title, text):
    root = tkinter.Tk()
    root.attributes('-topmost', 1)              # Raising root above all other windows
    root.withdraw()
    tkinter.messagebox.showinfo(title, text)
    root.destroy()

def msgbox_error(title, text):
    root = tkinter.Tk()
    root.attributes('-topmost', 1)              # Raising root above all other windows
    root.withdraw()
    tkinter.messagebox.showerror(title, text)
    root.destroy()
    
def is_valid_machineid(machineid):
    print(machineid)
    print(uuid.getnode())
    if machineid==str(uuid.getnode()):
        return 1
    else:
        msgbox_error("Error","Invalid MachineID")
        logger.error("Invalid MachineID")
        logger.info("Script Finished")
        logger.handlers = []
        logging.shutdown()
        sys.exit(-1)
        
#Validate MachineID
#is_valid_machineid(MY_MACHINEID)

#Put here the view name you wish to export
if len(sys.argv) == 1:
    views=["OR_10_1","OR_10_2","OR_10_3","OR_10_4_1","OR_10_4_2","OR_10_4_3"]
else:
    views=["OR_10_1_Update","OR_10_2_Update","OR_10_3_Update","OR_10_4_1_Update","OR_10_4_2_Update","OR_10_4_3_Update"]


'''
ResultDirectory = filedialog.askdirectory()
if not os.path.exists(ResultDirectory):
    logger.error("Path Not Selected")
    logger.info("Script Finished")
    logger.handlers = []
    logging.shutdown()
    sys.exit(-1)
'''


if len(sys.argv) == 1:
    ResultDirectory="C:\\AIVER\\Results"
else:
    ResultDirectory=ResultDirectoryUpdate


try:
    conn = sqlite3.connect(DatabasePath)
    cur = conn.cursor()
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    logger.info("AIVER Export Test_10 Script Finished")
    sys.exit(-1)


for view in views:
    print(view)
    logger.info("Export " + view)
    try:
        cur.execute('SELECT * FROM ' + view)
        with open(ResultDirectory+'/'+ view + '.csv','w',encoding='utf-8',newline='') as out_csv_file:
             csv_out = csv.writer(out_csv_file)
             # write header
             csv_out.writerow([d[0] for d in cur.description])
             # write data
             for result in cur:
                 csv_out.writerow(result)

    except Exception as err:
        logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))


conn.commit()
conn.close()
logger.info("AIVER Export Test_10 Script Finished")
logger.handlers = []
logging.shutdown()