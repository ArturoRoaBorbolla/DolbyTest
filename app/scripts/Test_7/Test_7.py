# -*- coding: utf-8 -*-

import logging
import sqlite3
import sys #handle parameters
import os
import csv
import uuid
import tkinter, tkinter.messagebox
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
import os
import shutil




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

data=var.data["Test_07"]


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
TEST_DIR = f"{ROOT_DIR}\\Test_7"
DatabasePath = f'{ROOT_DIR}\\..\\DataBase\\Dolby.db'
Source_Dir = f"{TEST_DIR}\\Source_Dir"

LogsPath = f"{TEST_DIR}\\Logs"    
Output_dir= f"{TEST_DIR}\\Output"
csv_folder = f'{Output_dir}\\csv'
html_dir= f'{Output_dir}\\html'


os.makedirs(LogsPath, exist_ok=True)
os.makedirs(Output_dir, exist_ok=True)
os.makedirs(csv_folder, exist_ok=True)
os.makedirs(Source_Dir, exist_ok=True)
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
    os.makedirs(f"{Output_dir}\\Report", exist_ok=True)
    shutil.move(f"{Output_dir}\\OR_07_1.xlsx", f"{Output_dir}\\Report\\OR_07_1.xlsx")
    shutil.move(f"{Output_dir}\\OR_07_2.xlsx", f"{Output_dir}\\Report\\OR_07_2.xlsx")
    shutil.move(f"{Output_dir}\\OR_07_3.xlsx", f"{Output_dir}\\Report\\OR_07_3.xlsx")
    shutil.move(f"{Output_dir}\\OR_07_4_1.xlsx", f"{Output_dir}\\Report\\OR_07_4_1.xlsx")
    shutil.move(f"{Output_dir}\\OR_07_4_2.xlsx", f"{Output_dir}\\Report\\OR_07_4_2.xlsx")
    shutil.move(f"{Output_dir}\\OR_07_4_3.xlsx", f"{Output_dir}\\Report\\OR_07_4_3.xlsx")



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

    #TE_010
    #TE_10_1    
    cur.execute('DROP VIEW IF EXISTS OR_07_1; ') #delete any previus View OR_07_1 table
    select= '''SELECT * 
    FROM CR_1 
    WHERE ("Transaction_Date" BETWEEN {0} AND {1}) AND ("Approval_Status" = "Approved" AND "Payment_Type" = "Out-of-Pocket") 
    ORDER BY "EMP_ID"; '''.format(DateFrom,DateTo)
    #print(select)
    cur.execute(f'CREATE VIEW OR_07_1 as {select}')


    #TE_10_2
    cur.execute('DROP VIEW IF EXISTS OR_07_2; ') #delete any previus View OR_07_2 table
    select= '''SELECT  "EMP_ID", "Employee", "Employee_Org_Unit_2_Code", "Employee_Country_Code", 
    sum("Approved_Amount__rpt_") AS "Sum(Approved_Amount_RPT)", 
    count("Payment_Type") AS "Count(Submissions)", 
    (sum("Approved_Amount__rpt_")/ count("Payment_Type")) AS "Average Claim Per Report" 
    FROM OR_07_1 
    GROUP BY "EMP_ID", "Employee", "Employee_Org_Unit_2_Code", "Employee_Country_Code" 
    HAVING "Sum(Approved_Amount_RPT)" > {0} 
    ORDER BY "Sum(Approved_Amount_RPT)" DESC, "Average Claim Per Report" DESC, "Employee_Org_Unit_2_Code"; '''.format(data["TE_007_2"])
    #print(select)
    cur.execute(f'CREATE VIEW OR_07_2 AS {select}')
    #TE_10_3
    cur.execute('DROP VIEW IF EXISTS OR_07_3; ') #delete any previus View OR_07_3 table
    cur.execute('CREATE VIEW OR_07_3 AS SELECT OR_07_1.*, OR_07_2."Sum(Approved_Amount_RPT)" '
    'FROM OR_07_1 '
    'INNER JOIN OR_07_2 ON (OR_07_1."EMP_ID" = OR_07_2."EMP_ID") AND (OR_07_1."Employee_Country_Code" = OR_07_2."Employee_Country_Code") '
    'ORDER BY OR_07_2."Sum(Approved_Amount_RPT)" DESC, OR_07_1."Employee_Country_Code"; ')

    #TE_10_4_1
    cur.execute('DROP VIEW IF EXISTS OR_07_4_1; ') #delete any previus View OR_07_4_1 table
    cur.execute('CREATE VIEW OR_07_4_1 AS SELECT * '
    'FROM OR_07_2 '
    'WHERE "Employee_Org_Unit_2___Code" LIKE "{0}" '
    'LIMIT 25; '.format(data["TE_007_4_1"]))

    #TE_10_4_2
    cur.execute('DROP VIEW IF EXISTS OR_07_4_2; ') #delete any previus View OR_07_4_1 table
    cur.execute('CREATE VIEW OR_07_4_2 AS SELECT * '
    'FROM OR_07_2 '
    'WHERE "Employee_Org_Unit_2___Code" LIKE "{0}" '
    'LIMIT 25; '.format(data["TE_007_4_2"]))

    #TE_10_4_3
    cur.execute('DROP VIEW IF EXISTS OR_07_4_3; ') #delete any previus View OR_07_4_1 table
    cur.execute('CREATE VIEW OR_07_4_3 AS SELECT * '
    'FROM OR_07_2 '
    'WHERE "Employee_Org_Unit_2___Code" LIKE "{0}" '
    'LIMIT 25; '.format(data["TE_007_4_3"]))


