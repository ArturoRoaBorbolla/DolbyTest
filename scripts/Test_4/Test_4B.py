import logging
import re
import sqlite3
import seaborn as sns
import sys
import os
import csv
import uuid
import tkinter
import tkinter as tk
import subprocess
import customtkinter
import tkinter.messagebox
import calendar
from CTkMessagebox import CTkMessagebox
import numpy as np
from calendar import monthrange
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd
from xlsxwriter.workbook import Workbook


PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, f'{PRO_DIR}\\common')
sys.path.insert(2, f'{PRO_DIR}\\Scripts_UI')

import get_data
import create_link
import DolbyUI
import var

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

data=var.data["Test_04"]
value=data["TE_004_1" ]
value2=data["TE_004_2" ]

global Start_year
global End_year
global DateTo
global DateFrom

ROOT_DIR = f"{PRO_DIR}\\Test_3\\Output"

connection = sqlite3.connect(var.DatabasePath)
cur = connection.cursor()

today = datetime.date.today()
Start_year = today.strftime("%Y")
End_year = today.strftime("%Y")
values = ["Q1", "Q2", "Q3", "Q4"]
DateFrom = "Q1"
DateTo = "Q4"


import logging
LogsPath = f"{PRO_DIR}\\Test_4\\Logs"  
os.makedirs(LogsPath, exist_ok=True)
testname=os.path.basename(__file__).replace(".py","").replace(".exe","")  #replace .exe and .py
formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(message)s',datefmt='%Y/%m/%d %I:%M:%S')

logpath= f"{LogsPath}\\{testname}.log"  
handler = logging.FileHandler(filename=logpath)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info("Script Started")






