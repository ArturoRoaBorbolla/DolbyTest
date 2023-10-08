# -*- coding: utf-8 -*-

import logging
import sqlite3
import sys #handle parameters
import os
import csv
import uuid
import tkinter, tkinter.messagebox
from fuzzywuzzy import process
import subprocess

from CTkMessagebox import CTkMessagebox
import datetime
import calendar
from calendar import monthrange
import customtkinter
import datetime
import calendar
from calendar import monthrange
from xlsxwriter.workbook import Workbook
import plotly.graph_objects as go
import pandas as pd
import sys
import shutil
import os




PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, f'{PRO_DIR}\\common')
sys.path.insert(2, f'{PRO_DIR}\\Scripts_UI')

import get_data
import create_link
import DolbyUI
import var
import visualize




customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

data=var.data["Test_09"]
#print(data)

global Start_year
global End_year
global DateTo
global DateFrom


connection = sqlite3.connect(var.DatabasePath)
cursor = connection.cursor()

today = datetime.date.today()
Start_year = today.strftime("%Y")
End_year = today.strftime("%Y")
values = ["Q1", "Q2", "Q3", "Q4"]
DateFrom = "Q1"
DateTo = "Q4"


ROOT_DIR = PRO_DIR
TEST_DIR = f"{ROOT_DIR}\\Test_9"
DatabasePath = f'{ROOT_DIR}\\..\\DataBase\\Dolby.db'
#Source_Dir = f"{TEST_DIR}\\Source_Dir"

LogsPath = f"{TEST_DIR}\\Logs"    
Output_dir= f"{TEST_DIR}\\Output"
csv_folder = f'{Output_dir}\\csv'
html_dir= f'{Output_dir}\\html'


os.makedirs(LogsPath, exist_ok=True)
os.makedirs(Output_dir, exist_ok=True)
os.makedirs(csv_folder, exist_ok=True)
#os.makedirs(Source_Dir, exist_ok=True)
os.makedirs(html_dir, exist_ok=True)



testname=os.path.basename(__file__).replace(".py","").replace(".exe","")  #replace .exe and .py
formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(message)s',datefmt='%Y/%m/%d %I:%M:%S')
logpath= f"{LogsPath}\\{testname}.log"  
handler = logging.FileHandler(filename=logpath)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info("Script Started")




def create_dashboard():
    Output=f'{ROOT_DIR}'
    Dasboard=f'{Output}\\Dashboard'
    Reports = f'{Output}\\Report'
    csv_folder = f'{Output}\\csv'
    Visualization = f'{Output}\\Visualization'
    os.makedirs(Dasboard, exist_ok=True)
    shutil.copy(f"{csv_folder}\\OR_4_1_9.csv", f"{Dasboard}")
    shutil.copy(f"{csv_folder}\\OR_4_2_9.csv", f"{Dasboard}")
    
def create_download():
    Output=f'{ROOT_DIR}'
    Reports = f'{Output}\\Report'
    Visualization = f'{Output}\\Visualization'
    Source=f'{Output}\\Source'
    download = f'{Output}\\Download'
    os.makedirs(download, exist_ok=True)
    downloads=[Reports,Source]
    for i in downloads:
        try:
            shutil.rmtree(f"{download}\\{i}")
        except:
            pass
        new_folder = i.split("\\")[-1] 
        os.makedirs(f"{download}\\{new_folder}", exist_ok=True)
        shutil.copytree(i,f"{download}\\{new_folder}", symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)

def create_zip_archive():
    shutil.make_archive(f"{ROOT_DIR}\\Test_2", 'zip', f'{ROOT_DIR}\\Download')
    
    
