# -*- coding: utf-8 -*-

import logging
import sqlite3
import sys #handle parameters
import os
import csv
import uuid
import tkinter, tkinter.messagebox
import subprocess
import customtkinter
import datetime
import calendar
from calendar import monthrange
from xlsxwriter.workbook import Workbook
import plotly.graph_objects as go
import pandas as pd
import os
import shutil
import sys




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

data=var.data["Test_05"]


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
TEST_DIR = f"{ROOT_DIR}\\Test_5"
DatabasePath = f'{ROOT_DIR}\\..\\DataBase\\Dolby.db'
#Source_Dir = f"{TEST_DIR}\\Source_Dir"

LogsPath = f"{TEST_DIR}\\Logs"    
Output_dir= f"{TEST_DIR}\\Output"
csv_folder = f'{Output_dir}\\csv'
HtdocsResultDirectory=f"{TEST_DIR}\\Output\\csv"
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
    shutil.move(f"{Output_dir}\\OR_5_1.xlsx", f"{Output_dir}\\Report\\OR_5_1.xlsx")
    shutil.move(f"{Output_dir}\\OR_5_2_3_1.xlsx", f"{Output_dir}\\Report\\OR_5_2_3_1.xlsx")
    shutil.move(f"{Output_dir}\\OR_5_2_3_2.xlsx", f"{Output_dir}\\Report\\OR_5_2_3_2.xlsx")





try:
    conn = sqlite3.connect(DatabasePath)
    cur = conn.cursor()
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    logger.info("Script Finished")
    sys.exit(-1)

if len(sys.argv)<3:
    DateFrom,DateTo,Start_year,End_year = DolbyUI.Get_Period("Q1","Q4",f"{Start_year}")
    del sys.modules["DolbyUI"] 
    del DolbyUI
else:
    DateFrom=sys.argv[1]
    DateTo=sys.argv[2]
    

##index1 = values.index(DateFrom)
##index2 = values.index(DateTo)
##from_date = get_date_from_quarter(1, index1,Start_year)
##to_date = get_date_from_quarter(2, index2,End_year)
#print(from_date, to_date)
##DateFrom=from_date
##DateTo=to_date


if len(sys.argv) < 3:
    index1 = values.index(DateFrom)
    index2 = values.index(DateTo)
    from_date = get_date_from_quarter(1, index1,Start_year)
    to_date = get_date_from_quarter(2, index2,End_year)
else:
    from_date=sys.argv[1]
    to_date=sys.argv[2]



cur.execute('PRAGMA auto_vacuum = 1;') #PRAGMA

logger.info('Date From {0} To {1}'.format(DateFrom,DateTo))

try:
    #START TE_005_1

    #TE_005_1
        cur.execute('DROP VIEW IF EXISTS OR_5_1;')
        select= '''SELECT CR_1.* 
        FROM CR_1 
        WHERE ("Transaction_Date" BETWEEN {0} AND {1}) AND ("Parent_Expense_Type" = "05. Government Official Expenses") 
        AND ("Approval_Status" = "Approved") 
        AND ("Employee_Country_Code" = "US") 
        ORDER BY "Transaction_Date";'''.format(DateFrom,DateTo)
        #print(select)
        cur.execute(f'CREATE VIEW OR_5_1 AS {select}')

except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

    #END TE_005_1

try:
    #START TE_005_2

    #TE_005_2_1
    cur.execute('DROP VIEW IF EXISTS OR_5_2_1;') #delete any previus View OR_5_1 table
    cur.execute('CREATE VIEW OR_5_2_1 AS SELECT CR_1.* '
    'FROM CR_1 '
    'WHERE ("Transaction_Date" BETWEEN {0} AND {1}) AND ("Parent_Expense_Type" = "05. Government Official Expenses") '
    'AND ("Approval_Status" = "Approved") '
    'AND ("Employee_Country_Code" != "US") '
    'ORDER BY "Employee_Country_Code", "EMP_ID", "Transaction_Date"; '.format(DateFrom,DateTo))

    #TE_005_2_2
    cur.execute('DROP VIEW IF EXISTS OR_5_2_2;') #delete any previus View TE_2_2_2 table
    cur.execute('CREATE VIEW OR_5_2_2 AS '
    'SELECT "EMP_ID", "Employee_Name", "Employee_Country_Code", "Employee_Org_Unit_2_Code", "Transaction_Date", "Expense_Type", round(sum("Approved_Amount_RPT"),2) AS "Sum(Approved_Amount_RPT)" '
    'FROM OR_5_2_1 '
    'GROUP BY "EMP_ID", "Employee_Name", "Employee_Country_Code", "Employee_Org_Unit_2_Code", "Transaction_Date", "Expense_Type" '
    'HAVING "Sum(Approved_Amount_RPT)" > {0} '
    'ORDER BY "Sum(Approved_Amount_RPT)" DESC, OR_5_2_1."EMP_ID"; '.format(data["TE_005_2_2"]))

    #TE_005_2_3_1
    cur.execute('DROP VIEW IF EXISTS OR_5_2_3_1;') #delete any previus View TE_2_2_2 table
    cur.execute('CREATE VIEW OR_5_2_3_1 AS '
    'SELECT OR_5_2_1.*, OR_5_2_2."Sum(Approved_Amount_RPT)" '
    'FROM OR_5_2_1 '
    'INNER JOIN OR_5_2_2 ON (OR_5_2_1."EMP_ID" = OR_5_2_2."EMP_ID") AND (OR_5_2_1."Transaction_Date" = OR_5_2_2."Transaction_Date") AND (OR_5_2_1."Expense_Type" = OR_5_2_2."Expense_Type") '
    'WHERE OR_5_2_2."Expense_Type" = "Government Official Expenses/Gifts" AND OR_5_2_2."Sum(Approved_Amount_RPT)" > {0} '
    'ORDER BY OR_5_2_2."Sum(Approved_Amount_RPT)" DESC, OR_5_2_1."EMP_ID", OR_5_2_1."Transaction_Date"; '.format(data["TE_005_2_3_1"]))

    #TE_005_2_3_2
    cur.execute('DROP VIEW IF EXISTS OR_5_2_3_2; ')
    cur.execute('CREATE VIEW OR_5_2_3_2 AS '
    'SELECT OR_5_2_1.*, OR_5_2_2."Sum(Approved_Amount_RPT)" '
    'FROM OR_5_2_1 '
    'INNER JOIN OR_5_2_2 ON (OR_5_2_1."EMP_ID" = OR_5_2_2."EMP_ID") AND (OR_5_2_1."Transaction_Date" = OR_5_2_2."Transaction_Date") AND (OR_5_2_1."Expense_Type" = OR_5_2_2."Expense_Type") '
    'WHERE OR_5_2_2."Expense_Type" = "Government Official Expenses/Meals and Entertainment" AND OR_5_2_2."Sum(Approved_Amount_RPT)" > {0} '
    'ORDER BY OR_5_2_2."Sum(Approved_Amount_RPT)" DESC, OR_5_2_1."EMP_ID", OR_5_2_1."Transaction_Date"; '.format(data["TE_005_2_3_2"]))

