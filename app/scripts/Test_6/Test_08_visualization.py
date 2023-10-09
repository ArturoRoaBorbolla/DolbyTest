import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import sys

# Local path
# df1 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\TEST_08\OR_8_1_1.csv')
# df2 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\TEST_08\OR_8_1_2.csv')
# df3 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\TEST_08\OR_8_1_3.csv')


if len(sys.argv) == 1:
    path_base='C:/AIVER/Results'
else:
    path_base='C:/AIVER/Results/Update'

ResultDirectory=f'{path_base}/TEST_08/'
HtdocsResultDirectory='C:/AIVER/Dash/AIVER/Results/TEST_08/'
df1 = pd.read_csv(ResultDirectory+'OR_8_1_1.csv')
df2 = pd.read_csv(ResultDirectory+'OR_8_1_2.csv')
df3 = pd.read_csv(ResultDirectory+'OR_8_1_3.csv')


# # Histogram
# Creating three subplots
fig = make_subplots(rows=1, cols=3, specs=[[{},{},{}]], column_widths = [0.3,0.3,0.3],
                    subplot_titles = ("N AMERICA","EMEA","APAC"))

fig.append_trace(go.Bar(
    x=df1['Employee'],
    y=df1['Sum(Approved_Amount_RPT)'],
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),

), 1, 1)

fig.append_trace(go.Bar(
    x=df2['Employee'],
    y=df2['Sum(Approved_Amount_RPT)'],
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),

), 1, 2)

fig.append_trace(go.Bar(
    x=df3['Employee'],
    y=df3['Sum(Approved_Amount_RPT)'],
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),

), 1, 3)

# Update xaxis properties
# fig.update_xaxes(title_text="Per Attendee Amount (USD)", row=1, col=1)#,range=[0, 10000])
fig.update_yaxes(title_text="Total Amount (USD)",row=1, col=1)
fig.update_xaxes(tickangle=45)


fig.update_layout(
    showlegend=False,
    title_text='<b>' + 'Top 25 Employees by Spend by Region' + '</b>',
    title_x=0.5,
    yaxis=dict(
        showgrid=True,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
        # autorange="reversed",
        automargin=False,
        tickprefix = "$",
    ),
    yaxis2=dict(
        showgrid=True,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
        # autorange="reversed",
        automargin=False,
        tickprefix = "$",
    ),
    yaxis3=dict(
        showgrid=True,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
        # autorange="reversed",
        automargin=False,
        tickprefix = "$",
    ),
    xaxis=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.3],
    ),

    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
)

import plotly
import os
if not os.path.exists("C:\AIVER\Dash\TestResultsForVisual\Test_08"):
    os.mkdir("C:\AIVER\Dash\TestResultsForVisual\Test_08")
plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_1.html', auto_open=False)
# fig.show()
print('\n\n\nGraph generated and saved in file location, plot show disabled')
