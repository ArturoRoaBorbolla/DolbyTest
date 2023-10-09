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

data=var.data["Test_03"]
value=data["TE_003" ]

global Start_year
global End_year
global DateTo
global DateFrom

ROOT_DIR = f"{PRO_DIR}\\Test_3\\Output"

connection = sqlite3.connect(var.DatabasePath)
cursor = connection.cursor()

today = datetime.date.today()
Start_year = today.strftime("%Y")
End_year = today.strftime("%Y")
values = ["Q1", "Q2", "Q3", "Q4"]
DateFrom = "Q1"
DateTo = "Q4"



import logging
LogsPath = f"{PRO_DIR}\\Test_3\\Logs"  
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
    logger.info("CReating Report for " + view) 
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


def do_the_graphics(meal_type, from_date, to_date, index1, index2, condition, value, folder):
    global Start_year
    global End_year
    global DateFrom
    global DateTo
    logger.info("Creating Graphics for " + str(meal_type))
    graphic_folder = f"{folder}\\Visualization"
    os.makedirs(graphic_folder, exist_ok=True)
    title = ""
    if meal_type == 1:
        title = "Employee Meals and Entertainment"
    if meal_type == 2:
        title = "Travel Meals"
    if meal_type == 3:
        title = "Third Party Meals & Entertainment"

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_1_2;')
    connection.commit()

    #dfrom = get_date_from_quarter(1, index1,Start_year)
    #dto = get_date_from_quarter(2, index2,End_year)
    if len(sys.argv) < 3:
        #index1 = values.index(DateFrom)
        #index2 = values.index(DateTo)
        from_date = get_date_from_quarter(1, index1,Start_year)
        to_date = get_date_from_quarter(2, index2,End_year)
    else:
        from_date=sys.argv[1]
        to_date=sys.argv[2]

    dfrom=from_date
    dto=to_date
    
    select = f""" Select  "Employee_Org_Unit_4___Code", CASE WHEN DptMapping."Bussiness__Group" = 'nan' THEN 'Others' 
                    ELSE DptMapping."Bussiness__Group"  END as "Bussiness_Group",  
                    SUM(CAST( "Approved_Amount__Reporting_Currency_" as float)) AS "SUM_Approved"  From CR_2 
                    JOIN DptMapping ON CR_2."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key" 
                    where "Transaction_Date" BETWEEN '{dfrom}' AND '{dto}' AND ({condition})  
                    GROUP BY "Bussiness_Group"   ORDER BY "SUM_Approved"  DESC """  # Having  "SUM_Approved" > {value}

    cursor.execute(select)
    Query = f""" CREATE VIEW Test_{meal_type}_1_2 as {select} """
    data = cursor.fetchall()
    cursor.execute(Query)

    query = "drop table if exists bck"
    cursor.execute(query)
    select = f'CReate table  bck  as  SELECT "Bussiness_Group","SUM_Approved" from  Test_{meal_type}_1_2'
    cursor.execute(select)

    select = f'select * from bck'
    cursor.execute(select)
    data = cursor.fetchall()

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_1_2;')
    connection.commit()
    Query = f"""CREATE VIEW Test_{meal_type}_1_2 as {select} """
    cursor.execute(Query)

    # Query =f''' Update Test_{meal_type}_1_X set "Bussiness__Group" = "Others"   where "Bussiness__Group" = "nan" '''
    # cursor.execute(Query)
    #print(f"Creating Test_{meal_type}_1_2")
    get_report(cursor, f"Test_{meal_type}_1_2", folder)
    df = pd.read_excel(f"{folder}\\Test_{meal_type}_1_2.xlsx")
    for column in df:
        try:
            df[column] = df[column].apply(np.floor)
            df[column] = df[column].apply(format_as_currency)
        except:
            pass
    df.to_excel(f"{folder}\\Test_{meal_type}_1_2.xlsx")

    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    #print(data)
    dpt = []
    vals = []
    [(dpt.append(x[0].replace("nan", 'Others')), vals.append(x[1])) for x in data]
    ax.bar(dpt, vals)
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    # ax.set_title("Employee Internal Meals Spend By Business Group - Q{} {}".format(i + 1, year))
    ax.set_title("{} By Business Group".format(title))
    ax.set_xlabel("Business Group")
    ax.set_ylabel("Total Spend")
    ax.yaxis.set_major_formatter("${x:,.0f}")
    # Add bar labels on top of each bar
    for container in ax.containers:
        for bar in container:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 5, f"${yval:,.0f}", ha='center', va='bottom',
                    color='black')
    try:
        os.remove(f"Test_{meal_type}_1_2.png")
    except:
        pass
    #print(f"Saving Test_{meal_type}_1_2.png")
    # fig.savefig(f"{folder}\\Test_{meal_type}_1_2.png")
    #print("\n\n\n\n\n", folder, "\n\n\n\n\n\n\n\n")
    fig.savefig(f"{graphic_folder}\\Test_{meal_type}_1_2_{title} By Business Group.png")

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_1;')
    connection.commit()

    select = f""" Select  "Employee_Org_Unit_4___Code","Employee","Report_ID", DptMapping."Bussiness__Group" as "Bussiness_Group" ,SUM( CAST("Approved_Amount__Reporting_Currency_" as float)) AS "Approved_Amount__Reporting_Currency_"  FRom CR_2 JOIN DptMapping ON CR_2."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key" where "Transaction_Date" BETWEEN '{from_date}' AND '{to_date}' AND ({condition})   GROUP BY "Entry_key", "Bussiness_Group" HAVING "Approved_Amount__Reporting_Currency_"  > {value}  ORDER BY "Approved_Amount__Reporting_Currency_" DESC"""
    Query = f""" CREATE VIEW Test_{meal_type}_1 as {select} """
    cursor.execute(Query)
    # get_report(cursor, f'Test_{meal_type}_1', folder)

    whole_data = []
    # To get custom colors for legend
    select = f'''
                SELECT DISTINCT 
                    CASE 
                        WHEN "Bussiness__Group" = 'nan' THEN 'Others' 
                        ELSE "Bussiness__Group"
                    END as "Bussiness_Group" 
                FROM DptMapping;'''
    cursor.execute(select)
    business_grp = cursor.fetchall()
    business_grp_df = pd.DataFrame(business_grp, columns=["Buss_grp"])
    unique_groups = business_grp_df["Buss_grp"].unique()
    color_palette = sns.color_palette("tab20", len(unique_groups))
    # color_palette_filter = color_palette[4: len(unique_groups)]
    colors = {group: color_palette[i] for i, group in enumerate(unique_groups)}
    # #print('colo::', colors)

    for i in range(index1, index2 + 1):
        cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_1_2_Q{i + 1};')
        connection.commit()
        dfrom = get_date_from_quarter(1, i,Start_year)
        dto = get_date_from_quarter(2, i,End_year)
        #print(dfrom, dto)
        select = f""" Select  "Employee_Org_Unit_4___Code", CASE WHEN DptMapping."Bussiness__Group" = 'nan' THEN 'Others' 
                        ELSE DptMapping."Bussiness__Group"  END as "Bussiness_Group" ,  
                        SUM(CAST( "Approved_Amount__Reporting_Currency_" as float)) AS "SUM_Approved"  From CR_2 
                        JOIN DptMapping ON CR_2."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key" 
                        where "Transaction_Date" BETWEEN '{dfrom}' AND '{dto}' AND ({condition})  
                        GROUP BY "Bussiness_Group"  Having  "SUM_Approved" > {value} ORDER BY "SUM_Approved" DESC """

        Query = f""" CREATE VIEW Test_{meal_type}_1_2_Q{i + 1} as {select} """
        cursor.execute(select)
        data = cursor.fetchall()
        cursor.execute(Query)
        Query1 = f''' Update "Bussiness_Group" = "Others"  FROM Test_{meal_type}Test_{meal_type}_1_2_Q{i + 1} where "Bussiness_Group" = "nan" '''
        query = "drop table if exists bck"
        cursor.execute(query)
        select = f'Create table  bck  as  SELECT "Bussiness_Group","SUM_Approved" from  Test_{meal_type}_1_2_Q{i + 1}'
        cursor.execute(select)

        select = f'select * from bck'
        cursor.execute(select)
        data = cursor.fetchall()

        cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_1_2_Q{i + 1};')
        connection.commit()
        Query = f"""CREATE VIEW Test_{meal_type}_1_2_Q{i + 1} as {select} """
        cursor.execute(Query)
        # #print(f"Creating Test_{meal_type}_1_2_Q{i + 1}")
        # get_report(cursor, f"Test_{meal_type}_1_2_Q{i + 1}", folder)
        fig, ax = plt.subplots()
        fig.set_size_inches(18.5, 10.5)
        #print(data)
        dpt = []
        vals = []
        [(dpt.append(x[0]), vals.append(x[1])) for x in data]
        for x in data:
            whole_data.append(['Q{}_{}'.format(i + 1, Start_year), x[0].replace("nan", 'Others'), x[1]])
        #print(whole_data)
        ax.bar(dpt, vals)
        ax.yaxis.get_major_formatter().set_scientific(False)
        ax.yaxis.get_major_formatter().set_useOffset(False)
        # ax.set_title("Employee Internal Meals Spend By Business Group - Q{} {}".format(i + 1, year))
        ax.set_title("{} Spend By Business Group - Q{} {}".format(title, i + 1, Start_year))
        ax.set_xlabel("Business Group")
        ax.set_ylabel("Total Spend")
        ax.yaxis.set_major_formatter("${x:,.0f}")
        # Add bar labels on top of each bar
        for container in ax.containers:
            for bar in container:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, yval + 5, f"${yval:,.0f}", ha='center', va='bottom',
                        color='black')
        try:
            os.remove(f"Test_{meal_type}_1_2_Q{i + 1}.png")
        except:
            pass
        # #print(f"Saving Test_{meal_type}_1_2_Q{i + 1}.png")
        # fig.savefig(f"{folder}\\Test_{meal_type}_1_2_Q{i + 1}.png")
        cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_1_2_Q{i + 1};')

    try:
        os.remove(f"Test_{meal_type}_Dpt_All_Quarters.png")
    except:
        pass

    #print(f"Creating Test_{meal_type}_1_1.png")
    # create combined df for both quarters
    fig_whole, ax_b = plt.subplots()
    fig_whole.set_size_inches(18.5, 10.5)
    ax_b.yaxis.get_major_formatter().set_scientific(False)
    ax_b.yaxis.get_major_formatter().set_useOffset(False)
    # ax_b.set_title('Employee Internal Meals Expense')
    ax_b.set_title(f'{title}')

    columns = ["Qtr", "Bus_grp", "Total"]
    df = pd.DataFrame(whole_data, columns=columns)
    # Rearrange row as column
    pivot_df = df.pivot(index="Bus_grp", columns="Qtr", values="Total")
    pivot_df.reset_index(inplace=True)
    #print("\nDataFrame after pivoting:")
    #print(pivot_df)

    # Reshape the DataFrame
    df_final = pivot_df.melt(id_vars="Bus_grp", var_name="Quarter", value_name="Value")

    # To get custom colors for legend
    # unique_groups = df_final["Bus_grp"].unique()
    # color_palette = sns.color_palette("bright", len(unique_groups))
    # color_palette_filter = color_palette[: len(unique_groups)]
    # colors = {group: color_palette_filter[i] for i, group in enumerate(unique_groups)}

    pivot_df2 = df_final.pivot(index="Quarter", columns="Bus_grp", values="Value")
    pivot_df2.plot(kind="bar", stacked=True, ax=ax_b, width=0.4, color=[colors[group] for group in pivot_df2.columns])
    pivot_df2.round(0)
    pivot_df2['Summary'] = pivot_df2.sum(axis=1)
    pivot_df2['Summary'] = pivot_df2['Summary'].round()
    ax_b.set_xlabel("Quarter")
    ax_b.set_ylabel("Total Spend")
    x = pivot_df2['Summary']
    y = []
    count = 0
    for i in x:
        # #print(x.iloc[count])
        y.append(x.iloc[count])  # (x.iloc[count])
        count += 1
    x = y
    for i in range(len(x)):
        #print(f"{str(x[i])}")
        plt.text(i, int(x[i] + 5), f"${x[i]:,.0f}", ha='center')

    ax_b.set_xlabel("Quarter")
    ax_b.set_ylabel("Total Spend")
    ax_b.yaxis.set_major_formatter("${x:,.0f}")
    # ax_b.set_xticklabels(ax_b.get_xticklabels(), rotation=45, ha="right")
    ax_b.set_xticklabels(ax_b.get_xticklabels(), rotation=0)
    lg = ax_b.legend(loc="upper right", title="Business Group")
    lg.get_title().set_fontsize('12')
    fig_whole.savefig(f"{graphic_folder}\\Test_{meal_type}_1_1_{title}.png")
    #print(f"Saving Test_{meal_type}_1_1_1.png")
    #print(pivot_df)
    for column in pivot_df2:
        pivot_df2[column] = pivot_df2[column].apply(np.floor)
        pivot_df2[column] = pivot_df2[column].apply(format_as_currency)
    pivot_df2.to_excel(f"{folder}\\Test_{meal_type}_1_1.xlsx")


