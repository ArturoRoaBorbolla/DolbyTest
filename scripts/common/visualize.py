import prettytable
import pandas as pd
import os
import sys

PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, f'{PRO_DIR}\\common')

import create_link


'''
def create_html(dir,size):
    csv_dir=f"{dir}\\csv"
    html_dir=f"{dir}\\html"
    os.makedirs(html_dir,exist_ok=True) 
    #try:
    listdir=os.listdir(csv_dir)
    for file_in_dir in listdir:
        if file_in_dir.endswith(".csv"):
            csv_file = pd.read_csv(f"{csv_dir}\\{file_in_dir}")
            real_size=len(csv_file)
            if size > real_size:
                size = real_size
            csv_file = csv_file[0:size]
            html_file=file_in_dir.replace(".csv",".html")
            with open(f'{html_dir}\\{html_file}',"w") as html:
                html.write('''#<Style>table {width: 70%;}</Style>
                #
'''                )
            with open(f'{html_dir}\\{html_file}',"ab") as html:
                html.write(csv_file.to_html().encode("utf-8"))
            with open(f'{html_dir}\\{html_file}',"a") as html:
                html.write(f'''
                #<button><a href="{csv_dir}\\{file_in_dir}" Download>Download Report</a></button>
''')
                    
    
    listdir=os.listdir(f"{dir}\\Visualization")
    for image in listdir:          
        extension=image.split(".")[1]
        html_name=image.replace(extension,"html")
        with open(f"{html_dir}\\{html_name}","w") as html_file:
            html_file.write(f'''#<html><style>
'''
            .parent {{
            width: 85%; 
            height: 85%;
            }}

            .parent img {{
            height: 100%;
            width: 100%;
            }}	
            </style>
            <body>
            <center>
            <div class="parent">
            <img src="{dir}\\Visualization\\{image}">
            </div>
            </center>
            <button><a href="{dir}\\Visualization\\{image}" Download>Download Image</a></button>
            </body>
            </html>''' #)
    #except:
    #    pass
                    
                
    #create_link.create_html(html_dir)



def create_html(dir,size):
    valid_image_extensions=['jpg','png','jpeg']
    #csv_dir=f"{dir}\\csv"
    html_dir=f"{dir}\\html"
    dashboard=f"{dir}\\Dashboard"
    os.makedirs(html_dir,exist_ok=True) 
    #try:
    listdir=os.listdir(dashboard)
    for file_in_dir in listdir:
        if file_in_dir.endswith(".csv"):
            csv_file = pd.read_csv(f"{dashboard}\\{file_in_dir}")
            real_size=len(csv_file)
            if size > real_size:
                size = real_size
            csv_file = csv_file[0:size]
            html_file=file_in_dir.replace(".csv",".html")
            with open(f'{html_dir}\\{html_file}',"w") as html:
                html.write('''<Center><Style>table {width: 80%;}</Style>''')
            with open(f'{html_dir}\\{html_file}',"ab") as html:
                html.write(csv_file.to_html().encode("utf-8"))
            with open(f'{html_dir}\\{html_file}',"a") as html:
                html.write(f'''<button><a href="{dashboard}\\{file_in_dir}" Download>Download Report</a></button></Center>''')
        extension=file_in_dir.split(".")[1]
        if extension in valid_image_extensions:
            html_name= file_in_dir.replace(extension,"html")
            with open(f"{html_dir}\\{html_name}","w") as html_file:
                html_file.write(f'''<html><style>
                .parent {{
                width: 85%; 
                height: 85%;
                }}

                .parent img {{
                height: 100%;
                width: 100%;
                }}	
                </style>
                <body>
                <center>
                <div class="parent">
                <img src="{dashboard}\\{file_in_dir}">
                </div>
                <button><a href="{dashboard}\\{file_in_dir}" download>Download Image</a></button></center>
                </body>
                </html>''' )
    #except:
    #    pass
    create_link.create_html(html_dir)