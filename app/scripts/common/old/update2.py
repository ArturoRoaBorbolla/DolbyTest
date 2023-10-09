import os
import sqlite3 as db
import pandas
import re

con = db.connect('C:\\Aiver\\Dolbyb.db', isolation_level=None) # change to 'sqlite:///your_filename.db'
Internal = os.listdir("C:\\Aiver\\Reports\\Internal")
External = os.listdir("C:\\Aiver\\Reports\\External")
print(Internal,External,'C:\\Aiver\\Dolbyb.db')
cur = con.cursor()
cur.execute("CREATE TABLE  CR_1 ('Approval_Status' TEXT,'Report__' TEXT,'Entry_Key' TEXT,'Entry_Legacy_Key' TEXT,'Allocation_Key' TEXT,'Org_Unit_2_Code' TEXT,'Org_Unit_4_Code' TEXT,'Total_Report_Amount_RPT' TEXT,'Total_Approved_Amount_RPT' TEXT,'Reporting_Currency1' TEXT,'EMP_ID' TEXT,'Employee' TEXT,'Employee_Org_Unit_2_Code' TEXT,'Employee_Org_Unit_4_Code' TEXT,'Employee_Country_Code' TEXT,'Submitted_by_a_Delegate' TEXT,'Report_Name' TEXT,'Vendor' TEXT,'Purpose' TEXT,'City_Location' TEXT,'State_Province_Region' TEXT,'Country' TEXT,'Last_Submitted_Date' DATE,'Total_Report_Amount' TEXT,'Total_Personal_Amount' TEXT,'Total_Claimed_Amount' TEXT,'Number_of_Entries' TEXT,'Number_of_Comments' TEXT,'Transaction_Date' DATE,'Payment_Type_Code' TEXT,'Payment_Type' TEXT,'Expense_Type' TEXT,'Parent_Expense_Type' TEXT,'GL_Account' TEXT,'A_P_Processed_Date' DATE,'Reporting_Currency2' TEXT,'Approved_Amount_RPT' TEXT,'Reimb_Exp_Amt' TEXT,'Reimb_Curr' TEXT,'Paid_Date' DATE,'Receipt_Required' TEXT,'Receipt_Image_Required' TEXT,'Receipt_Received' TEXT,'Number_of_Attendees' TEXT)")
cur.execute("CREATE TABLE  CR_2 ('Uno' TEXT,'Dos' DATE)")
st= "insert into CR_2 values ('Texto','2023-02-02 00:00:00')"
cur.execute(st)
con.commit()
data={}
data["CR_1"]="('Approval_Status','Report__','Entry_Key','Entry_Legacy_Key','Allocation_Key','Org_Unit_2_Code','Org_Unit_4_Code','Total_Report_Amount_RPT','Total_Approved_Amount_RPT','Reporting_Currency1','EMP_ID','Employee','Employee_Org_Unit_2_Code','Employee_Org_Unit_4_Code','Employee_Country_Code','Submitted_by_a_Delegate','Report_Name','Vendor','Purpose','City_Location','State_Province_Region','Country','Last_Submitted_Date','Total_Report_Amount','Total_Personal_Amount','Total_Claimed_Amount','Number_of_Entries','Number_of_Comments','Transaction_Date','Payment_Type_Code','Payment_Type','Expense_Type','Parent_Expense_Type','GL_Account','A_P_Processed_Date','Reporting_Currency2','Approved_Amount_RPT','Reimb_Exp_Amt','Reimb_Curr','Paid_Date','Receipt_Required','Receipt_Image_Required','Receipt_Received','Number_of_Attendees')"
st2='''Insert into CR_1 ('Approval_Status','Report__','Entry_Key','Entry_Legacy_Key','Allocation_Key','Org_Unit_2_Code','Org_Unit_4_Code','Total_Report_Amount_RPT','Total_Approved_Amount_RPT','Reporting_Currency1','EMP_ID','Employee','Employee_Org_Unit_2_Code','Employee_Org_Unit_4_Code','Employee_Country_Code','Submitted_by_a_Delegate','Report_Name','Vendor','Purpose','City_Location','State_Province_Region','Country','Last_Submitted_Date','Total_Report_Amount','Total_Personal_Amount','Total_Claimed_Amount','Number_of_Entries','Number_of_Comments','Transaction_Date','Payment_Type_Code','Payment_Type','Expense_Type','Parent_Expense_Type','GL_Account','A_P_Processed_Date','Reporting_Currency2','Approved_Amount_RPT','Reimb_Exp_Amt','Reimb_Curr','Paid_Date','Receipt_Required','Receipt_Image_Required','Receipt_Received','Number_of_Attendees') Values ('Approved','210497.0','1315927.0','1643528.0','1469895.0','1000.0','F3144','0.0','0.0','USD','302225.0','Zuena, Jake','1000.0','F3144','US','N','iPad Stands Purchase and Return','WAL-MART #2119','Bought these iPad holders for a demonstration','Milpitas','California','UNITED STATES','2023-02-21 00:00:00','0.0','0.0','0.0','2.0','3.0','2023-02-13 00:00:00','IBCP','US Bank Visa','Office Supplies','06. Office Expenses','644000.0','2023-02-21 00:00:00','USD','55.5','55.5','USD','2023-02-21 00:00:00','N','N','N','0.0')'''
print(st)
#print(st2)
cur.execute(st)
#cur.execute(st2)
con.commit()

df = pandas.read_excel(f"C:\\Aiver\\Reports\\Internal\\CR_1.xlsx",skiprows=1)
substatement=""
for index,row in df.iterrows():
    count=0
    for value in row:
        #print(value,type(value))
        if type(value) is pandas._libs.tslibs.timestamps.Timestamp:
            replaced = f"'{value.to_pydatetime()}'" #to_pydatetime()
        else:
            if type(value) is str: 
                replaced = value.replace("'s","s")
                replaced = f"'{replaced}'"
            else:
                replaced = f"'{value}'"
        count+=1
        substatement += f"{replaced},"
    substatement=substatement[:-1]
    statement =f'''Insert into CR_1 {data["CR_1"]} Values ({substatement})'''
    statement=statement.replace("nan","")
    print(f"{statement} \n")
    cur.execute(statement)
    con.commit()
    substatement=""
    statement=""
     
    break
con.close()
a=set(st2.split())
b=set(statement.split())
a.symmetric_difference(b)