def convert_csv_to_xlsx(csvfile,folder):
    name= csvfile[:-4] + '.xlsx'
    name= name.split("\\")[-1]
    workbook = Workbook(f"{folder}\\{name}")
    worksheet = workbook.add_worksheet()
    with open(csvfile, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()




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


def get_report(cursor, view, folder):
    logger.info("Creating Report for " + view)
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




def do_test4(DateFrom,DateTo,value, condition,test_type): 
     
    #TE_4_1_1
    folder = f"{ROOT_DIR}"
    logger.info("Creating main View ")
    cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_1;''') #delete any previus View OR_4_1_1 table
    select = ''' CREATE VIEW OR_4_{0}_1 AS SELECT *, substr(Transaction_Date,1,4) as "Year", substr(Transaction_Date,5,2) as "Month" 
    FROM CR_1 
    WHERE "Transaction_Date" BETWEEN {1} AND {2} AND {3}
    ORDER BY "Transaction_Date" ;'''.format(test_type,DateFrom,DateTo,condition)
    cur.execute(select)
    cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_2;''') #delete any previus View TE_004_1_2 table
    
     
    
    #TE_004_1_2 
    cur.execute(''' CREATE VIEW OR_4_{0}_2 AS 
    SELECT "EMP_ID", "Employee", "Employee_Country_Code", "Year", "Month", sum("Approved_Amount__rpt_") AS "Sum(Approved_Amount__rpt_)" 
    FROM OR_4_{0}_1 
    GROUP BY "EMP_ID", "Employee", "Employee_Country_Code", "Year", "Month" 
    HAVING "Sum(Approved_Amount__rpt_)" > {1} 
    ORDER BY "Sum(Approved_Amount__rpt_)" DESC, "EMP_ID";'''.format(test_type,value))
    logger.info("Getting spend by Month")
    
    
    
    
    
    
    #TE_004_1_3
    cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_3;''') #delete any previus View OR_4_1_3 table
    cur.execute(''' CREATE VIEW OR_4_{0}_3 AS SELECT OR_4_{0}_1.* , OR_4_{0}_2."Sum(Approved_Amount__rpt_)" 
                    FROM OR_4_{0}_1 INNER JOIN OR_4_{0}_2 
                    ON (OR_4_{0}_1."EMP_ID" = OR_4_{0}_2."EMP_ID") AND (OR_4_{0}_1."Employee" = OR_4_{0}_2."Employee") AND (OR_4_{0}_1."Employee_Country_Code" = OR_4_{0}_2."Employee_Country_Code") AND (OR_4_{0}_1."Year" = OR_4_{0}_2."Year") AND (OR_4_{0}_1."Month" = OR_4_{0}_2."Month") 
                    ORDER BY OR_4_{0}_2."Sum(Approved_Amount__rpt_)" DESC, OR_4_{0}_1."EMP_ID", OR_4_{0}_1."Transaction_Date";'''.format(test_type))
    
    logger.info("Getting Cumulative spend by Month")
    
        
    #TE_004_1_4
    cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_4;''') #delete any previus View OR_4_1_4 table
    cur.execute('''CREATE VIEW OR_4_{0}_4 AS SELECT "EMP_ID", "Employee", "Employee_Country_Code", count("Month") AS "Frequency", round(sum("Sum(Approved_Amount__rpt_)"),2) AS "Cumulative(Approved_Amount_RPT)" 
    FROM OR_4_{0}_3
    GROUP BY "EMP_ID", "Employee"  , "Employee_Country_Code"
    HAVING "Frequency(Month)" >= {1} 
    ORDER BY "Cumulative(Approved_Amount_RPT)", "Frequency(Month)", "EMP_ID" DESC; '''.format(test_type,3))
    ###, "Employee_Country_Code"

    

    #TE_004_1_5
    cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_5;''') #delete any previus View OR_4_1_5 table
    cur.execute('''CREATE VIEW OR_4_{0}_5 AS SELECT OR_4_{0}_3.*, OR_4_{0}_4."Cumulative(Approved_Amount_RPT)", OR_4_{0}_4."Frequency" 
    FROM OR_4_{0}_3 
    INNER JOIN OR_4_{0}_4 ON (OR_4_{0}_3."EMP_ID" = OR_4_{0}_4."EMP_ID")
    ORDER BY "Cumulative(Approved_Amount_RPT)" DESC, "Frequency" DESC, "EMP_ID"; '''.format(test_type))
    
    
    
    #cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_6;''') #delete any previus View OR_4_1_5 table
    #cur.execute('''CREATE VIEW OR_4_{0}_6 AS SELECT "EMP_ID","Employee",Year,"Month",count("Entry_Key") AS "Times" FROM OR_4_{0}_5 GROUP BY  "Year","Month",    "Employee" '''.format(test_type,value))
    
    #cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_7;''') #delete any previus View OR_4_1_5 table
    #cur.execute('''CREATE VIEW OR_4_{0}_7 AS SELECT "EMP_ID","Employee",Year,"Month",count("Times at month over {1}") AS "Time at month over {1}" FROM OR_4_{0}_6 GROUP BY   "Year","Month",    "Employee" '''.format(test_type,value))
    
    #cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_8;''') #delete any previus View OR_4_1_5 table
    #cur.execute('''CREATE VIEW OR_4_{0}_8 AS SELECT "EMP_ID","Employee",count("Time at month over {1}") AS "Months over {1}" ,
    #    CASE WHEN count("Times at month over {1}") > 2
    #    THEN "Yes" ELSE "No" END AS "Flagged"
    #    FROM OR_4_{0}_7 group by  "Employee" ORDER By "Months over {1}" DESC'''.format(test_type,value))
        
     
          
     
        
    logger.info("Creating Result View ")
    cur.execute(f'''DROP VIEW IF EXISTS OR_4_{test_type}_9;''') #delete any previus View OR_4_1_5 table
    cur.execute('''CREATE VIEW OR_4_{0}_9 AS SELECT "EMP_ID","Employee","Months over {1}" FROM OR_4_{0}_8 WHERE "Flagged" = "Yes"'''.format(test_type,value))
    
    
    logger.info("Creating Reports ")
    get_report(cur,f"OR_4_{test_type}_1",folder)
    get_report(cur,f"OR_4_{test_type}_2",folder)
    get_report(cur,f"OR_4_{test_type}_3",folder)
    get_report(cur,f"OR_4_{test_type}_4",folder)
    get_report(cur,f"OR_4_{test_type}_5",folder)
    get_report(cur,f"OR_4_{test_type}_6",folder)
    get_report(cur,f"OR_4_{test_type}_7",folder)
    get_report(cur,f"OR_4_{test_type}_8",folder)
    get_report(cur,f"OR_4_{test_type}_9",folder)

    '''
    #TE_004_2_1
    cur.execute('DROP VIEW IF EXISTS OR_4_2_1;') #delete any previus View OR_4_2_1 table
    #select =  CREATE VIEW OR_4_2_1 AS SELECT * , substr("Transaction_Date",1,4) as "Year", substr("Transaction_Date",5,2) as "Month"
    #FROM CR_1 
    #WHERE "Transaction_Date" BETWEEN {0} AND {1} AND ({2})
    #ORDER BY "Transaction_Date" ; .format(DateFrom,DateTo,condition2) 
    #print(select)
    #cur.execute(select)

    #TE_004_2_2
    cur.execute('DROP VIEW IF EXISTS OR_4_2_2;') #delete any previus View TE_004_2_2 table
    cur.execute(CREATE VIEW OR_4_2_2 AS 
    SELECT "EMP_ID", "Employee", "Employee_Country_Code", "Year", "Month", sum("Approved_Amount_RPT") AS "Sum(Approved_Amount_RPT)" 
    FROM OR_4_2_1 
    GROUP BY "EMP_ID", "Employee", "Employee_Country_Code", "Year", "Month" 
    HAVING "Sum(Approved_Amount_RPT)" > {0} 
    ORDER BY "Sum(Approved_Amount_RPT)" DESC, "EMP_ID";.format(value2))

    #TE_004_2_3
    cur.execute('DROP VIEW IF EXISTS OR_4_2_3;') #delete any previus View OR_4_2_3 table
    cur.execute('CREATE VIEW OR_4_2_3 AS SELECT OR_4_2_1.*, OR_4_2_2."Sum(Approved_Amount_RPT)" '
    'FROM OR_4_2_1 '
    'INNER JOIN OR_4_2_2 ON (OR_4_2_1."EMP_ID" = OR_4_2_2."EMP_ID") AND (OR_4_2_1."Employee" = OR_4_2_2."Employee") AND (OR_4_2_1."Employee_Country_Code" = OR_4_2_2."Employee_Country_Code") AND (OR_4_2_1."Year" = OR_4_2_2."Year") AND (OR_4_2_1."Month" = OR_4_2_2."Month") '
    'ORDER BY OR_4_2_2."Sum(Approved_Amount_RPT)" DESC, OR_4_2_1."EMP_ID", OR_4_2_1."Transaction_Date";')

    #TE_004_2_4
    cur.execute('DROP VIEW IF EXISTS OR_4_2_4;') #delete any previus View OR_4_2_4 table
    cur.execute('CREATE VIEW OR_4_2_4 AS SELECT "EMP_ID", "Employee", "Employee_Country_Code", count(Month) AS "Frequency(Month)", round(sum("Sum(Approved_Amount_RPT)"),2) AS "Cumulative(Approved_Amount_RPT)" '
    'FROM OR_4_2_3 '
    'GROUP BY "EMP_ID", "Employee", "Employee_Country_Code" '
    'HAVING "Frequency(Month)" >= {0} '
    'ORDER BY "Cumulative(Approved_Amount_RPT)" DESC, "Frequency(Month)" DESC, "EMP_ID"; '.format(value2))

    #TE_004_2_5
    cur.execute('DROP VIEW IF EXISTS OR_4_2_5;') #delete any previus View OR_4_2_5 table
    cur.execute('CREATE VIEW OR_4_2_5 AS SELECT OR_4_2_3.*, OR_4_2_4."Cumulative(Approved_Amount_RPT)", OR_4_2_4."Frequency(Month)" '
    'FROM OR_4_2_3 '
    'INNER JOIN OR_4_2_4 ON (OR_4_2_3."EMP_ID" = OR_4_2_4."EMP_ID")'
    'ORDER BY "Cumulative(Approved_Amount_RPT)" DESC, "Frequency(Month)" DESC, "EMP_ID"; ')
    '''
    #get_report(cur,"OR_4_2_1",folder)
    #get_report(cur,"OR_4_2_2",folder)
    #get_report(cur,"OR_4_2_3",folder)
    #get_report(cur,"OR_4_2_4",folder)
    #get_report(cur,"OR_4_2_5",folder)
    
    
