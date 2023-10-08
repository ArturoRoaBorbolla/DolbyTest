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
import pandas as pd
import sys
import shutil




PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, f'{PRO_DIR}\\common')
sys.path.insert(2, f'{PRO_DIR}\\Scripts_UI')

import get_data
import create_link
import DolbyUI
import var
from create_graph import creategraph
import visualize




customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

data=var.data["Test_06"]


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
TEST_DIR = f"{ROOT_DIR}\\Test_6"
DatabasePath = f'{ROOT_DIR}\\..\\DataBase\\Dolby.db'
#Source_Dir = f"{TEST_DIR}\\Source_Dir"


LogsPath = f"{TEST_DIR}\\Logs"    
Output_dir= f"{TEST_DIR}\\Output"
csv_folder = f'{Output_dir}\\csv'
#HtdocsResultDirectory=f"{TEST_DIR}\\Output\\csv"
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
    os.makedirs(f"{Output_dir}\\Report", exist_ok=True)
    shutil.move(f"{Output_dir}\\OR_6.xlsx", f"{Output_dir}\\Report\\OR_6.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_1_1.xlsx", f"{Output_dir}\\Report\\OR_6_1_1.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_1_2.xlsx", f"{Output_dir}\\Report\\OR_6_1_2.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_1_3.xlsx", f"{Output_dir}\\Report\\OR_6_1_3.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_2.xlsx", f"{Output_dir}\\Report\\OR_6_2.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_2_1.xlsx", f"{Output_dir}\\Report\\OR_6_2_1.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_3_1.xlsx", f"{Output_dir}\\Report\\OR_6_3_2.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_3_2.xlsx", f"{Output_dir}\\Report\\OR_6_3_2.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_3_3.xlsx", f"{Output_dir}\\Report\\OR_6_3_3.xlsx")
    shutil.move(f"{Output_dir}\\OR_6_3_3_1.xlsx", f"{Output_dir}\\Report\\OR_6_3_3_1.xlsx")











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
    print(f'SELECT * FROM {view}')
    cursor.execute(f'SELECT * FROM {view}')
    # htdocs_out_csv_file = open(f'{csv_folder}\\{view.replace("_temp","")}.csv','w',encoding='utf-8',newline='')
    with open(f'{csv_folder}\\{view.replace("_temp", "")}.csv', 'w', encoding='utf-8', newline='') as out_csv_file:
        csv_out = csv.writer(out_csv_file)
        # csv_out1 = csv.writer(htdocs_out_csv_file)
        csv_out.writerow([d[0].replace('nan', 'Others') for d in cursor.description])
        # csv_out1.writerow([d[0] for d in cursor.description])
        for result in cursor:
            csv_out.writerow(result)
    print(view)
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
    print(from_date, to_date)
    DateFrom=from_date
    DateTo=to_date

    cur.execute('PRAGMA auto_vacuum = 1;') #PRAGMA

    logger.info('Date From {0} To {1}'.format(DateFrom,DateTo))
    #try:

    #TE_008_1
    #TE_008_1_1
    # cur.execute('DROP VIEW IF EXISTS OR_6_1_1;') #delete any previus View OR_6_1_1 table

    # cur.execute('CREATE VIEW OR_6_1_1 AS SELECT CR_1.*, substr(CR_1."Transaction_Date",1,4) as "Year", substr(CR_1."Transaction_Date",5,2) as "Month", '
    # 'substr(CR_1."Parent_Expense_Type",1,2) as "Parent_ExpenseType_Code"'
    # 'FROM CR_1;')
    # cur.execute('DROP TABLE IF EXISTS OR_6; ')

    cur.execute('DROP VIEW IF EXISTS OR_6; ')
    cur.execute('CREATE VIEW OR_6 '
    'AS SELECT CR_1.*, '
    'substr(CR_1."Transaction_Date",5,2) as "Month", '
    'CAST(substr(CR_1."Transaction_Date",1,4) AS int) as "C_Year", '
    'CASE '
    'WHEN CAST(substr(CR_1."Transaction_Date",5,2) AS int) >= 1 AND  CAST(substr(CR_1."Transaction_Date",5,2) AS int) <= 3 THEN "02" '
    'WHEN CAST(substr(CR_1."Transaction_Date",5,2) AS int) >= 4 AND  CAST(substr(CR_1."Transaction_Date",5,2) AS int) <= 6 THEN "03" '
    'WHEN CAST(substr(CR_1."Transaction_Date",5,2) AS int) >= 7 AND  CAST(substr(CR_1."Transaction_Date",5,2) AS int) <= 9 THEN "04" '
    'ELSE "01" '
    'END "F_Qtr", '
    'CASE '
    'WHEN CAST(substr(CR_1."Transaction_Date",5,2) AS int) >= 1 AND  CAST(substr(CR_1."Transaction_Date",5,2) AS int) <= 9 THEN CAST(substr(CR_1."Transaction_Date",1,4) AS int) '
    'ELSE (CAST(substr(CR_1."Transaction_Date",1,4) AS int) + 1) '
    'END "F_Year" '
    'FROM CR_1 '
    'WHERE ("Transaction_Date" BETWEEN {0} AND {1}); '.format(DateFrom,DateTo))

    cur.execute('DROP VIEW IF EXISTS OR_6_1; ')
    cur.execute('CREATE VIEW OR_6_1 '
    'AS SELECT "EMP_ID", "Employee", "Employee_Org_Unit_2___Code", "Employee_Country_Code", round(sum("Approved_Amount__rpt_"), 2) AS "Sum(Approved_Amount_RPT)" '
    'FROM OR_6 '
    'GROUP BY "EMP_ID", "Employee", "Employee_Org_Unit_2___Code", "Employee_Country_Code" '
    'ORDER BY "Sum(Approved_Amount_RPT)" DESC, "Employee_Country_Code", "Employee_Org_Unit_2___Code", "EMP_ID", "Employee"; ')

    cur.execute('DROP VIEW IF EXISTS OR_6_1_1; ')
    select = f'''SELECT *  FROM OR_6_1  WHERE "Employee_Org_Unit_2___Code" LIKE "{data["OR_6_1_1"]}" LIMIT 25; '''
    print(select)
    cur.execute(f'CREATE VIEW OR_6_1_1  AS {select}' )

    cur.execute('DROP VIEW IF EXISTS OR_6_1_2; ')
    cur.execute('CREATE VIEW OR_6_1_2 '
    'AS SELECT * '
    'FROM OR_6_1 '
    'WHERE "Employee_Org_Unit_2___Code" LIKE "{0}" '
    'LIMIT 25; '.format(data["OR_6_1_2"]))

    # cur.execute('DROP TABLE IF EXISTS OR_6_1_3; ')
    cur.execute('DROP VIEW IF EXISTS OR_6_1_3; ')
    cur.execute('CREATE VIEW OR_6_1_3 '
    'AS SELECT * '
    'FROM OR_6_1 '
    'WHERE "Employee_Org_Unit_2___Code" LIKE "{0}" '
    'LIMIT 25; '.format(data["OR_6_1_3"]))

    cur.execute('DROP VIEW IF EXISTS OR_6_2; ')
    cur.execute('CREATE VIEW OR_6_2 '
    'AS SELECT "Parent_Expense_Type", "Expense_Type", "F_Qtr", "F_Year", "Employee_Org_Unit_2___Code", (CAST(substr("Employee_Org_Unit_2_Code",1,2) AS varchar)) AS "REGION", "Employee_Country_Code", round(sum("Approved_Amount__rpt_"), 2) AS "Sum(Approved_Amount_RPT)" '
    'FROM OR_6 '
    'GROUP BY "Expense_Type", "F_Qtr", "F_Year", "Employee_Org_Unit_2___Code", "Employee_Country_Code" '
    'ORDER BY "Employee_Org_Unit_2___Code", "Employee_Country_Code", "Expense_Type", "F_Qtr", "F_Year"; ')

    cur.execute('DROP VIEW IF EXISTS OR_6_2_1; ')
    cur.execute(''' CREATE VIEW OR_6_2_1 AS SELECT "Parent_Expense_Type", "F_Qtr", "F_Year",
                    CASE
                            WHEN "REGION" = "10" THEN "NAMERICA" 
                            WHEN "REGION" = "20" THEN "EMEA" 
                            ELSE "APAC" 
                            END "GEO", 
                    round(sum("Sum(Approved_Amount_RPT)"), 2) AS "Sum(Approved_Amount)" 
                    FROM OR_6_2 
                    WHERE "Parent_Expense_Type" LIKE "01%" OR "Parent_Expense_Type" LIKE "02%" 
                    OR "Parent_Expense_Type" LIKE "03%" OR "Parent_Expense_Type" LIKE "04%" 
                    OR "Parent_Expense_Type" LIKE "05%" OR "Parent_Expense_Type" LIKE "06%" OR "Parent_Expense_Type" LIKE "07%" 
                    GROUP BY "Parent_Expense_Type", "F_Qtr", "F_Year", "GEO" 
                    ORDER BY "Parent_Expense_Type", "F_Qtr", "F_Year", "GEO"; ''')

    # cur.execute('CREATE TABLE OR_6_2_1 '
    # 'AS SELECT "Parent_Expense_Type", "F_Qtr", "F_Year", '
    # 'CASE'
    #     'WHEN "REGION" like "10%" THEN "NAMERICA" '
    #     'WHEN "REGION" like "20%" THEN "EMEA" '
    #     'ELSE "APAC" '
    #     'END "GEO", '
    # 'round(sum("Sum(Approved_Amount_RPT)"), 2) AS "Sum(Approved_Amount)" '
    # 'FROM OR_6_2 '
    # 'WHERE "Parent_Expense_Type" LIKE "01%" OR "Parent_Expense_Type" LIKE "02%" OR "Parent_Expense_Type" LIKE "03%" OR "Parent_Expense_Type" LIKE "04%" OR "Parent_Expense_Type" LIKE "05%" OR "Parent_Expense_Type" LIKE "06%" OR "Parent_Expense_Type" LIKE "07%" '
    # 'GROUP BY "Parent_Expense_Type", "F_Qtr", "F_Year", "GEO" '
    # 'ORDER BY "Parent_Expense_Type", "F_Qtr", "F_Year", "GEO"; ')

    cur.execute('DROP VIEW IF EXISTS OR_6_3_1; ')
    cur.execute('CREATE VIEW OR_6_3_1 '
    'AS SELECT * '
    'FROM OR_6_2 '
    'WHERE "Employee_Org_Unit_2___Code" LIKE "10%"; ')

    cur.execute('DROP VIEW IF EXISTS OR_6_3_2; ')
    cur.execute('CREATE VIEW OR_6_3_2 '
    'AS SELECT * '
    'FROM OR_6_2 '
    'WHERE "Employee_Org_Unit_2___Code" LIKE "20%"; ')

    cur.execute('DROP VIEW IF EXISTS OR_6_3_3; ')
    cur.execute('CREATE VIEW OR_6_3_3 '
    'AS SELECT * '
    'FROM OR_6_2 '
    'WHERE "Employee_Org_Unit_2___Code" LIKE "30%"; ')

    cur.execute('DROP VIEW IF EXISTS OR_6_3_3_1; ')
    cur.execute('CREATE VIEW OR_6_3_3_1 '
    'AS SELECT "F_Qtr", "F_Year", "Parent_Expense_Type", "Sum(Approved_Amount_RPT)" '
    'FROM OR_6_3_3 '
    'WHERE OR_6_3_3."Employee_Country_Code" = "AU"; ')





    #except Exception as err:
    #    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    #    sys.exit(-1)



    '''
    try:
        cur.execute('SELECT * FROM OR_6_3_3_1')
        htdocs_out_csv_file = open(Htdocsf'{csv_folder}\\OR_6_3_3_1.csv','w',encoding='utf-8',newline='')
        with open(f'{csv_folder}\\OR_6_3_3_1.csv','w',encoding='utf-8',newline='') as out_csv_file:
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

    #Script Finished Information Message Box
    #msgbox_info("All Processed" ,"Process " + testname + " finished")
    '''



    #try:
        #if len(sys.argv) == 1:
            #START Export Report Function

            #Export OR_07_1
            #cur.execute('SELECT * FROM OR_07_1 ')
    get_report(cur,"OR_6",Output_dir)
    get_report(cur,"OR_6_1_1",Output_dir)
    get_report(cur,"OR_6_1_2",Output_dir)
    get_report(cur,"OR_6_1_3",Output_dir)
    get_report(cur,"OR_6_2",Output_dir)
    get_report(cur,"OR_6_2_1",Output_dir)
    get_report(cur,"OR_6_3_1",Output_dir)
    get_report(cur,"OR_6_3_2",Output_dir)
    get_report(cur,"OR_6_3_3",Output_dir)
    get_report(cur,"OR_6_3_3_1",Output_dir)

            
            
    
    #except Exception as err:
    #    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    #    sys.exit(-1)

    #Script Finished Information Message Box
    #msgbox_inf o("All Processed" ,"Process " + testname + " finished")

    conn.commit()
    conn.close()
    logger.info("Script Finished")
    logger.handlers = []
    logging.shutdown()
    #sys.exit(0)
    '''
    try:
        if len(sys.argv) == 1:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_visualization.py'], stdout=subprocess.PIPE)
            print(result)
        else:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_visualization.py',"1"], stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode))  
    try:
        if len(sys.argv) == 1:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_2_APAC.py'], stdout=subprocess.PIPE)
            print(result)
        else:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_2_APAC.py',"1"], stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode))
    try:
        if len(sys.argv) == 1:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_2_EMEA.py'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_2_EMEA.py',"1"], stdout=subprocess.PIPE)
        print(result)
    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode))
    try:
        if len(sys.argv) == 1:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_2_NAmerica.py'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_2_NAmerica.py',"1"], stdout=subprocess.PIPE)
        print(result)
    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode))
    try:
        if len(sys.argv) == 1:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_3_APAC.py'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_3_APAC.py',"1"], stdout=subprocess.PIPE)
        print(result)
    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode))
    try:
        if len(sys.argv) == 1:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_3_EMEA.py'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_3_EMEA.py',"1"], stdout=subprocess.PIPE)
        print(result)
    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode))
    try:
        if len(sys.argv) == 1:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_3_NAmerica.py'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['python', f'{ROOT_DIR}\\scripts\\Test_08_3_NAmerica.py',"1"], stdout=subprocess.PIPE)
        print(result)
    except subprocess.CalledProcessError as e:
        sys.exit(int (e.returncode)) 
    '''
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