def calculate_total_expense(from_date, to_date, condition):
    logger.info("Calculating Total Expense")
    Query = f"""  Select  Count(*) from CR_2 where "Transaction_Date" BETWEEN '{from_date}' AND '{to_date}' AND ({condition}) """
    cursor.execute(Query)
    return int(cursor.fetchone()[0])


def calculate_non_compliance(from_date, to_date, condition, value):
    logger.info("Calculating Non Compliance")
    Query = f"""  Select  Count(*) from CR_2 where "Transaction_Date" BETWEEN '{from_date}' AND '{to_date}' 
                    AND ({condition}) AND  CAST("Approved_Amount__Reporting_Currency_" as float)  > {value} """
    cursor.execute(Query)
    return int(cursor.fetchone()[0])


def create_view_non_compliance_per_attendee(meal_type, from_date, to_date, condition, value, folder):
    select = f""" Select  "Employee_Org_Unit_4___Code","Employee" ,"Report_ID", "Purpose",  "Transaction_Date","Expense_Type",
                "Approved_Amount__rpt_" AS "Total Meal Amount -- Approved Amount (rpt)", DptMapping."Bussiness__Group" as "Bussiness_Group",
                "Entry_Key", "Attendee_Name",
                "Approved_Amount__Reporting_Currency_" AS "Meal Amount per person -- Approved Amount (Reporting Currency)", 
                "1" as "#_of_Attendees"  From CR_2 JOIN DptMapping 
                ON CR_2."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key" where "Transaction_Date" 
                BETWEEN '{from_date}' AND '{to_date}' AND ({condition})  AND 
                CAST("Approved_Amount__Reporting_Currency_" as float) > {value} 
                GROUP BY "ENtry_Key"  Having  count(*)  = 1 
                ORDER BY CAST("Approved_Amount__Reporting_Currency_" as float) DESC  """

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_2_1;')
    Query = f""" CREATE VIEW Test_{meal_type}_2_1 as {select} """
    cursor.execute(Query)
    # get_report(cursor,f'Test_{meal_type}_2_1',folder)


