from plotly import graph_objects as go
import pandas as pd
import os
from create_graph import creategraph
import sys

if len(sys.argv) == 1:
    path_base='C:/AIVER/Results'
else:
    path_base='C:/AIVER/Results/Update'

# df1 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\TEST_08\OR_8_2_1.csv')

ResultDirectory=f'{path_base}/TEST_08/'
HtdocsResultDirectory='C:/AIVER/Dash/AIVER/Results/TEST_08/'
df1 = pd.read_csv(ResultDirectory+'OR_8_2_1.csv')

r1=df1.groupby(['F_Qtr','F_Year','GEO',"Parent_Expense_Type"]).agg(['sum'])

r1=r1.swaplevel(1,0,axis=1)
r1=r1.droplevel(0, axis=1)
a=r1.reset_index()
a["period"] = a["F_Year"].astype(str) + '/Q' + a["F_Qtr"].astype(str)

x=pd.unique(a['period'])
# print(x)
# print(a.head(2))

r1 = a[(a['GEO'] == 'NAMERICA')]
r2 = a[(a['GEO'] == 'EMEA')]
r3 = a[(a['GEO'] == 'APAC')]
# print(r3)

# print(r3.head(5))


trace1=go.Bar(x=x,y=r1['Sum(Approved_Amount)'],marker=dict(color='green',opacity=0.5),name="NAMERICA")
trace2=go.Bar(x=x,y=r2['Sum(Approved_Amount)'],marker=dict(color='red',opacity=0.5),name="EMEA")
trace3=go.Bar(x=x,y=r3['Sum(Approved_Amount)'],marker=dict(color='blue',opacity=0.5),name="APAC")

data=[trace1,trace2,trace3]

layout = go.Layout(
                   title_text='<b>' + 'Selected Parent Expense Types Trend Analysis' + '</b>',
                   title_x=0.5,
                   showlegend=True,
                   yaxis=dict(title="Total Amount (USD)"),
                   xaxis=dict(title="Fiscal Quarters"),
                   barmode="group")

fig = go.Figure(data,layout)

import plotly
if not os.path.exists("C:/AIVER/Dash/TestResultsForVisual/Test_08"):
    os.mkdir("C:/AIVER/Dash/TestResultsForVisual/Test_08")
plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_2_old.html', auto_open=False)
# fig.show()
print(r1['Sum(Approved_Amount)'].iloc[0],r2['Sum(Approved_Amount)'].iloc[0],r3['Sum(Approved_Amount)'].iloc[0])
filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_2.html'
headers=["NAmerica","EMEA", "APAC"]
data=[int(r1['Sum(Approved_Amount)'].iloc[0]),int(r2['Sum(Approved_Amount)'].iloc[0]),int(r3['Sum(Approved_Amount)'].iloc[0])]
html = creategraph(filename,headers,data)        
with open(filename,"w") as html_writer:
    html_writer.write(html)
print('\n\n\nGraph generated and saved in file location, plot show disabled')

