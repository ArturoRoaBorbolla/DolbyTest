def create_html(image):
    extension=image.split(".")[1]
    html_name=image.replace(extension,"html")
    with open(html_name,"w") as html_file:
        html_file.write(f'''<html><style>
        .parent {{
           width: 50%; 
           height: 50%;
        }}

        .parent img {{
           height: 100%;
           width: 100%;
        }}	
        </style>
        <body>
        <center>
        <div class="parent">
           <img src="{image}">
        </div>
        </center>
        </body>
        </html>''' )