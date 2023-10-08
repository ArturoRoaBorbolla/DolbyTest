import plotly.graph_objects as go
import pandas as pd
import os
from create_graph import creategraph
import sys

# df1 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\OR_2_1.csv')
# df2 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\OR_2_2_3_1.csv')
# df3 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\OR_2_2_3_2.csv')

#For ALex machine comment above line, uncomment below either one


if len(sys.argv) == 1:
    path_base='C:/AIVER/Results'
else:
    path_base='C:/AIVER/Results/Update'
    
ResultDirectory=f'{path_base}/TEST_02/'
HtdocsResultDirectory='C:/AIVER/Dash/AIVER/Results/TEST_02/'

df1 = pd.read_csv(ResultDirectory+'OR_2_1.csv')
df2 = pd.read_csv(ResultDirectory+'OR_2_2_3_1.csv')
df3 = pd.read_csv(ResultDirectory+'OR_2_2_3_2.csv')

yaxis_values=[]
us_amt =df1[['Approved_Amount_RPT']].agg(['sum']).reset_index().round(0)
# print(us_amt)
# print(us_amt['Approved_Amount_RPT'][0])
yaxis_values.append(int(us_amt['Approved_Amount_RPT'][0]))

nonus_gifts =df2[['Approved_Amount_RPT']].agg(['sum']).reset_index().round(0)
yaxis_values.append(int(nonus_gifts['Approved_Amount_RPT'][0]))

nonus_meals =df3[['Approved_Amount_RPT']].agg(['sum']).reset_index().round(0)
yaxis_values.append(int(nonus_meals['Approved_Amount_RPT'][0]))
# print(yaxis_values)


'''
yaxis_dollar=[]
for i in yaxis_values:
    i = '${{}}'.format(i)
    yaxis_dollar.append(i)
# print(type(yaxis_values))

colors = ['crimson','indianred','lightsalmon']
fig = go.Figure(go.Bar(
    x=['US','Non US - Gifts','Non US - Meals'],
    y=yaxis_values,
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
    ),
    text=yaxis_dollar,
    # texttemplate='$',
    textposition='outside',

))
fig.update_yaxes(title_text="Amount (USD)")

fig.update_layout(
    width=800, height=500,
    # coloraxis=dict(colorscale='Bluered_r'),
    title_text='<b>'+'Government Meals & Entertainment For Approval'+'</b>',
    title_x=0.5,
    yaxis=dict(
        showgrid=False,
        showline=True,
        showticklabels=True,
        # domain=[0, 0.85],
        # # autorange="reversed",
        # automargin=False,
    ),
    xaxis=dict(
        # tickangle=45,
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=False,
        # domain=[0, 0.3],
    ),
)
import plotly
plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_02/Test_02.html', auto_open=False)
# fig.show()
print('\n\n\nGraph generated and saved in file location, plot show disabled')

'''
filename='C:/AIVER/Dash/TestResultsForVisual/Test_02/Test_02.html'
headers=["Us","Non Us Gifts", "Non Us Meals"]
data=[int(us_amt['Approved_Amount_RPT'][0]),int(nonus_gifts['Approved_Amount_RPT'][0]),int(nonus_meals['Approved_Amount_RPT'][0])]
html = creategraph(filename,headers,data)        
with open(filename,"w") as html_writer:
    html_writer.write(html)