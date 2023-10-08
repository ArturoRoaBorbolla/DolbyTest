import os
import sys
from ast import literal_eval
import json

def return_data():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(ROOT_DIR)
    #data_dir=f'{ROOT_DIR}\\assets\\json'
    data_dir=f'{ROOT_DIR}\\scripts'
    print(data_dir)
    json_data={}
    #with open(f"{data_dir}\\thresholds.json","r") as json_file:
    with open(f"{data_dir}\\tresholds.json","r") as json_file:
        json_data=literal_eval(json_file.read())
        #print(json_data)
    return json_data