except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)







try:
    if len(sys.argv) == 1:
        #START Export Report Function

        #Export OR_07_1
        #cur.execute('SELECT * FROM OR_07_1 ')
        get_report(cur,"OR_07_1",Output_dir)
        get_report(cur,"OR_07_2",Output_dir)
        get_report(cur,"OR_07_3",Output_dir)
        get_report(cur,"OR_07_4_3",Output_dir)
        get_report(cur,"OR_07_4_1",Output_dir)
        get_report(cur,"OR_07_4_2",Output_dir)
       
        
        
 
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

#Script Finished Information Message Box
#msgbox_info("All Processed" ,"Process " + testname + " finished")
try:
    conn.commit()
    conn.close()
    logger.info("Script Finished")
    logger.handlers = []
    logging.shutdown()



    from create_graph import creategraph
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

try:
    df = pd.read_csv(f'{csv_folder}\\OR_07_4_3.csv')

    # df = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\OR_07_4_3.csv')

    alter_columns = ['Employee ID', 'Name', 'Employee_Org_Unit_2_Code', 'Country', 'Total Amount (USD)', 'Submission Count', 'Average Claim Per Report']

    fig = go.Figure(data=[go.Table(

        header=dict(values=['<b>'+ x +'</b>' for x in list(alter_columns)],
                    fill_color='paleturquoise',
                    align='right',
                    ),

        cells=dict(
                # values=df.values.T, # to transpose DF values into cells
                values=[df['EMP_ID'],df['Employee'],df['Employee_Org_Unit_2_Code'],df['Employee_Country_Code'],
                        df['Sum(Approved_Amount_RPT)'].apply(lambda x:f"${str(round(x,2))}"),df['Count(Submissions)'],
                        df['Average Claim Per Report'].round(2)],
                fill_color='lavender',
                align='right'))
    ])
    fig.update_layout(
        # width=1100,
        height=500,
        title_text='<b>'+'Top 25 Submitters of Out-of-Pocket Expenses'+'</b>',
        title_x=0.5,
        )

    import plotly
    import os
    #if not os.path.exists("C:\AIVER\Dash\TestResultsForVisual\Test_10"):
    #    os.mkdir("C:\AIVER\Dash\TestResultsForVisual\Test_10")
    plotly.offline.plot(fig, filename=f'{html_dir}\\Test_10.html', auto_open=False)
    # fig.show()

    #print('\n\n\nGraph generated and saved in file location, plot show disabled')
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)
try:
    move()
    sys.exit(0)
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)