def calculate_per_attn_amt(meal_type):
    Query = f"""  Select  SUM(CAST ("Total Meal Amount -- Approved Amount (rpt)" AS FLOAT)) as per_att_total,
                 SUM("#_of_Attendees") as per_att_count
                from Test_{meal_type}_2_1  """
    cursor.execute(Query)
    return cursor.fetchone()


def create_view_non_compliance_2plus(meal_type, from_date, to_date, condition, value, folder):
    select = f""" Select  "Employee_Org_Unit_4___Code","Employee" ,"Report_ID", 
                "Purpose", "Transaction_Date","Expense_Type" ,"Approved_Amount__rpt_" AS "Total Meal Amount -- Approved Amount (rpt)",
                DptMapping."Bussiness__Group" as "Bussiness_Group" ,"Entry_Key", "Attendee_Name",
                "Approved_Amount__Reporting_Currency_" AS "Meal Amount per person -- Approved Amount (Reporting Currency)",
                count("Entry_Key") as "#_of_Attendees" FRom CR_2 
                JOIN DptMapping ON CR_2."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key" 
                where "Transaction_Date" BETWEEN '{from_date}' AND '{to_date}' AND ({condition})  
                AND CAST("Approved_Amount__Reporting_Currency_" as float) > {value} 
                GROUP BY "Entry_Key"  Having  count(*)  > 1 
                ORDER BY CAST("Approved_Amount__Reporting_Currency_" as float) DESC  """
    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_2_2;')
    Query = f""" CREATE VIEW Test_{meal_type}_2_2 as {select} """
    cursor.execute(Query)
    # get_report(cursor,f'Test_{meal_type}_2_2',folder)


