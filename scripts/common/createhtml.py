import prettytable
import pandas as pd
import os
from scripts import create_link

def create_html(dir,size):
    listdir=os.listdir(dir)
    for file_in_dir in listdir:
        if file_in_dir.endswith(".csv"):
            file_in_dir=f"{dir}\\{file_in_dir}"
            #print(file_in_dir)
            csv_file = pd.read_csv(file_in_dir)
            real_size=len(csv_file)
            if size > real_size:
                size = real_size
            csv_file = csv_file[0:size]
            html_file=file_in_dir.replace(".csv",".html")
            with open(html_file,"w") as html:
                html.write('''<Style>table {width: 70%;}</Style>''')
            with open(html_file,"ab") as html:
                html.write(csv_file.to_html().encode("utf-8"))
            with open(html_file,"a") as html:
                html.write(f'''
                <button><a href="{file_in_dir}" Download>Download Report</a></button>
                ''')
                #for link_file in listdir:
                #    if link_file.endswith(".html"):
                #        link=link_file
                #        link_file=f"{dir}\\{link_file}"
                #        html.write(f'''
                #        <button><a href="{link_file}">Open Report: {link}</a></button>
                #        ''') 
    create_link.create_html(dir)
            