############APAC_2
try:
    df1 = pd.read_csv(f'{csv_folder}\\OR_6_2_1.csv')
    df2 = df1[(df1['GEO'] == 'APAC')]
    df3=df2.sort_values(by=['F_Qtr','F_Year','Sum(Approved_Amount)'],ascending=False)


    # for region  APAC
    pv1 = pd.pivot_table(df3, columns=['F_Qtr', 'F_Year'], index=["Parent_Expense_Type"], values=['Sum(Approved_Amount)'],
                        aggfunc=sum, fill_value=0)
    r11 = pv1.droplevel(0, axis=1)
    r11.columns = [str(col[1]) + '/Q' + str(col[0]) for col in r11.columns.values]
    # print(r11)
    a1 = r11.reset_index()

    a1.set_index("Parent_Expense_Type", inplace = True)
    #print(a1)

    legend=[]
    for col in a1.columns:
        d=a1[col].to_dict()
        e={k: d[k] for k in sorted(d, key=d.get, reverse=True)}
        legend.append(list(e.keys())[:5])
    # print(legend)
    import itertools
    leg=list(dict.fromkeys(itertools.chain.from_iterable(legend)))
    print(leg)

    # to find the odd parent type
    # res = list(set.intersection(*map(set, legend)))
    # print(res)
    # not_in=(list(set(legend) - set(res)))
    # print(not_in)

    # below sort independently each column values
    for col in a1.columns:
        if col not in ['Parent_Expense_Type']:
            a1[col] = sorted(a1[col], reverse=True)

    x1 = [col for col in a1.columns if col not in ['Parent_Expense_Type']]

    graph_values1 = a1#.drop(['Parent_Expense_Type'], axis=1)

    from plotly import graph_objects as go
    import plotly.express as px

    data = {
        "model_E1": list(graph_values1[0:1].values.flatten()),
        "model_E2": list(graph_values1[1:2].values.flatten()),
        "model_E3": list(graph_values1[2:3].values.flatten()),
        "model_E4": list(graph_values1[3:4].values.flatten()),
        "model_E5": list(graph_values1[4:5].values.flatten()),
        "labels": x1
    }
    '''
    print(leg)
    fig = go.Figure(
        data=[

            go.Bar(
                name=leg[0],
                x=data["labels"],
                y=data["model_E1"],
                offsetgroup=1,
            ),
            go.Bar(
                name=leg[1],
                x=data["labels"],
                y=data["model_E2"],
                offsetgroup=1,
                base=data["model_E1"],
            ),
            go.Bar(
                name=leg[2],
                x=data["labels"],
                y=data["model_E3"],
                offsetgroup=1,
                base=[val1 + val2 for val1, val2 in zip(data["model_E1"], data["model_E2"])],
            ),
            go.Bar(
                name=leg[3],
                x=data["labels"],
                y=data["model_E4"],
                offsetgroup=1,
                base=[val1 + val2 + val3 for val1, val2, val3 in zip(data["model_E1"], data["model_E2"], data["model_E3"])],
            ),
            go.Bar(
                name=leg[4],
                x=data["labels"],
                y=data["model_E5"],
                offsetgroup=1,
                base=[val1 + val2 + val3 + val4 for val1, val2, val3, val4 in
                    zip(data["model_E1"], data["model_E2"], data["model_E3"], data["model_E4"])],
            ),

        ],
        layout=go.Layout(
            title_text="<b>"+"Selected Parent Expense Types Trend Analysis for Region APAC"+"</br>",
            title_x=0.5,
            yaxis_title="<b>"+"Total Amount (USD)"+"</br>",
            xaxis_title="<b>"+"Fiscal Quarters"+"</br>",
            showlegend=True,
            legend_title='Parent Expense Type',
        )
    )

    import plotly
    plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_2_APAC.html', auto_open=False)
    print("Graph plotted and saved, show disabled")
    '''


    #fig.show()
    print()
    filename=f'{html_dir}\Test_06_2_APAC.html'
    headers=leg
    data=[list(a1.iloc[1])][0]
    print(data)
    print(len(data),len(headers))
    html = creategraph(filename,headers,data)        
    with open(filename,"w") as html_writer:
        html_writer.write(html)
    print('\n\n\nGraph generated and saved in file location, plot show disabled')
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