def calculate_2plus_amt(meal_type):
    Query = f"""  Select  SUM(CAST ("Total Meal Amount -- Approved Amount (rpt)" AS FLOAT)) as per_att_total,
                  SUM("#_of_Attendees") as per_att_count
                  from Test_{meal_type}_2_2 """
    cursor.execute(Query)
    return cursor.fetchone()


def create_main_view_data(meal_type, from_date, to_date, condition, value, folder):
    logger.info("Creating Main View")
    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type};')
    connection.commit()
    select = f""" Select  "Employee_Org_Unit_4___Code","Employee","Report_ID","Purpose","Total_Approved_Amount__rpt_",
    "Approved_Amount__Reporting_Currency_", DptMapping."Bussiness__Group"  as "Bussiness_Group" FROM CR_2 JOIN DptMapping 
    ON CR_2."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key" 
    where "Transaction_Date" BETWEEN '{from_date}' AND '{to_date}' AND ({condition}) 
    and CAST("Approved_Amount__Reporting_Currency_" as float) > {value} 
    ORDER BY CAST("Approved_Amount__Reporting_Currency_" as float) DESC """
    Query = f""" CREATE VIEW Test_{meal_type} as {select} """
    cursor.execute(Query)
    # get_report(cursor,f'Test_{meal_type}',folder)


def get_total_amount(view_or_table, from_date, to_date, condition, value):
    logger.info("Getting Total Amount")
    select = f""" Select  SUM( CAST ( "Approved_Amount__Reporting_Currency_"as float ) )as "Total"  
                  FROM {view_or_table}  where "Transaction_Date"  BETWEEN '{from_date}' AND '{to_date}' 
                  AND ({condition})  AND CAST("Approved_Amount__Reporting_Currency_" as float) > {value}  """
    #print(select)
    cursor.execute(select)
    return int(cursor.fetchone()[0])


def get_all_amt(view_or_table, from_date, to_date, condition, value):
    select = f""" Select  SUM( CAST ( "Approved_Amount__Reporting_Currency_"as float ) )as "Total"  
                  FROM {view_or_table} 
                  JOIN DptMapping ON {view_or_table}."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key"
                  where "Transaction_Date"  BETWEEN '{from_date}' AND '{to_date}' 
                  AND ({condition}) """
    #print('get_all_amt', select)
    cursor.execute(select)
    # return round(float(cursor.fetchone()[0]), 2)
    return int(cursor.fetchone()[0])


# def format_as_currency(value):
#     return "${:,.2f}".format(value)

def format_as_currency(value):
    if value is None:
        return None
    if str(value) == "nan":
        return ""
    try:
        formatted_value = "${:,.0f}".format(value)
        return formatted_value
    except ValueError:
        return value