def move():
    os.makedirs(f"{ROOT_DIR}\\Report", exist_ok=True)
    shutil.move(f"{ROOT_DIR}\\OR_9_1_1.xlsx", f"{ROOT_DIR}\\Report\\OR_9_1_1.xlsx")
    shutil.move(f"{ROOT_DIR}\\OR_9_1_2.xlsx", f"{ROOT_DIR}\\Report\\OR_9_1_2.xlsx")
    shutil.move(f"{ROOT_DIR}\\OR_9_1_3.xlsx", f"{ROOT_DIR}\\Report\\OR_9_1_3.xlsx")
    shutil.move(f"{ROOT_DIR}\\OR_9_2_1.xlsx", f"{ROOT_DIR}\\Report\\OR_9_2_1.xlsx")
    shutil.move(f"{ROOT_DIR}\\OR_9_2_2.xlsx", f"{ROOT_DIR}\\Report\\OR_9_2_2.xlsx")
    shutil.move(f"{ROOT_DIR}\\OR_9_2_3.xlsx", f"{ROOT_DIR}\\Report\\OR_9_2_3.xlsx")











def get_date_from_quarter(str_or_end, ind,year):
    Months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if str_or_end == 1:
        month = Months[((ind + 1) * 3) - 3]
    if str_or_end == 2:
        month = Months[((ind + 1) * 3) - 1]
    From_month_in_number = str(list(calendar.month_abbr).index(month))
    if len(From_month_in_number) < 2:
        From_month_in_number = f"0{From_month_in_number}"
    if str_or_end == 1:
        return f"{year}{From_month_in_number}01"
    else:
        days = monthrange(int(year), int(From_month_in_number))[1]
        return f"{year}{From_month_in_number}{days}"