except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

    #END TE_005_2

        #END TE_005_2
try:
    folder = f"{ROOT_DIR}"

    get_report(cursor, "OR_5_1", Output_dir )
    get_report(cursor, "OR_5_2_1", Output_dir )
    get_report(cursor, "OR_5_2_2", Output_dir )
    get_report(cursor, "OR_5_2_3_1", Output_dir )
    get_report(cursor, "OR_5_2_3_2", Output_dir )
    conn.commit()
    conn.close()
    logger.info("Script Finished")
    logger.handlers = []
    logging.shutdown()
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)


#try:
#    if len(sys.argv) == 1:
#        result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\PS_Export_Test_02.py'], stdout=subprocess.PIPE)
#        msgbox_info("Exported" ,"Process " + testname + " Exported")
#    else:
#        result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\PS_Export_Test_02.py',"1"], stdout=subprocess.PIPE)
#except subprocess.CalledProcessError as e:
#    sys.exit(int (e.returncode))
#    #print(result)
#try:
#    if len(sys.argv) == 1:
#        result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_02_visualization.py'], stdout=subprocess.PIPE)
#    else:
#        result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_02_visualization.py',"1"], stdout=subprocess.PIPE)
#    #print(result)
#except subprocess.CalledProcessError as e:
#    sys.exit(int (e.returncode))  

try:

    df1 = pd.read_csv(f'{csv_folder}\\OR_5_1.csv')
    df2 = pd.read_csv(f'{csv_folder}\\OR_5_2_3_1.csv')
    df3 = pd.read_csv(f'{csv_folder}\\OR_5_2_3_2.csv')

    yaxis_values=[]
    us_amt =df1[['Approved_Amount_rpt']].agg(['sum']).reset_index().round(0)
    # #print(us_amt)
    # #print(us_amt['Approved_Amount_RPT'][0])
    yaxis_values.append(int(us_amt['Approved_Amount_rpt'][0]))

    nonus_gifts =df2[['Approved_Amount_rpt']].agg(['sum']).reset_index().round(0)
    yaxis_values.append(int(nonus_gifts['Approved_Amount_rpt'][0]))

    nonus_meals =df3[['Approved_Amount_rpt']].agg(['sum']).reset_index().round(0)
    yaxis_values.append(int(nonus_meals['Approved_Amount_rpt'][0]))
    # #print(yaxis_values)


    '''
    yaxis_dollar=[]
    for i in yaxis_values:
        i = '${{}}'.format(i)
        yaxis_dollar.append(i)
    # #print(type(yaxis_values))

    colors = ['crimson','indianred','lightsalmon']
    fig = go.Figure(go.Bar(
        x=['US','Non US - Gifts','Non US - Meals'],
        y=yaxis_values,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
        ),
        text=yaxis_dollar,
        # texttemplate='$',
        textposition='outside',

    ))
    fig.update_yaxes(title_text="Amount (USD)")

    fig.update_layout(
        width=800, height=500,
        # coloraxis=dict(colorscale='Bluered_r'),
        title_text='<b>'+'Government Meals & Entertainment For Approval'+'</b>',
        title_x=0.5,
        yaxis=dict(
            showgrid=False,
            showline=True,
            showticklabels=True,
            # domain=[0, 0.85],
            # # autorange="reversed",
            # automargin=False,
        ),
        xaxis=dict(
            # tickangle=45,
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=False,
            # domain=[0, 0.3],
        ),
    )
    import plotly
    plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_02/Test_02.html', auto_open=False)
    # fig.show()
    #print('\n\n\nGraph generated and saved in file location, plot show disabled')

    '''
    #filename='C:/AIVER/Dash/TestResultsForVisual/Test_02/Test_02.html'
    filename=f'{html_dir_dir}\\Test_05.html'
    headers=["Us","Non Us Gifts", "Non Us Meals"]
    data=[int(us_amt['Approved_Amount_rpt'][0]),int(nonus_gifts['Approved_Amount_rpt'][0]),int(nonus_meals['Approved_Amount_rpt'][0])]
    html = creategraph(filename,headers,data)        
    with open(filename,"w") as html_writer:
        html_writer.write(html)
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)





try:
    move()


    create_link.create_html(f"{csv_folder}")
    #if len(sys.argv) == 1:
    #    msgbox_info("All Processed" ,"Process " + testname + " finished")
    sys.exit(0)
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)