def do_test3(value):
    global Start_year
    global End_year
    global DateFrom
    global DateTo
    meal_type = 3

    if len(sys.argv) < 3:
        index1 = values.index(DateFrom)
        index2 = values.index(DateTo)
        from_date = get_date_from_quarter(1, index1,Start_year)
        to_date = get_date_from_quarter(2, index2,End_year)
    else:
        from_date=sys.argv[1]
        to_date=sys.argv[2]
        index1=1
        index2=1
    #print(from_date, to_date)
    folder = f"{ROOT_DIR}"
    os.makedirs(folder, exist_ok=True)
    condition = ''' "Expense_Type" = "Meals/Entertainment (Third Party)" OR "Expense_Type" = "Meals/Entertainment (Third Party) EMEA" '''
    ###Test_1
    create_main_view_data(meal_type, from_date, to_date, condition, value, folder)

    ###TEST_1_1
    do_the_graphics(meal_type, from_date, to_date, index1, index2, condition, value, folder)

    #####TEST_1_2
    create_view_non_compliance_per_attendee(meal_type, from_date, to_date, condition, value, folder)
    create_view_non_compliance_2plus(meal_type, from_date, to_date, condition, value, folder)

    ######Test_1_3
    Total = calculate_total_expense(from_date, to_date, condition)
    #print(f"Total = {Total}")
    OverValue = calculate_non_compliance(from_date, to_date, condition, value)
    #print(f"Overvalue = {OverValue}")
    Percentage = (OverValue / Total) * 100

    total_meal_amt = get_all_amt("CR_2", from_date, to_date, condition, 0)
    #print('total_meal_amt', total_meal_amt)

    attn_per_values = calculate_per_attn_amt(meal_type)
    attn_per_amt = round(attn_per_values[0], 0)
    attn_per_count = attn_per_values[1]
    #print('attn_per_amt', attn_per_amt, attn_per_count)
    Percentage1 = (attn_per_amt / total_meal_amt) * 100
    Percentage1count = (attn_per_count / Total) * 100

    attn_2plus_values = calculate_2plus_amt(meal_type)
    attn_2plus_amt = round(attn_2plus_values[0], 0)
    attn_2plus_count = attn_2plus_values[1]
    #print('attn_2plus_amt', attn_2plus_amt, attn_2plus_count)
    Percentage2plus = (attn_2plus_amt / total_meal_amt) * 100
    Percentage2pluscount = (attn_2plus_count / Total) * 100

    total_attn = attn_per_amt + attn_2plus_amt
    Percentagetotal = (total_attn / total_meal_amt) * 100
    #print('total attn', total_attn, Percentagetotal)

    # call 2 function
    try:
        cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_3;')
    except:
        cursor.execute(f'DROP TABLE IF EXISTS Test_{meal_type}_3;')
    # Query = f""" CREATE VIEW Test_{meal_type}_3 as Select {year} AS "Input Year", '{DateFrom}' AS "Input Quarter From",
    #                 '{DateTo}' AS "Input Quarter To" ,{Total}  AS "# of Total Meal", {OverValue} AS "# of Meal over {value}"
    #                 , CAST(ROUND({Percentage},2) as VARCHAR) + ' %'  AS "Percentage" """
    # cursor.execute(Query)

    # updated 09-09-2023
    test_1_3 = [
        ['#', '# Number of Total Meal', '# Number of Meal over {}'.format(value),
         '% Percentage', '$ Amount of Total Meal',
         '$ Amount of Total Meal over {}'.format(value),
         '% Percentage Amt'],
        ['Total Attendee', Total, OverValue, '{}{}'.format(round(Percentage, 2), '%'),
         "${:,.0f}".format(total_meal_amt), "${:,.0f}".format(total_attn), '{}{}'.format(round(Percentagetotal, 0), '%')],
        ['1 Attendee', '', attn_per_count, '{}{}'.format(round(Percentage1count, 2), '%'),
         '', "${:,.0f}".format(attn_per_amt), '{}{}'.format(round(Percentage1, 0), '%')],
        ['2 and 2+ Attendee', '', attn_2plus_count, '{}{}'.format(round(Percentage2pluscount, 2), '%'),
         '', "${:,.0f}".format(attn_2plus_amt), '{}{}'.format(round(Percentage2plus, 0), '%')]
    ]
    #print('test_1_3:::\n\n', pd.DataFrame(test_1_3))
    test_1_3_df = pd.DataFrame(test_1_3)
    test_1_3_df.columns = test_1_3_df.iloc[0]
    test_1_3_df = test_1_3_df[1:]

    # test_1_3_df['$ Amount of Total Meal'] = test_1_3_df['$ Amount of Total Meal'].str.replace(',', '', regex=True).astype(float)
    # test_1_3_df['$ Amount of Total Meal over {}'] = test_1_3_df['$ Amount of Total Meal over {}'].str.replace(',', '', regex=True).astype(float)
    test_1_3_df['$ Amount of Total Meal'] = test_1_3_df['$ Amount of Total Meal'].apply(format_as_currency)
    test_1_3_df['$ Amount of Total Meal over {}'.format(value)] = test_1_3_df[
        '$ Amount of Total Meal over {}'.format(value)].apply(format_as_currency)

    table_name = f"Test_{meal_type}_3"
    test_1_3_df.to_sql(table_name, con=connection, if_exists='replace', index=False)
    # query = f"""
    #     CREATE VIEW Test_{meal_type}_3 AS
    #     SELECT * FROM {table_name};
    #     """
    # cursor.execute(query)
    test_1_3_report = [["Input Year From","Input Year To" "Input Quarter From", "Input Quarter To"],
                       [Start_year,End_year, DateFrom, DateTo],
                       ['#', '# Number of Total Meal', '# Number of Meal over {}'.format(value),
                        '% Percentage', '$ Amount of Total Meal',
                        '$ Amount of Total Meal over {}'.format(value),
                        '% Percentage Amt'],
                       ['Total Attendee', Total, OverValue, '{}{}'.format(round(Percentage, 2), '%'),
                        "${:,.0f}".format(total_meal_amt), "${:,.0f}".format(total_attn), '{}{}'.format(round(Percentagetotal, 0), '%')],
                       ['1 Attendee', '', attn_per_count, '{}{}'.format(round(Percentage1count, 2), '%'),
                        '', "${:,.0f}".format(attn_per_amt), '{}{}'.format(round(Percentage1, 0), '%')],
                       ['2 and 2+ Attendee', '', attn_2plus_count, '{}{}'.format(round(Percentage2pluscount, 2), '%'),
                        '', "${:,.0f}".format(attn_2plus_amt), '{}{}'.format(round(Percentage2plus, 0), '%')]
                       ]
    test_1_3_df1 = pd.DataFrame(test_1_3_report)
    test_1_3_df1.columns = test_1_3_df1.iloc[0]
    test_1_3_df1 = test_1_3_df1[1:]
    #print(test_1_3_df1.columns)

    # test_1_3_df1.iloc[:, 3] = test_1_3_df1.iloc[:, 3].apply(format_as_currency)
    # test_1_3_df1.iloc[:, 4] = test_1_3_df1.iloc[:, 4].apply(format_as_currency)

    csv_folder = f"{folder}\\csv"
    xlsx_folder = f"{folder}"
    test_1_3_df1.to_csv(os.path.join(csv_folder, "{}.csv".format(table_name)), index=False)
    test_1_3_df1.to_excel(os.path.join(xlsx_folder, "{}.xlsx".format(table_name)), index=False)

    # get_report(cursor, f'Test_{meal_type}_3', folder)
    # cursor.execute(f 'DROP TABLE IF EXISTS Test_{meal_type}_3;')

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_3_1;')
    Query = f""" CREATE VIEW Test_{meal_type}_3_1 as SELECT CAST(ROW_NUMBER() OVER (ORDER BY Employee) as int) AS "No",
         "Employee","Report_ID","Purpose",
         CAST("Approved_Amount__rpt_" as float) as "Total Meal Amount -- Approved Amount (rpt)",
         CAST("Approved_Amount__Reporting_Currency_" as REAL) as "Meal Amount per person -- Approved Amount (Reporting Currency)",

        CASE WHEN CAST("Approved_Amount__Reporting_Currency_" as float ) > {value} 
         THEN 'yes' ELSE "no"  END as "Meal over {value}", "Employee_Org_Unit_4___Code",

         CASE WHEN DptMapping."Bussiness__Group" = 'nan' 
         THEN 'Others' ELSE DptMapping."Bussiness__Group"  END as "Bussiness_Group", 

        "Transaction_Date",   "Expense_Type", "Entry_key" 
         FROM CR_2 JOIN DptMapping ON CR_2."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key" 
         where "Transaction_Date" BETWEEN '{from_date}' AND '{to_date}' AND ({condition})  """

    cursor.execute(Query)
    get_report(cursor, f'Test_{meal_type}_3_1', folder)

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_3_2;')
    # "Total Meal Amount -- Approved Amount (rpt)",

    # Query = f""" CREATE VIEW Test_{meal_type}_3_2 as SELECT "No", "Employee_Org_Unit_4___Code", "Employee",
    #             "Report_ID","Purpose",
    #             "Meal Amount per person -- Approved Amount (Reporting Currency)" ,
    #             "Bussiness__Group" , "Meal over {value}",
    #             "Entry_Key", COUNT("Entry_Key") AS "#_of_attendees"  FROM  Test_{meal_type}_3_1
    #             GROUP BY  "Entry_key" Having "#_of_attendees" > 0 """
    Query = f""" CREATE VIEW Test_{meal_type}_3_2 as 
                SELECT CAST(ROW_NUMBER() OVER (ORDER BY Employee) as int) AS "No",
                "Employee","Report_ID","Purpose",
         CAST("Approved_Amount__rpt_" as float) as "Total Meal Amount -- Approved Amount (rpt)",
                CAST("Approved_Amount__Reporting_Currency_" as float) as "Meal Amount per person -- Approved Amount (Reporting Currency)",

                CASE
                WHEN DptMapping."Bussiness__Group" = 'nan' THEN 'Others' ELSE DptMapping."Bussiness__Group"
                END  as "Bussiness_Group",

                CASE WHEN CAST("Approved_Amount__Reporting_Currency_" as float ) > {value}
                THEN 'yes' ELSE "no"  END as "Meal over {value}", "Employee_Org_Unit_4___Code",

                "Entry_key" , CAST(COUNT("Entry_Key") as int) AS "#_of_attendees"
                FROM CR_2 JOIN DptMapping ON
                CR_2."Employee_Org_Unit_4___Code" =  DptMapping."Cost_Center___Key" where "Transaction_Date"
                BETWEEN '{from_date}' AND '{to_date}' AND ({condition})
                GROUP BY  "Entry_key" Having "#_of_attendees" > 0"""
    cursor.execute(Query)
    get_report(cursor, f'Test_{meal_type}_3_2', folder)

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_3_2_temp;')
    Query = f""" CREATE VIEW Test_{meal_type}_3_2_temp as SELECT "Employee" ,"Report_ID", "Purpose", 
                "Total Meal Amount -- Approved Amount (rpt)",
                "Meal Amount per person -- Approved Amount (Reporting Currency)",
                "Bussiness_Group","Meal over {value}","#_of_attendees"  
                FROM  Test_{meal_type}_3_2 """
    cursor.execute(Query)
    get_report(cursor, f"Test_{meal_type}_3_2_temp", folder)

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_2_1_temp;')
    Query = f""" CREATE VIEW Test_{meal_type}_2_1_temp as SELECT   "Employee" ,"Report_ID", "Purpose", "Transaction_Date","Expense_Type","Bussiness_Group", 
                    "Total Meal Amount -- Approved Amount (rpt)",
                    "Meal Amount per person -- Approved Amount (Reporting Currency)",
                    "#_of_Attendees"  FROM  Test_{meal_type}_2_1 """

    cursor.execute(Query)
    get_report(cursor, f"Test_{meal_type}_2_1_temp", folder)

    cursor.execute(f'DROP VIEW IF EXISTS Test_{meal_type}_2_2_temp;')
    Query = f""" CREATE VIEW Test_{meal_type}_2_2_temp as SELECT "Employee" ,"Report_ID", "Purpose", "Transaction_Date","Expense_Type","Bussiness_Group", 
                    "Total Meal Amount -- Approved Amount (rpt)",
                    "Meal Amount per person -- Approved Amount (Reporting Currency)","#_of_Attendees"  
                    FROM  Test_{meal_type}_2_2 """
    cursor.execute(Query)
    get_report(cursor, f"Test_{meal_type}_2_2_temp", folder)


