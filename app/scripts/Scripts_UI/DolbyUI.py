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
#import Test1



PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
ROOT_DIR = f"{PRO_DIR}"




global DateFrom
global DateTo
global root
global start1
global start2
global values
global year
global entry_year

global combo1
global combo2
global entry_year1
global entry_year2
global test1_entry
global test2_entry
global test3_entry

global start_period
global start_year
global end_period
global end_year

global test1_value
global test2_value
global test3_value

global Test_1_Treshold 
global Test_2_Treshold
global Test_3_Treshold


test3_value =100
test2_value = 150
test1_value =250


entry_year = ""
today = datetime.date.today()

values = ["Q1", "Q2", "Q3", "Q4"]
DateFrom = ""
DateTo = ""
year = today.strftime("%Y")
global root2

start1 = 0
start2 = 0






'''
def msgbox_info(title, text):
    root = tkinter.Tk()
    root.attributes('-topmost', 1)
    root.withdraw()
    tkinter.messagebox.showinfo(title, text)
    root.destroy()

'''

def on_closing2():
    try:
        global root2
        global root
        root2.withdraw()
        root.deiconify()
    except:
        pass


def submit():
    global DateFrom
    global DateTo
    global DtFrom
    global DtTo
    global entry_1
    global root
    global year
    global entry_year

    global start_period
    global start_year
    global end_period
    global end_year

    global test1_value
    global test2_value
    global test3_value

    DateFrom = combo1.get()
    start_year = entry_year1.get()
    DateTo = combo2.get()
    end_year = entry_year2.get()
    test1_value = test1_entry.get()
    test2_value = test2_entry.get()
    test3_value = test3_entry.get()

    # entry_year = str(entry_1.get())
    if start_year == "" or end_year == "":
        start_year = year
        end_year = year
    else:
        year = start_year

    #print("DateFrom : " + DateFrom)
    #print("DateTo : " + DateTo)
    #print("Year : " + start_year, end_year)
    if DateFrom == "" or DateTo == "":
        CTkMessagebox(title="Error", message="Any value could be empty!!!", icon="cancel")
    else:
        #Test.set_variables(DateFrom,DateTo)
        try:
            root.withdraw()
            root.destroy()
        except:
            try:
                root.destroy()
            except:
                pass
        try:
            root.withdraw()
            root2.destroy()
        except:
            try:
                root2.destroy()
            except:
                pass
    
    


def combobox_callback(val):
    global DateFrom
    DateFrom = val
    combo_box1 = val


def combobox2_callback(val):
    global DateTo
    DateTo = val
    combo_box2 = val


def Get_Period(From, To, yr):
    global DateFrom
    global DateTo
    global root
    global root2
    global start1
    global DtFrom
    global DtTo
    global values
    global year
    global entry_year
    # global start_period
    # global start_year
    # global end_period
    # global end_year
    global test1_entry
    global test2_entry
    global test3_entry
    # global combo_box1
    # global combo_box2
    global combo1
    global combo2
    global entry_year1
    global entry_year2
    
    if start1 == 0:
        DateFrom = From
        DateTo = To
        root = customtkinter.CTk()
        start1 = 1
    try:
        root2.withdraw()
    except:
        pass

    root.geometry("650x450")
    root.title("Dolby Period Selection")

    entry_year1 = tk.StringVar()
    entry_year1.set("2023")
    entry_year2 = tk.StringVar()
    entry_year2.set("2023")
    combo_box1 = tk.StringVar()
    combo_box2 = tk.StringVar()
    test1_entry = tk.StringVar()
    test2_entry = tk.StringVar()
    test3_entry = tk.StringVar()
    test1_entry.set(f"{test1_value}")
    test2_entry.set(f"{test2_value}")
    test3_entry.set(f"{test3_value}")


    header_label = customtkinter.CTkLabel(root, text="Select Period", font=("Arial", 14, "bold"))
    header_label.grid(row=0, column=0, padx=20, pady=10)

    start_label = customtkinter.CTkLabel(root, text="Start Period")
    start_label.grid(row=1, column=0, padx=20, pady=10)

    combo1 = customtkinter.CTkComboBox(master=root, values=values,
                                       variable=combo_box1)
    combo1.set("Q1")
    combo1.grid(row=1, column=1, padx=20, pady=10)

    entry_yr1 = customtkinter.CTkEntry(master=root, textvariable=entry_year1, placeholder_text=f"{yr}")
    entry_yr1.grid(row=1, column=2, padx=10, pady=30)

    end_label = customtkinter.CTkLabel(root, text="End Period")
    end_label.grid(row=2, column=0, padx=20, pady=10)
    combo2 = customtkinter.CTkComboBox(master=root, values=values,
                                       variable=combo_box2)
    combo2.set("Q1")
    combo2.grid(row=2, column=1, padx=20, pady=10)

    entry_yr2 = customtkinter.CTkEntry(master=root, textvariable=entry_year2, placeholder_text=f"{yr}")
    entry_yr2.grid(row=2, column=2, padx=10, pady=30)

    #test1_label = customtkinter.CTkLabel(root, text="Test 1 Employee Meal Threshold")
    #test1_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')

    #test1_entry = customtkinter.CTkEntry(root, textvariable=test1_entry, placeholder_text=f"{test1_value}")
    #test1_entry.grid(row=3, column=1, padx=10, pady=10)

    #test2_label = customtkinter.CTkLabel(root, text="Test 2 Travel Meal Threshold")
    #test2_label.grid(row=4, column=0, padx=20, pady=10, sticky='w')

    #test2_entry = customtkinter.CTkEntry(root, textvariable=test2_entry, placeholder_text=f"{test2_value}")
    #test2_entry.grid(row=4, column=1, padx=10, pady=10)

    ##test3_label = customtkinter.CTkLabel(root, text="Test 3 Third-Party Meal Threshold")
    #test3_label.grid(row=5, column=0, padx=20, pady=10, sticky='w')

    #test3_entry = customtkinter.CTkEntry(root, textvariable=test3_entry, placeholder_text=f"{test3_value}")
    #test3_entry.grid(row=5, column=1, padx=10, pady=10)

    confirm_date = customtkinter.CTkButton(root, text="Confirm Quarter", hover=True, command=submit)
    confirm_date.grid(row=6, column=0, columnspan=3, padx=10, pady=30)
    root.mainloop()
    return(DateFrom,DateTo,start_year,end_year)






#Get_Period("Q1","Q1" , year)
#Test.do_test1(test1_value)
#Test.do_test2(test2_value)
#Test.do_test3(test3_value,test3_value)