#############APAC_3
try:
    df1 = pd.read_csv(f'{csv_folder}\\OR_6_3_3.csv')

    r1=df1[['Parent_Expense_Type','Sum(Approved_Amount_RPT)','F_Qtr']].groupby(['F_Qtr','Parent_Expense_Type']).agg(['sum'])
    # print(r1)

    a=r1.droplevel(0, axis=1)
    a=a.reset_index()
    print(a)
    '''
    FiscalQtr=[]
    for i in a['F_Qtr']:
        i='Q'+str(i)
        FiscalQtr.append(i)


    # Region APAC

    fig=go.Figure(go.Bar(
        x=a['Parent_Expense_Type'],
        y=a['sum'],
        marker=dict(color=a['F_Qtr']),
        text=FiscalQtr,
        textposition='inside',
        #  texttemplate='Q',),
    ))


    fig.update_yaxes(title_text="Total Amount (USD)")

    # Change the bar mode
    fig.update_layout(
        title_text='<b>' + 'Parent Expense Types for Region APAC' + '</b>',
        # # title='Score Report > 95',
        title_x=0.5,
        showlegend=False,
        barmode='stack',
        )

    import os
    if not os.path.exists("C:\AIVER\Dash\TestResultsForVisual\Test_08"):
        os.mkdir("C:\AIVER\Dash\TestResultsForVisual\Test_08")

    plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_3_APAC.html', auto_open=False)
    # fig.show()
    '''



    filename=f'{html_dir}\\Test_06_3_APAC.html'
    headers=a['Parent_Expense_Type']
    data=a['sum']
    html = creategraph(filename,headers,data)        
    with open(filename,"w") as html_writer:
        html_writer.write(html)
    print('\n\n\nGraph generated and saved in file location, plot show disabled')
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)


