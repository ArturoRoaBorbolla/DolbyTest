import os
import sqlite3 as db
import pandas
import re

con = db.connect('C:\\Aiver\\Dolby.db') # change to 'sqlite:///your_filename.db'
Internal = os.listdir("C:\\Aiver\\Reports\\Internal")
External = os.listdir("C:\\Aiver\\Reports\\External")
print(Internal,External,'C:\\Aiver\\Dolby.db')
cur = con.cursor()

#cur.execute("CREATE TABLE CR_1 ('Approval_Status' TEXT,'Report__' TEXT,'Entry_Key' TEXT,'Entry_Legacy_Key' TEXT,'Allocation_Key' TEXT,'Org_Unit_2_Code' TEXT,'Org_Unit_4_Code' TEXT,'Total_Report_Amount_RPT' TEXT,'Total_Approved_Amount_RPT' TEXT,'Reporting_Currency1' TEXT,'EMP_ID' TEXT,'Employee' TEXT,'Employee_Org_Unit_2_Code' TEXT,'Employee_Org_Unit_4_Code' TEXT,'Employee_Country_Code' TEXT,'Submitted_by_a_Delegate' TEXT,'Report_Name' TEXT,'Vendor' TEXT,'Purpose' TEXT,'City_Location' TEXT,'State_Province_Region' TEXT,'Country' TEXT,'Last_Submitted_Date' DATE,'Total_Report_Amount' TEXT,'Total_Personal_Amount' TEXT,'Total_Claimed_Amount' TEXT,'Number_of_Entries' TEXT,'Number_of_Comments' TEXT,'Transaction_Date' DATE,'Payment_Type_Code' TEXT,'Payment_Type' TEXT,'Expense_Type' TEXT,'Parent_Expense_Type' TEXT,'GL_Account' TEXT,'A_P_Processed_Date' DATE,'Reporting_Currency2' TEXT,'Approved_Amount_RPT' TEXT,'Reimb_Exp_Amt' TEXT,'Reimb_Curr' TEXT,'Paid_Date' DATE,'Receipt_Required' TEXT,'Receipt_Image_Required' TEXT,'Receipt_Received' TEXT,'Number_of_Attendees' TEXT)")
#cur.execute("CREATE TABLE CR_2 ('Uno' TEXT,'Dos' DATE)")
#st= "insert into CR_2 values ('Texto','2023-02-02 00:00:00')"

data={}
data["CR_1"]="('Approval_Status','Report__','Entry_Key','Entry_Legacy_Key','Allocation_Key','Org_Unit_2_Code','Org_Unit_4_Code','Total_Report_Amount_RPT','Total_Approved_Amount_RPT','Reporting_Currency1','EMP_ID','Employee','Employee_Org_Unit_2_Code','Employee_Org_Unit_4_Code','Employee_Country_Code','Submitted_by_a_Delegate','Report_Name','Vendor','Purpose','City_Location','State_Province_Region','Country','Last_Submitted_Date','Total_Report_Amount','Total_Personal_Amount','Total_Claimed_Amount','Number_of_Entries','Number_of_Comments','Transaction_Date','Payment_Type_Code','Payment_Type','Expense_Type','Parent_Expense_Type','GL_Account','A_P_Processed_Date','Reporting_Currency2','Approved_Amount_RPT','Reimb_Exp_Amt','Reimb_Curr','Paid_Date','Receipt_Required','Receipt_Image_Required','Receipt_Received','Number_of_Attendees')"

#cur.execute(st)
#con.commit()

#len_L=len(data["CR_1"][1:-1].split(","))
#lenv=[]

for i in Internal:
    print(f"Trying to insert {i}")
    try:
        print("Trying Csv")
        df = pandas.read_csv(f"C:\\Aiver\\Reports\\Internal\\{i}",skiprows=1)
    except Exception as e:
        try:
            print(f"Trying Excel {e}")
            df = pandas.read_excel(f"C:\\Aiver\\Reports\\Internal\\{i}",skiprows=1)
        except Exception as e:
            print(f" No csv, No Excel {e}")
            continue
    table_name = i.split(".")[0]
    name_list=[]
    for column in df.columns:
        name_list.append(column)
    columns="".join(f"{x}," for x in name_list)
    columns=f"({columns[:-1]})"
    substatement=""
    for index,row in df.iterrows():
        count=0
        for value in row:
            if type(value) is pandas._libs.tslibs.timestamps.Timestamp:
                replaced = f"{value.date()}".replace("-","") #to_pydatetime()
            elif type(value) is str:
                #print(f"found str {value}")
                replaced = value.replace("'","")
                #print(f"Replaced: {replaced}")
                replaced = f"'{replaced}'"
            elif type(value) is float:
                if str(value)[-2:] == ".0":
                    replaced=int()
                    replaced = f"'{replaced}'"
            else:
                replaced = f"'{value}'"
            count+=1
            substatement += f"{replaced},"
        substatement=substatement[:-1]
        #lenv.append(len(substatement.split(",")))
        #print(substatement)
        statement =f'''Insert into {table_name} {data[table_name]} Values ({substatement})'''
        statement=statement.replace("nan","")
        #print(f"{statement} \n")
        cur.execute(statement)
        con.commit()
        substatement=""
        statement=""
    
for i in External:
    print(f"Trying to insert {i}")
    try:
        print("Trying Csv")
        df = pandas.read_csv(f"C:\\Aiver\\Reports\\External\\{i}",skiprows=1)
    except Exception as e:
        try:
            print(f"Trying Excel {e}")
            df = pandas.read_excel(f"C:\\Aiver\\Reports\\External\\{i}",skiprows=1)
        except Exception as e:
            print(f" No csv, No Excel {e}")
            continue
    table_name = i.split(".")[0]
    st=f'Delete from {table_name}'
    print(st)
    cur.execute(st)
    con.commit()
    name_list=[]
    for column in df.columns:
        name_list.append(column)
    columns="".join(f"{x}," for x in name_list)
    columns=f"({columns[:-1]})"
    substatement=""
    for index,row in df.iterrows():
        count=0
        for value in row:
            if type(value) is pandas._libs.tslibs.timestamps.Timestamp:
                replaced = f"{value.date()}".replace("-","") #to_pydatetime()
            elif type(value) is str:
                #print(f"found str {value}")
                replaced = value.replace("'","")
                #print(f"Replaced: {replaced}")
                replaced = f"'{replaced}'"
            elif type(value) is float:
                if str(value)[-2:] == ".0":
                    replaced=int()
                    replaced = f"'{replaced}'"
            else:
                replaced = f"'{value}'"
            count+=1
            substatement += f"{replaced},"
        substatement=substatement[:-1]
        #lenv.append(len(substatement.split(",")))
        #print(substatement)
        statement =f'''Insert into {table_name} Values ({substatement})'''
        statement=statement.replace("nan","")
        #print(f"{statement} \n")
        cur.execute(statement)
        con.commit()
        substatement=""
        statement=""
    
cur.close()
con.close() 
#print(st)
#print(data)
