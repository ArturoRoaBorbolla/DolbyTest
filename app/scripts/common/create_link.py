import os

def create_html(dir):
    html_list=[]
    listdir=os.listdir(dir)
    for files in listdir:
        if files.endswith(".html"):
            html_list.append(f"{dir}/{files}")
    #print(html_list)
    if len(html_list) > 1:
        for html_file in html_list:
            html_string_list=[]
            html_openning=""
            html_footer=""
            with open(html_file,"rb") as html:
                html_string=html.read().decode()
                #print(html_string_list)
                html_string_list=html_string.splitlines()
                html_openning= "".join(x for x in html_string_list[0:-2])
                html_footer= "".join(x for x in html_string_list[-2:])
            html_openning =f"{html_openning}<Center>"
            html_footer=f"</Center>{html_footer}"
            html_to_insert="<br>"
            for link_file in html_list:
                    if link_file.endswith(".html"):
                        link=link_file.split("/")[-1]
                        html_to_insert+=f'''<button><a href="{link_file}">Open Report: {link}</a></button>'''
            print(f"Processing: {html_file}")
            print(html_string_list[-1].strip().upper())
            if html_string_list[-1].strip().upper()=="</HTML>" or  html_string_list[-1].strip().upper()=="</BODY>":
                html_to_write=f"{html_openning}{html_to_insert}{html_footer}".encode()
                with open(html_file,"wb") as html:
                    html.write(html_to_write)
            else:
                #{html_to_insert}
                html_to_write=f"{html_string}<Center>{html_to_insert}</Center>".encode()
                print(html_to_write)
                with open(html_file,"wb") as html:
                    html.write(html_to_write)
            
                