def close_connection():
    connection.close()


'''
def change_names():
    folder = f"{ROOT_DIR}\\Test_1"
    old_names=["Test_1_1_1","Test_1_1_2","Test_1_2_1","Test_1_2_2","Test_1_3","Test_1_3_1","Test_1_3_2"]
    new_names= ["Test_1_1_1_Employee_Meals_and_Entertainment_Data_CR2","Test_1_1_2_Employee_Meals_and_Entertainment_By_Business_Group_Data_CR2","Test_1_2_1_EM&E_with_1_attendee_over_threshold_CR2","Test_1_2_2_EM&E_with_2+_attendees_over_threshold_CR2","Test_1_3_EM&E_Summary_CR2","Test_1_3_1_EM&E_CR2_Source_data","Test_1_3_2_EM&E _CR2_Summary_Verification"]
    for i in range(len(old_names)):
        
        from_old_file=f'{folder}\\{old_names[i]}.xlsx'
        to_new_file= f'{folder}\\{new_names[i]}.xlsx'
        os.rename(from_old_file,to_new_file)
        #command = ['move', f"'{from_old_file}'", f"'{to_new_file}'" ]
        ##print(command)
        #p = subprocess.Popen(command)
'''


def change_names_test1():
    folder = f"{ROOT_DIR}\\Test_1"
    source_folder = f"{folder}\\Source"
    os.makedirs(source_folder, exist_ok=True)
    old_names = ["Test_1_1_1", "Test_1_1_2", "Test_1_2_1", "Test_1_2_2", "Test_1_3", "Test_1_3_1", "Test_1_3_2"]
    source = ["Test_1_3_1_EM&E_CR2_Source_data", "Test_1_3_2_EM&E _CR2_Summary_Verification"]
    new_names = ["Test_1_1_1_Employee_Meals_and_Entertainment_Data_CR2",
                 "Test_1_1_2_Employee_Meals_and_Entertainment_By_Business_Group_Data_CR2",
                 "Test_1_2_1_EM&E_with_1_attendee_over_threshold_CR2",
                 "Test_1_2_2_EM&E_with_2+_attendees_over_threshold_CR2", "Test_1_3_EM&E_Summary_CR2",
                 "Test_1_3_1_EM&E_CR2_Source_data", "Test_1_3_2_EM&E _CR2_Summary_Verification"]
    to_folder = ""
    for i in range(len(old_names)):
        if new_names[i] in source:
            to_folder = f"{source_folder}"
        else:
            to_folder = folder
        from_old_file = f'{folder}\\{old_names[i]}.xlsx'
        to_new_file = f'{to_folder}\\{new_names[i]}.xlsx'
        try:
            os.remove(to_new_file)
        except:
            pass
        os.rename(from_old_file, to_new_file)