#############EMEA_2
try:
    
    df1 = pd.read_csv(f'{csv_folder}\\OR_6_2_1.csv')

    df3 = df1[(df1['GEO'] == 'EMEA')]


    # for region  EMEA
    pv1 = pd.pivot_table(df3, columns=['F_Qtr', 'F_Year'], index=["Parent_Expense_Type"], values=['Sum(Approved_Amount)'],
                        aggfunc=sum, fill_value=0)
    r11 = pv1.droplevel(0, axis=1)
    r11.columns = [str(col[1]) + '/Q' + str(col[0]) for col in r11.columns.values]
    # print(r11)
    a1 = r11.reset_index()

    a1.set_index("Parent_Expense_Type", inplace = True)
    #print(a1)

    legend=[]
    for col in a1.columns:
        d=a1[col].to_dict()
        e={k: d[k] for k in sorted(d, key=d.get, reverse=True)}
        legend.append(list(e.keys())[:5])
    # print(leg)
    import itertools
    leg=list(dict.fromkeys(itertools.chain.from_iterable(legend)))
    #print(leg)

    # below sort independently each column values
    for col in a1.columns:
        if col not in ['Parent_Expense_Type']:
            a1[col] = sorted(a1[col], reverse=True)

    x1 = [col for col in a1.columns if col not in ['Parent_Expense_Type']]
    # print(a1['Parent_Expense_Type'][:5])

    graph_values1 = a1#.drop(['Parent_Expense_Type'], axis=1)

    from plotly import graph_objects as go

    data = {
        "model_E1": list(graph_values1[0:1].values.flatten()),
        "model_E2": list(graph_values1[1:2].values.flatten()),
        "model_E3": list(graph_values1[2:3].values.flatten()),
        "model_E4": list(graph_values1[3:4].values.flatten()),
        "model_E5": list(graph_values1[4:5].values.flatten()),
        "labels": x1
    }
    '''
    fig = go.Figure(
        data=[

            go.Bar(
                name=leg[0],
                x=data["labels"],
                y=data["model_E1"],
                offsetgroup=1,
                # marker=dict(color=leg),
            ),
            go.Bar(
                name=leg[1],
                x=data["labels"],
                y=data["model_E2"],
                offsetgroup=1,
                base=data["model_E1"],
                # marker=dict(color=leg),
            ),
            go.Bar(
                name=leg[2],
                x=data["labels"],
                y=data["model_E3"],
                offsetgroup=1,
                base=[val1 + val2 for val1, val2 in zip(data["model_E1"], data["model_E2"])],
            ),
            go.Bar(
                name=leg[3],
                x=data["labels"],
                y=data["model_E4"],
                offsetgroup=1,
                base=[val1 + val2 + val3 for val1, val2, val3 in zip(data["model_E1"], data["model_E2"], data["model_E3"])],
            ),
            go.Bar(
                name=leg[4],
                x=data["labels"],
                y=data["model_E5"],
                offsetgroup=1,
                base=[val1 + val2 + val3 + val4 for val1, val2, val3, val4 in
                    zip(data["model_E1"], data["model_E2"], data["model_E3"], data["model_E4"])],
            ),


        ],
        layout=go.Layout(
            title_text="<b>"+"Selected Parent Expense Types Trend Analysis for Region EMEA"+"</br>",
            title_x=0.5,
            yaxis_title="<b>"+"Total Amount (USD)"+"</br>",
            xaxis_title="<b>"+"Fiscal Quarters"+"</br>",
            showlegend=True,
            legend_title='Parent Expense Type',
        )
    )

    import plotly
    plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_2_EMEA.html', auto_open=False)
    print("Graph plotted and saved, show disabled")
    #fig.show()

    '''


    filename=f'{html_dir}\\Test_06_2_EMEA.html'
    headers=leg
    #data=[int(data["model_E1"][0]),int(data["model_E2"][0]),int(data["model_E3"][0]),int(data["model_E4"][0]),int(data["model_E5"][0])]
    data=[list(a1.iloc[1])][0]
    html = creategraph(filename,headers,data)        
    with open(filename,"w") as html_writer:
        html_writer.write(html)
    print('\n\n\nGraph generated and saved in file location, plot show disabled')
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)