def change_names(value,value2):
    logger.info("Changing names ")
    folder = f"{ROOT_DIR}"  
    source_folder=f"{folder}\\Source"
    os.makedirs(source_folder, exist_ok=True)
    for i in range(2):
        for j in range(8):
            try:
                os.remove(f"{source_folder}\\OR_4_{i+1}_{j+1}.xlsx")
            except:
                pass
            os.rename(f"{folder}\\OR_4_{i+1}_{j+1}.xlsx",f"{source_folder}\\OR_4_{i+1}_{j+1}.xlsx")
    first=f"Test_4_1_Mobile_Expense_over_{value}_for_3_or_more_months.xlsx"
    second=f"Test_4_2_MiFi_Expense_over_{value2}_for_3_or_more_months.xlsx"
    try:
        os.remove(f"{folder}\\{first}")
        os.remove(f"{folder}\\{second}")
    except:
        pass
    os.rename(f"{folder}\\OR_4_1_9.xlsx",f"{folder}\\{first}")
    os.rename(f"{folder}\\OR_4_2_9.xlsx",f"{folder}\\{second}")
    
    for i in range(2):
        for j in range(3,7):
            try:
                os.remove(f"{source_folder}\\OR_4_{i+1}_{j}.xlsx")
            except:
                pass
    
    for i in range(2):
        for j in range(7,9):
            first=f"{source_folder}\\OR_4_{i+1}_{j}.xlsx"
            second=f"{source_folder}\\OR_4_{i+1}_{j-4}.xlsx"
            try:
                os.remove(f"{source_folder}\\{second}")
            except:
                pass
            os.rename(first,second)
            
            
    old_names=["OR_4_1_1","OR_4_1_2","OR_4_1_3","OR_4_1_4","OR_4_2_1","OR_4_2_2","OR_4_2_3","OR_4_2_4"]   
    new_names=["Mobile_Souce_Data_CR1","Mobile_sum_total_amount_per_person_month_CR1",	"Mobile_per_month_person_over_threshold_CR1",	"Mobile_per_month_person_over_threshold_3_month_flag_CR1","MiFi_Souce_Data_CR1","MiFi_sum_total_amount_per_person_month_CR1","MiFi_per_month_person_over_threshold_CR1","MiFi_per_month_person_over_threshold_3_month_flag_CR1"]
    
    
    for i in range(len(old_names)):
        from_old_file = f'{source_folder}\\{old_names[i]}.xlsx'
        to_new_file = f'{source_folder}\\{old_names[i]}_{new_names[i]}.xlsx'
        try:
            os.remove(to_new_file)
        except:
            pass
        os.rename(from_old_file, to_new_file)

    

DateFrom,DateTo,Start_year,End_year = DolbyUI.Get_Period("Q1","Q4",f"{Start_year}")
del sys.modules["DolbyUI"] 
del DolbyUI

index1 = values.index(DateFrom)
index2 = values.index(DateTo)
from_date = get_date_from_quarter(1, index1,Start_year)
to_date = get_date_from_quarter(2, index2,End_year)
print(from_date, to_date)

condition= """("Expense_Type" = "Mobile/Cellular Phone") AND ("Approval_Status" = "Approved") AND ("Employee_Country_Code" = "US")"""
condition2= """("Expense_Type" = "Wifi/Internet/Telephone") AND ("Approval_Status" = "Approved") AND ("Employee_Country_Code" = "US")"""
do_test4(from_date,to_date,value,condition,1)
do_test4(from_date,to_date,value2,condition2,2)
change_names(value,value2)

logger.info("Finished")