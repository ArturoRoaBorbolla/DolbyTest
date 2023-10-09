import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from create_graph import creategraph
import sys

if len(sys.argv) == 1:
    path_base='C:/AIVER/Results'
else:
    path_base='C:/AIVER/Results/Update'

ResultDirectory=f'{path_base}/TEST_08/'
HtdocsResultDirectory='C:/AIVER/Dash/AIVER/Results/TEST_08/'
df1 = pd.read_csv(ResultDirectory+'OR_8_3_3.csv')

r1=df1[['Parent_Expense_Type','Sum(Approved_Amount_RPT)','F_Qtr']].groupby(['F_Qtr','Parent_Expense_Type']).agg(['sum'])
# print(r1)

a=r1.droplevel(0, axis=1)
a=a.reset_index()
print(a)
'''
FiscalQtr=[]
for i in a['F_Qtr']:
    i='Q'+str(i)
    FiscalQtr.append(i)


# Region APAC

fig=go.Figure(go.Bar(
    x=a['Parent_Expense_Type'],
    y=a['sum'],
    marker=dict(color=a['F_Qtr']),
    text=FiscalQtr,
    textposition='inside',
    #  texttemplate='Q',),
))


fig.update_yaxes(title_text="Total Amount (USD)")

# Change the bar mode
fig.update_layout(
    title_text='<b>' + 'Parent Expense Types for Region APAC' + '</b>',
    # # title='Score Report > 95',
    title_x=0.5,
    showlegend=False,
    barmode='stack',
    )

import os
if not os.path.exists("C:\AIVER\Dash\TestResultsForVisual\Test_08"):
    os.mkdir("C:\AIVER\Dash\TestResultsForVisual\Test_08")

plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_3_APAC.html', auto_open=False)
# fig.show()
'''



filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_3_APAC.html'
headers=a['Parent_Expense_Type']
data=a['sum']
html = creategraph(filename,headers,data)        
with open(filename,"w") as html_writer:
    html_writer.write(html)
print('\n\n\nGraph generated and saved in file location, plot show disabled')