#####################EMEA_3
try:
    
    df1 = pd.read_csv(f'{csv_folder}\\OR_6_3_2.csv')

    r1=df1[['Parent_Expense_Type','Sum(Approved_Amount_RPT)','F_Qtr']].groupby(['F_Qtr','Parent_Expense_Type']).agg(['sum'])
    # print(r1)
    a=r1.droplevel(0, axis=1)
    a=a.reset_index()
    '''
    print(a)
    FiscalQtr=[]
    for i in a['F_Qtr']:
        i='Q'+str(i)
        FiscalQtr.append(i)


    # Region EMEA

    fig=go.Figure(go.Bar(
        x=a['Parent_Expense_Type'],
        y=a['sum'],
        marker=dict(color=a['F_Qtr']),
        text=FiscalQtr,
        textposition='inside',
        #  texttemplate='Q',),
    ))


    fig.update_yaxes(title_text="Total Amount (USD)")

    # Change the bar mode
    fig.update_layout(
        title_text='<b>' + 'Parent Expense Types for Region EMEA' + '</b>',
        # # title='Score Report > 95',
        title_x=0.5,
        showlegend=False,
        barmode='stack',
        )

    import os
    if not os.path.exists("C:\AIVER\Dash\TestResultsForVisual\Test_08"):
        os.mkdir("C:\AIVER\Dash\TestResultsForVisual\Test_08")

    plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_3_EMEA.html', auto_open=False)
    # fig.show()
    print('\n\n\nGraph generated and saved in file location, plot show disabled')
    '''


    filename=f'{html_dir}\\Test_06_3_EMEA.html'
    headers=a['Parent_Expense_Type']
    data=a['sum']
    html = creategraph(filename,headers,data)        
    with open(filename,"w") as html_writer:
        html_writer.write(html)
    print('\n\n\nGraph generated and saved in file location, plot show disabled')
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