def convert_csv_to_xlsx(csvfile, folder):
    name = csvfile[:-4] + '.xlsx'
    name = name.split("\\")[-1]
    workbook = Workbook(f"{folder}\\{name}")
    worksheet = workbook.add_worksheet()
    with open(csvfile, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()


def get_report(cursor, view, folder):
    logger.info("Creating Report for " + view) 
    csv_folder = f"{folder}\\csv"
    os.makedirs(csv_folder, exist_ok=True)
    #print(f'SELECT * FROM {view}')
    cursor.execute(f'SELECT * FROM {view}')
    # htdocs_out_csv_file = open(f'{csv_folder}\\{view.replace("_temp","")}.csv','w',encoding='utf-8',newline='')
    with open(f'{csv_folder}\\{view.replace("_temp", "")}.csv', 'w', encoding='utf-8', newline='') as out_csv_file:
        csv_out = csv.writer(out_csv_file)
        # csv_out1 = csv.writer(htdocs_out_csv_file)
        csv_out.writerow([d[0].replace('nan', 'Others') for d in cursor.description])
        # csv_out1.writerow([d[0] for d in cursor.description])
        for result in cursor:
            csv_out.writerow(result)
    #print(view)
    convert_csv_to_xlsx(f'{csv_folder}\\{view.replace("_temp", "")}.csv', folder)




try:
    conn = sqlite3.connect(DatabasePath)
    cur = conn.cursor()
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    logger.info("Script Finished")
    sys.exit(-1)



try:
    if len(sys.argv)<3:
        DateFrom,DateTo,Start_year,End_year = DolbyUI.Get_Period("Q1","Q4",f"{Start_year}")
        del sys.modules["DolbyUI"] 
        del DolbyUI
    else:
        DateFrom=sys.argv[1]
        DateTo=sys.argv[2]
        

    index1 = values.index(DateFrom)
    index2 = values.index(DateTo)
    from_date = get_date_from_quarter(1, index1,Start_year)
    to_date = get_date_from_quarter(2, index2,End_year)
    #print(from_date, to_date)
    DateFrom=from_date
    DateTo=to_date

    cur.execute('PRAGMA auto_vacuum = 1;') #PRAGMA

    logger.info('Date From {0} To {1}'.format(DateFrom,DateTo))


    #Just for View what Parameters is passed by AutoIt - this need to be removed Later

    #if len(sys.argv) == 1:
    #TE_009
    #TE_009_1
    cur.execute('DROP VIEW IF EXISTS OR_9_1;') #delete any previus View OR_9_1 table

    #    Real query
    cur.execute('CREATE VIEW OR_9_1 AS SELECT CR_1.* '
    'FROM CR_1 '
    'WHERE ("Transaction_Date" BETWEEN {0} AND {1}) AND (("Parent_Expense_Type" LIKE "03%") OR ("Parent_Expense_Type" LIKE "04%") OR ("Parent_Expense_Type" LIKE "05%") OR ("Parent_Expense_Type" LIKE "06%") OR ("Parent_Expense_Type" LIKE "07%") OR ("Parent_Expense_Type" LIKE "11%") OR ("Parent_Expense_Type" LIKE "12%")) '
    'ORDER BY "Employee";'.format(DateFrom,DateTo))


    #    Create Table For Fuzzy
    cur.execute('DROP TABLE IF EXISTS OR_9_1_1;') #Table All Fuzzy
    cur.execute('CREATE TABLE OR_9_1_1 AS SELECT OR_9_1.* '
    'FROM OR_9_1;')
    #   Alter add Keyword and Distance
    cur.execute('ALTER TABLE OR_9_1_1 ADD Keyword TEXT;')
    cur.execute('ALTER TABLE OR_9_1_1 ADD distance INTEGER;')


    #Get all Purpose listPurpose_OR_9_1_1
    cur.execute('SELECT rowid,"Purpose" from OR_9_1_1') #OR_9_1_1 reference table  
    listPurpose_OR_9_1_1=cur.fetchall()
    # #print("listPurpose_OR_9_1_1")
    # #print(listPurpose_OR_9_1_1)

    #    Get Reference Keywords
    cur.execute('SELECT "Keyword" from EXT_9') #EXT_9 reference table  
    listKeywords_EXT_9=cur.fetchall()
    # #print("listKeywords_EXT_9")
    # #print(listKeywords_EXT_9)

    # #print("\nFuzzy OR_9_1_1>Keywords EXT_9")
    for id,Purpose in listPurpose_OR_9_1_1:
        highest = process.extractOne(Purpose,(row[0] for row in listKeywords_EXT_9)) #Check names 
        # #print(id,Purpose,'|',highest[0],highest[1])
        cur.execute("UPDATE OR_9_1_1 SET 'Keyword'=?, Distance=? WHERE rowid=?",(highest[0],highest[1],id))

    #   Create View OR_9_1_2 Match 100
    cur.execute('DROP VIEW IF EXISTS OR_9_1_2;') #table for Distance > 90
    cur.execute('CREATE VIEW OR_9_1_2 AS SELECT OR_9_1_1.* '
    'FROM OR_9_1_1 '
    'WHERE (Distance > 90)'
    'ORDER BY Distance DESC;')

    cur.execute('DROP VIEW IF EXISTS OR_9_1_3;')
    cur.execute('CREATE VIEW OR_9_1_3 AS SELECT OR_9_1.*, OR_9_1_2.Keyword, OR_9_1_2.Distance '
    'FROM OR_9_1 '
    'INNER JOIN OR_9_1_2 ON (OR_9_1.EMP_ID = OR_9_1_2.EMP_ID) AND (OR_9_1.Report__ = OR_9_1_2.Report__) AND (OR_9_1.Transaction_Date = OR_9_1_2.Transaction_Date) AND (OR_9_1.Purpose = OR_9_1_2.Purpose) '
    'ORDER BY OR_9_1_2.Distance DESC;')


    #TE_009_2
    cur.execute('DROP VIEW IF EXISTS OR_9_2;') #delete any previus View TE_009_2 table
    #    Real query   
    cur.execute('CREATE VIEW OR_9_2 AS SELECT CR_1.* '
    'FROM CR_1 '
    'WHERE ("Transaction_Date" BETWEEN {0} AND {1}) AND (("Parent_Expense_Type" LIKE "03%") OR ("Parent_Expense_Type" LIKE "04%") OR ("Parent_Expense_Type" LIKE "05%") OR ("Parent_Expense_Type" LIKE "06%") OR ("Parent_Expense_Type" LIKE "07%") OR ("Parent_Expense_Type" LIKE "11%") OR ("Parent_Expense_Type" LIKE "12%")) '
    'ORDER BY "Employee";'.format(DateFrom,DateTo))


    #    Create Table For Fuzzy
    cur.execute('DROP TABLE IF EXISTS OR_9_2_1;') #Table All Fuzzy
    cur.execute('CREATE TABLE OR_9_2_1 AS SELECT OR_9_2.* '
    'FROM OR_9_2;')
    #   Alter add Keyword and Distance
    cur.execute('ALTER TABLE OR_9_2_1 ADD Keyword TEXT;')
    cur.execute('ALTER TABLE OR_9_2_1 ADD distance INTEGER;')


    #Get all Purpose listPurpose_OR_9_2_1
    cur.execute('SELECT rowid,Purpose from OR_9_2_1') #OR_9_2_1 reference table  
    listPurpose_OR_9_2_1=cur.fetchall()
    # #print("listPurpose_OR_9_2_1")
    # #print(listPurpose_OR_9_2_1)

    #    Get Reference Keywords
    cur.execute('SELECT Keyword from EXT_9_2') #EXT_9_2 reference table  
    listKeywords_EXT_9_2=cur.fetchall()
    # #print("listKeywords_EXT_9_2")
    # #print(listKeywords_EXT_9_2)

    # #print("\nFuzzy OR_9_2_1>Keywords EXT_9_2")
    for id,Purpose in listPurpose_OR_9_2_1:
        highest = process.extractOne(Purpose,(row[0] for row in listKeywords_EXT_9_2)) #Check names 
        # #print(id,Purpose,'|',highest[0],highest[1])
        cur.execute("UPDATE OR_9_2_1 SET Keyword='{0}',Distance={1} WHERE rowid = {2}".format(highest[0],highest[1],id))



    #   Create View OR_9_2_2 Match 100
    cur.execute('DROP VIEW IF EXISTS OR_9_2_2;') #table for Distance > 90
    cur.execute('CREATE VIEW OR_9_2_2 AS SELECT OR_9_2_1.* '
    'FROM OR_9_2_1 '
    'WHERE (Distance > 90)'
    'ORDER BY Distance DESC;')

    cur.execute('DROP VIEW IF EXISTS OR_9_2_3;')
    cur.execute('CREATE VIEW OR_9_2_3 AS SELECT OR_9_2.*, OR_9_2_2.Keyword, OR_9_2_2.Distance  '
    'FROM OR_9_2 '
    'INNER JOIN OR_9_2_2 ON (OR_9_2.EMP_ID = OR_9_2_2.EMP_ID) AND (OR_9_2.Report__ = OR_9_2_2.Report__) AND (OR_9_2.Transaction_Date = OR_9_2_2.Transaction_Date) AND (OR_9_2.Purpose = OR_9_2_2.Purpose) '
    'ORDER BY OR_9_2_2.Distance DESC;')




    #if len(sys.argv) == 1:
    get_report(cur,"OR_9_1_1",Output_dir)
    get_report(cur,"OR_9_2_1",Output_dir)
    get_report(cur,"OR_9_1_2",Output_dir)
    get_report(cur,"OR_9_2_2",Output_dir)
    get_report(cur,"OR_9_1_3",Output_dir)
    get_report(cur,"OR_9_2_3",Output_dir)

    '''
    try:  
        #Export OR_9_1_1
        cur.execute('SELECT EMP_ID, Employee, Employee_Country_Code, Report_Name, Approved_Amount_RPT, Transaction_Date, Purpose, Keyword, Distance FROM OR_9_1_1 ORDER BY Distance DESC ')
        with open(ResultDirectory+'OR_9_1_1.csv','w',encoding='utf-8',newline='') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            # write header                        
            csv_out.writerow([d[0] for d in cur.description])
            # write data                          
            for result in cur:
            csv_out.writerow(result)
        
    except Exception as err:
        logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        sys.exit(-1)

    try:  
        #Export OR_9_2_1
        cur.execute('SELECT EMP_ID, Employee, Employee_Country_Code, Report_Name, Approved_Amount_RPT, Transaction_Date, Purpose, Keyword, Distance FROM OR_9_2_1 ORDER BY Distance DESC')
        with open(ResultDirectory+'OR_9_2_1.csv','w',encoding='utf-8',newline='') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            # write header                        
            csv_out.writerow([d[0] for d in cur.description])
            # write data                          
            for result in cur:
            csv_out.writerow(result)
        
    except Exception as err:
        logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))    
        sys.exit(-1)


    #Export Fuzzy CSV 
        
    try:  
        #Export OR_9_1_2
        cur.execute('SELECT * FROM OR_9_1_2 ORDER BY Distance DESC')
        htdocs_out_csv_file = open(HtdocsResultDirectory+'OR_9_1_2.csv','w',encoding='utf-8',newline='')
        with open(ResultDirectory+'OR_9_1_2.csv','w',encoding='utf-8',newline='') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            csv_out1 = csv.writer(htdocs_out_csv_file)
            # write header                        
            csv_out.writerow([d[0] for d in cur.description])
            csv_out1.writerow([d[0] for d in cur.description])
            # write data                          
            for result in cur:
            csv_out.writerow(result)
            csv_out1.writerow(result) 

        
        cur.execute('SELECT * FROM OR_9_1_3 ORDER BY Distance DESC')
        htdocs_out_csv_file = open(HtdocsResultDirectory+'OR_9_1_3.csv','w',encoding='utf-8',newline='')
        with open(ResultDirectory+'OR_9_1_3.csv','w',encoding='utf-8',newline='') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            csv_out1 = csv.writer(htdocs_out_csv_file)
            # write header                        
            csv_out.writerow([d[0] for d in cur.description])
            csv_out1.writerow([d[0] for d in cur.description])
            # write data                          
            for result in cur:
            csv_out.writerow(result)
            csv_out1.writerow(result) 

    except Exception as err:
        logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        sys.exit(-1)
        

    try:  
        #Export OR_9_2_2
        cur.execute('SELECT * FROM OR_9_2_2 ORDER BY Distance DESC')
        htdocs_out_csv_file = open(HtdocsResultDirectory+'OR_9_2_2.csv','w',encoding='utf-8',newline='')
        with open(ResultDirectory+'OR_9_2_2.csv','w',encoding='utf-8',newline='') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            csv_out1 = csv.writer(htdocs_out_csv_file)
            # write header                        
            csv_out.writerow([d[0] for d in cur.description])
            csv_out1.writerow([d[0] for d in cur.description])
            # write data                          
            for result in cur:
            csv_out.writerow(result)
            csv_out1.writerow(result) 
        
        cur.execute('SELECT * FROM OR_9_2_3 ORDER BY Distance DESC')
        htdocs_out_csv_file = open(HtdocsResultDirectory+'OR_9_2_3.csv','w',encoding='utf-8',newline='')
        with open(ResultDirectory+'OR_9_2_3.csv','w',encoding='utf-8',newline='') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
            csv_out1 = csv.writer(htdocs_out_csv_file)
            # write header                        
            csv_out.writerow([d[0] for d in cur.description])
            csv_out1.writerow([d[0] for d in cur.description])
            # write data                          
            for result in cur:
            csv_out.writerow(result)
            csv_out1.writerow(result) 

    except Exception as err:
        logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        sys.exit(-1)

    finished")
    '''
    conn.commit()
    conn.close()
    logger.info("Script Finished")
    logger.handlers = []
    logging.shutdown()


    '''
    try:
        result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\PS_Export_Test_09.py'], stdout=subprocess.PIPE)
        if len(sys.argv) == 1:
            msgbox_info("Exported" ,"Process " + testname + " Exported")
    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode))
        #print(result)
    try:
        result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_09_visualization.py'], stdout=subprocess.PIPE)
        #print(result)
    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode))  
    create_link.create_html("C:/AIVER/Dash/TestResultsForVisual/Test_09/")
    if len(sys.argv) == 1:
        msgbox_info("All Processed" ,"Process " + testname + " finished")
    sys.exit(0)
    '''

    move()


    sys.exit(0)
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)