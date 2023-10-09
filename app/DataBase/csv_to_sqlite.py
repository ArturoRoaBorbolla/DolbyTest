import csv
import pandas as pd
import sqlite3
import sys
import os
from time import sleep


PRO_DIR = os.path.dirname(os.path.abspath(__file__))
print(PRO_DIR)
ROOT_DIR = f"{PRO_DIR}\\Input"

database = 'Dolby.db'
connection=sqlite3.connect(database)
cursor=connection.cursor()

CR1_folder=f"{ROOT_DIR}\\CR_1"
CR2_folder=f"{ROOT_DIR}\\CR_2"
Departments_folder=f"{ROOT_DIR}\\Departments"


CR1_files = os.listdir(CR1_folder)
CR2_files = os.listdir(CR2_folder)
Dpt_files = os.listdir(Departments_folder)




for file in CR1_files:
        tabs = pd.ExcelFile(f'{CR1_folder}\\{file}').sheet_names
        for tab in tabs:
                print(f"Trying to insert {tab}")
                skip_rows=0
                while True:
                        excel_df = pd.read_excel(f'{CR1_folder}\\{file}',skiprows=[skip_rows],sheet_name=tab)
                        columns = excel_df.head()
                        print(columns)
                        if 'Approval Status' in columns:
                                break
                        else:
                                skip_rows+=1
                #print("Out of the while")
                Table_query = f'CREATE TABLE IF NOT EXISTS CR_1 ('
                Table_query +=''.join(f'{x.replace(" ","_").replace("/","_").replace("(","_").replace(")","_").replace("-","_").replace("#","_").replace(".","_")} Text,' for x in excel_df.head())
                Table_query = Table_query[:-1] 
                Table_query +=')'
                print(Table_query)
                cursor.execute(Table_query)
                error_count=0
                count=0
                for index, row in excel_df.iterrows():
                    try:
                        converted = [x.replace("\"","") if type(x) is str else x.date().strftime("%Y%m%d") if type(x) is pd._libs.tslibs.timestamps.Timestamp else x  for x in row]       
                        Insert= f'INSERT INTO CR_1 VALUES ('
                        Insert += ''.join(f'"{x}",' for x in converted)
                        Insert = Insert[:-1]
                        Insert += ')' 
                        cursor.execute(Insert)
                        count+=1
                    except:
                        error_count+=1
                connection.commit()
                print(f" There was {error_count} Errors on insert. {count} Inserted , {error_count/count} Percentage of Error on inserted..... {tab} inserted on DB")
                
print("\n\n\nCR_1 Finished\n\n\n")
sleep(5)




for file in CR2_files:
        tabs = pd.ExcelFile(f'{CR2_folder}\\{file}').sheet_names
        for tab in tabs:
                print(f"Trying to insert {tab}")
                skip_rows=0
                while True:
                        excel_df = pd.read_excel(f'{CR2_folder}\\{file}',skiprows=[skip_rows])
                        columns = excel_df.head()
                        print(columns)
                        if 'Employee' in columns:
                                break
                        else:
                                skip_rows+=1
                Table_query = f'CREATE TABLE IF NOT EXISTS CR_2 ('
                Table_query +=''.join(f'{x.replace(" ","_").replace("/","_").replace("(","_").replace(")","_").replace("-","_").replace("#","_").replace(".","_")} Text,' for x in excel_df.head())
                Table_query = Table_query[:-1] 
                Table_query +=')'
                print(Table_query)
                cursor.execute(Table_query)
                error_count=0
                count=0
                for index, row in excel_df.iterrows():
                    try:
                        converted = [x.replace("\"","") if type(x) is str else x.date().strftime("%Y%m%d") if type(x) is pd._libs.tslibs.timestamps.Timestamp else x  for x in row]       
                        Insert= f'INSERT INTO CR_2 VALUES ('
                        Insert += ''.join(f'"{x}",' for x in converted)
                        Insert = Insert[:-1]
                        Insert += ')' 
                        cursor.execute(Insert)
                        count+=1
                    except:
                        error_count+=1
                connection.commit()
                connection.close()
                print(f"  There was {error_count} Errors on insert. {count} Inserted , {error_count/count} Percentage of Error on inserted... {tab} inserted on DB")
                
print("\n\n\nCR_2 Finished\n\n\n")
sleep(5)