################NAMERICA_2
try:
    df1 = pd.read_csv(f'{csv_folder}\\OR_6_2_1.csv')
    df3 = df1[(df1['GEO'] == 'NAMERICA')]


    # for region  NAMERICA
    pv1 = pd.pivot_table(df3, columns=['F_Qtr', 'F_Year'], index=["Parent_Expense_Type"], values=['Sum(Approved_Amount)'],
                        aggfunc=sum, fill_value=0)
    r11 = pv1.droplevel(0, axis=1)
    r11.columns = [str(col[1]) + '/Q' + str(col[0]) for col in r11.columns.values]
    # print(r11)
    a1 = r11.reset_index()

    a1.set_index("Parent_Expense_Type", inplace = True)
    # print(a1)

    legend=[]
    for col in a1.columns:
        d=a1[col].to_dict()
        e={k: d[k] for k in sorted(d, key=d.get, reverse=True)}
        legend.append(list(e.keys())[:5])
    # print(leg)
    import itertools
    leg=list(dict.fromkeys(itertools.chain.from_iterable(legend)))
    #print(leg)

    # below sort independently each column values
    for col in a1.columns:
        if col not in ['Parent_Expense_Type']:
            a1[col] = sorted(a1[col], reverse=True)

    x1 = [col for col in a1.columns if col not in ['Parent_Expense_Type']]

    graph_values1 = a1#.drop(['Parent_Expense_Type'], axis=1)


    from plotly import graph_objects as go

    data = {
        "model_E1": list(graph_values1[0:1].values.flatten()),
        "model_E2": list(graph_values1[1:2].values.flatten()),
        "model_E3": list(graph_values1[2:3].values.flatten()),
        "model_E4": list(graph_values1[3:4].values.flatten()),
        "model_E5": list(graph_values1[4:5].values.flatten()),
        "labels": x1
    }
    '''
    fig = go.Figure(
    data=[

            go.Bar(
                name=leg[0],
                x=data["labels"],
                y=data["model_E1"],
                offsetgroup=1,
                # marker=dict(color=leg),
            ),
            go.Bar(
                name=leg[1],
                x=data["labels"],
                y=data["model_E2"],
                offsetgroup=1,
                base=data["model_E1"],
                # marker=dict(color=leg),
            ),
            go.Bar(
                name=leg[2],
                x=data["labels"],
                y=data["model_E3"],
                offsetgroup=1,
                base=[val1 + val2 for val1, val2 in zip(data["model_E1"], data["model_E2"])],
            ),
            go.Bar(
                name=leg[3],
                x=data["labels"],
                y=data["model_E4"],
                offsetgroup=1,
                base=[val1 + val2 + val3 for val1, val2, val3 in zip(data["model_E1"], data["model_E2"], data["model_E3"])],
            ),
            go.Bar(
                name=leg[4],
                x=data["labels"],
                y=data["model_E5"],
                offsetgroup=1,
                base=[val1 + val2 + val3 + val4 for val1, val2, val3, val4 in
                    zip(data["model_E1"], data["model_E2"], data["model_E3"], data["model_E4"])],
            ),


        ],
        layout=go.Layout(
            title_text="<b>"+"Selected Parent Expense Types Trend Analysis for Region NAMERICA"+"</br>",
            title_x=0.5,
            yaxis_title="<b>"+"Total Amount (USD)"+"</br>",
            xaxis_title="<b>"+"Fiscal Quarters"+"</br>",
            showlegend=True,
            legend_title='Parent Expense Type'
        )
    )



    import plotly
    plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_2_NAmerica.html', auto_open=False)
    print("Graph plotted and saved, show disabled")
    #fig.show()



    '''
    filename=f'{html_dir}\\Test_06_2_NAmerica.html'
    headers=leg
    #data=[int(data["model_E1"][0]),int(data["model_E2"][0]),int(data["model_E3"][0]),int(data["model_E4"][0]),int(data["model_E5"][0])]
    data=[list(a1.iloc[1])][0]
    html = creategraph(filename,headers,data)        
    with open(filename,"w") as html_writer:
        html_writer.write(html)
    print('\n\n\nGraph generated and saved in file location, plot show disabled')