def change_names_test2():
    folder = f"{ROOT_DIR}\\Test_2"
    source_folder = f"{folder}\\Source"
    os.makedirs(source_folder, exist_ok=True)
    old_names = ["Test_2_2_1", "Test_2_2_2", "Test_2_2"]
    source = ["Test_2_2_1_Travel Meals",
              "Test_2_2_2_Travel Meals per attendee with aggregate total expense per day",
              ]

    new_names = ["Test_2_2_1_Travel Meals",
                 "Test_2_2_2_Travel Meals per attendee with aggregate total expense per day",
                 "Test_2_2_Travel Meals per attendee with aggregate total expense per day over threshold"]
    to_folder = ""
    for i in range(len(old_names)):
        if new_names[i] in source:
            to_folder = f"{source_folder}"
        else:
            to_folder = folder
        from_old_file = f'{folder}\\{old_names[i]}.xlsx'
        to_new_file = f'{to_folder}\\{new_names[i]}.xlsx'
        try:
            os.remove(to_new_file)
        except:
            pass
        os.rename(from_old_file, to_new_file)


def change_names_test3():
    logger.info("Change Names Test 3")
    folder = f"{ROOT_DIR}"
    source_folder = f"{folder}\\Source"
    os.makedirs(source_folder, exist_ok=True)
    Report = f"{folder}\\Report"
    os.makedirs(Report, exist_ok=True)
    old_names = ["Test_3_1_1", "Test_3_1_2", "Test_3_2_1", "Test_3_2_2", "Test_3_3", "Test_3_3_1", "Test_3_3_2"]
    source = ["Test_3_3_1_EM&E_CR2_Source_data", "Test_3_3_2_EM&E _CR2_Summary_Verification"]
    new_names = ["Test_3_1_1_Thrid_Party_Meals_and_Entertainment_Data_CR2",
                 "Test_3_1_2_Thrid_Party_Meals_and_Entertainment_By_Business_Group_Data_CR2",
                 "Test_3_2_1_EM&E_with_1_attendee_over_threshold_CR2",
                 "Test_3_2_2_EM&E_with_2+_attendees_over_threshold_CR2", "Test_3_3_EM&E_Summary_CR2",
                 "Test_3_3_1_EM&E_CR2_Source_data", "Test_3_3_2_EM&E _CR2_Summary_Verification"]
    to_folder = ""
    for i in range(len(old_names)):
        if new_names[i] in source:
            to_folder = f"{source_folder}"
        else:
            to_folder = Report
        from_old_file = f'{folder}\\{old_names[i]}.xlsx'
        to_new_file = f'{to_folder}\\{new_names[i]}.xlsx'
        try:
            os.remove(to_new_file)
        except:
            pass
        os.rename(from_old_file, to_new_file)

