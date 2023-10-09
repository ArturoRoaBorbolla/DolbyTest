import pandas as pd
from create_graph import creategraph
import sys


if len(sys.argv) == 1:
    path_base='C:/AIVER/Results'
else:
    path_base='C:/AIVER/Results/Update'

#df1 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\TEST_08\OR_8_2_1.csv')
ResultDirectory=f'{path_base}/TEST_08/'
HtdocsResultDirectory='C:/xampp/htdocs/Dash/AIVER/Results/TEST_08/'

df1 = pd.read_csv(ResultDirectory+'OR_8_2_1.csv')
df2 = df1[(df1['GEO'] == 'APAC')]
df3=df2.sort_values(by=['F_Qtr','F_Year','Sum(Approved_Amount)'],ascending=False)


# for region  APAC
pv1 = pd.pivot_table(df3, columns=['F_Qtr', 'F_Year'], index=["Parent_Expense_Type"], values=['Sum(Approved_Amount)'],
                    aggfunc=sum, fill_value=0)
r11 = pv1.droplevel(0, axis=1)
r11.columns = [str(col[1]) + '/Q' + str(col[0]) for col in r11.columns.values]
# print(r11)
a1 = r11.reset_index()

a1.set_index("Parent_Expense_Type", inplace = True)
#print(a1)

legend=[]
for col in a1.columns:
    d=a1[col].to_dict()
    e={k: d[k] for k in sorted(d, key=d.get, reverse=True)}
    legend.append(list(e.keys())[:5])
# print(legend)
import itertools
leg=list(dict.fromkeys(itertools.chain.from_iterable(legend)))
print(leg)

# to find the odd parent type
# res = list(set.intersection(*map(set, legend)))
# print(res)
# not_in=(list(set(legend) - set(res)))
# print(not_in)

# below sort independently each column values
for col in a1.columns:
    if col not in ['Parent_Expense_Type']:
        a1[col] = sorted(a1[col], reverse=True)

x1 = [col for col in a1.columns if col not in ['Parent_Expense_Type']]

graph_values1 = a1#.drop(['Parent_Expense_Type'], axis=1)

from plotly import graph_objects as go
import plotly.express as px

data = {
    "model_E1": list(graph_values1[0:1].values.flatten()),
    "model_E2": list(graph_values1[1:2].values.flatten()),
    "model_E3": list(graph_values1[2:3].values.flatten()),
    "model_E4": list(graph_values1[3:4].values.flatten()),
    "model_E5": list(graph_values1[4:5].values.flatten()),
    "labels": x1
}
'''
print(leg)
fig = go.Figure(
    data=[

        go.Bar(
            name=leg[0],
            x=data["labels"],
            y=data["model_E1"],
            offsetgroup=1,
        ),
        go.Bar(
            name=leg[1],
            x=data["labels"],
            y=data["model_E2"],
            offsetgroup=1,
            base=data["model_E1"],
        ),
        go.Bar(
            name=leg[2],
            x=data["labels"],
            y=data["model_E3"],
            offsetgroup=1,
            base=[val1 + val2 for val1, val2 in zip(data["model_E1"], data["model_E2"])],
        ),
        go.Bar(
            name=leg[3],
            x=data["labels"],
            y=data["model_E4"],
            offsetgroup=1,
            base=[val1 + val2 + val3 for val1, val2, val3 in zip(data["model_E1"], data["model_E2"], data["model_E3"])],
        ),
        go.Bar(
            name=leg[4],
            x=data["labels"],
            y=data["model_E5"],
            offsetgroup=1,
            base=[val1 + val2 + val3 + val4 for val1, val2, val3, val4 in
                  zip(data["model_E1"], data["model_E2"], data["model_E3"], data["model_E4"])],
        ),

    ],
    layout=go.Layout(
        title_text="<b>"+"Selected Parent Expense Types Trend Analysis for Region APAC"+"</br>",
        title_x=0.5,
        yaxis_title="<b>"+"Total Amount (USD)"+"</br>",
        xaxis_title="<b>"+"Fiscal Quarters"+"</br>",
        showlegend=True,
        legend_title='Parent Expense Type',
    )
)

import plotly
plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_2_APAC.html', auto_open=False)
print("Graph plotted and saved, show disabled")
'''


#fig.show()
print()
filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_2_APAC.html'
headers=leg
data=[list(a1.iloc[1])][0]
print(data)
print(len(data),len(headers))
html = creategraph(filename,headers,data)        
with open(filename,"w") as html_writer:
    html_writer.write(html)
print('\n\n\nGraph generated and saved in file location, plot show disabled')