except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

#######################NAMERICA3

try:
    r1=df1[['Parent_Expense_Type','Sum(Approved_Amount_RPT)','F_Qtr']].groupby(['F_Qtr','Parent_Expense_Type']).agg(['sum'])
    # print(r1)
    a=r1.droplevel(0, axis=1)
    a=a.reset_index()
    # print(a)

    '''
    FiscalQtr=[]
    for i in a['F_Qtr']:
        i='Q'+str(i)
        FiscalQtr.append(i)



    # Region N America
    fig=go.Figure(go.Bar(
        x=a['Parent_Expense_Type'],
        y=a['sum'],
        marker=dict(color=a['F_Qtr']),
        text=FiscalQtr,
        textposition='inside',
        #  texttemplate='Q',),
    ))


    fig.update_yaxes(title_text="Total Amount (USD)")

    # Change the bar mode
    fig.update_layout(
        title_text='<b>' + 'Parent Expense Types for Region N AMERICA' + '</b>',
        # # title='Score Report > 95',
        title_x=0.5,
        showlegend=False,
        barmode='stack',
        )

    import os
    if not os.path.exists("C:\AIVER\Dash\TestResultsForVisual\Test_08"):
        os.mkdir("C:\AIVER\Dash\TestResultsForVisual\Test_08")x
    plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_3_NAmerica.html', auto_open=False)
    # fig.show()
    print('\n\n\nGraph generated and saved in file location, plot show disabled')
    '''

    filename=f'{html_dir}\\Test_06_3_NAmerica.html'
    headers=a['Parent_Expense_Type']
    data=a['sum']
    html = creategraph(filename,headers,data)        
    with open(filename,"w") as html_writer:
        html_writer.write(html)
    print('\n\n\nGraph generated and saved in file location, plot show disabled')
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)

try:
    move()

    sys.exit(0)
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    sys.exit(-1)