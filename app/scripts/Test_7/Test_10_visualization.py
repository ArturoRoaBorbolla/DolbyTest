import plotly.graph_objects as go
import pandas as pd
import sys
import os


ROOT_DIR = PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, f'{PRO_DIR}\\common')
sys.path.insert(2, f'{PRO_DIR}\\Scripts_UI')

from create_graph import creategraph

TEST_DIR = f"{ROOT_DIR}\\Test_7"
Output_dir = f"{TEST_DIR}\\Output"
html_dir= f'{Output_dir}\\html'
csv_folder = f'{Output_dir}\\csv'

os.makedirs(html_dir, exist_ok=True)
df = pd.read_csv(f'{csv_folder}\\OR_07_4_3.csv')

# df = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\OR_07_4_3.csv')

alter_columns = ['Employee ID', 'Name', 'Employee_Org_Unit_2_Code', 'Country', 'Total Amount (USD)', 'Submission Count', 'Average Claim Per Report']

fig = go.Figure(data=[go.Table(

    header=dict(values=['<b>'+ x +'</b>' for x in list(alter_columns)],
                fill_color='paleturquoise',
                align='right',
                ),

    cells=dict(
               # values=df.values.T, # to transpose DF values into cells
               values=[df['EMP_ID'],df['Employee'],df['Employee_Org_Unit_2_Code'],df['Employee_Country_Code'],
                       df['Sum(Approved_Amount_RPT)'].apply(lambda x:f"${str(round(x,2))}"),df['Count(Submissions)'],
                       df['Average Claim Per Report'].round(2)],
               fill_color='lavender',
               align='right'))
])
fig.update_layout(
    # width=1100,
    height=500,
    title_text='<b>'+'Top 25 Submitters of Out-of-Pocket Expenses'+'</b>',
    title_x=0.5,
    )

import plotly
import os
#if not os.path.exists("C:\AIVER\Dash\TestResultsForVisual\Test_10"):
#    os.mkdir("C:\AIVER\Dash\TestResultsForVisual\Test_10")
plotly.offline.plot(fig, filename=f'{html_dir}\\Test_10.html', auto_open=False)
# fig.show()

print('\n\n\nGraph generated and saved in file location, plot show disabled')