def create_dashboard():
    Output=f'{ROOT_DIR}'
    Dasboard=f'{Output}\\Dashboard'
    Reports = f'{Output}\\Report'
    csv_folder = f'{Output}\\csv'
    Visualization = f'{Output}\\Visualization'
    os.makedirs(Dasboard, exist_ok=True)
    shutil.copy(f"{csv_folder}\\Test_3_1_2.csv", f"{Dasboard}")
    shutil.copy(f"{csv_folder}\\Test_3_2_2.csv", f"{Dasboard}")
    shutil.copy(f"{Visualization}\\Test_3_1_1_Third Party Meals & Entertainment.png", f"{Dasboard}")
    shutil.copy(f"{Visualization}\\Test_3_1_2_Third Party Meals & Entertainment By Business Group.png", f"{Dasboard}")
    
def create_download():
    Output=f'{ROOT_DIR}'
    Reports = f'{Output}\\Report'
    Visualization = f'{Output}\\Visualization'
    Source=f'{Output}\\Source'
    download = f'{Output}\\Download'
    os.makedirs(download, exist_ok=True)
    downloads=[Reports,Visualization,Source]
    for i in downloads:
        try:
            shutil.rmtree(f"{download}\\{i}")
        except:
            pass
        new_folder = i.split("\\")[-1] 
        os.makedirs(f"{download}\\{new_folder}", exist_ok=True)
        shutil.copytree(i,f"{download}\\{new_folder}", symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)

def create_zip_archive():
    shutil.make_archive(f"{ROOT_DIR}\\Test_3", 'zip', f'{ROOT_DIR}\\Download')
    
    
#def move():
#    shutil.move(f"{ROOT_DIR}\\Test_3_1_1.xlsx", f"{ROOT_DIR}\\Report\\Test_3_1_1.xlsx")
#    shutil.move(f"{ROOT_DIR}\\Test_3_1_2.xlsx", f"{ROOT_DIR}\\Report\\Test_3_1_2.xlsx")
#    shutil.move(f"{ROOT_DIR}\\Test_3_2_1.xlsx", f"{ROOT_DIR}\\Report\\Test_3_2_1.xlsx")
#    shutil.move(f"{ROOT_DIR}\\Test_3_2_2.xlsx", f"{ROOT_DIR}\\Report\\Test_3_2_2.xlsx")
#    shutil.move(f"{ROOT_DIR}\\Test_3_3.xlsx", f"{ROOT_DIR}\\Report\\Test_3_3.xlsx")
#    shutil.move(f"{ROOT_DIR}\\Test_3_3_1.xlsx", f"{ROOT_DIR}\\Report\\Test_3_3_1.xlsx")
#    shutil.move(f"{ROOT_DIR}\\Test_3_3_2.xlsx", f"{ROOT_DIR}\\Report\\Test_3_3_2.xlsx")
    


try:
    print(sys.argv)
    if len(sys.argv) < 3:
        DateFrom,DateTo,Start_year,End_year = DolbyUI.Get_Period("Q1","Q4",f"{Start_year}")
    del sys.modules["DolbyUI"] 
    del DolbyUI
    do_test3(value)
    change_names_test3()
    logger.info("Script Finished")
    create_dashboard()
    create_download()
    create_zip_archive()
    visualize.create_html(ROOT_DIR,10)
    sys.exit(0)
except Exception as err:
    logger.error(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    print(str(err) + "   -   " + "Error on line {}".format(sys.exc_info()[-1].tb_lineno))
    print(err)
    sys.exit(-1)