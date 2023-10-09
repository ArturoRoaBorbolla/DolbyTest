import pandas as pd
import sys
#df1 = pd.read_csv('D:\SOA_Project\SOA_Histogram\Test_visualization\CSV_Inputs\TEST_08\OR_8_2_1.csv')


if len(sys.argv) == 1:
    path_base='C:/AIVER/Results'
else:
    path_base='C:/AIVER/Results/Update'
ResultDirectory=f'{path_base}/TEST_08/'
HtdocsResultDirectory='C:/xampp/htdocs/Dash/AIVER/Results/TEST 008/'

df1 = pd.read_csv(ResultDirectory+'OR_8_2_1.csv')
df2 = df1[(df1['GEO'] == 'NAMERICA')]
df3 = df1[(df1['GEO'] == 'EMEA')]
df4 = df1[(df1['GEO'] == 'APAC')]


# For Region NAmerica
pv = pd.pivot_table(df2, columns=['F_Qtr', 'F_Year'], index=["Parent_Expense_Type"], values=['Sum(Approved_Amount)'],
                    aggfunc=sum, fill_value=0)
r1 = pv.droplevel(0, axis=1)
r1.columns = [str(col[1]) + '/Q' + str(col[0]) for col in r1.columns.values]
print(r1)
a = r1.reset_index()

# below sort independently each column values
for col in a.columns:
    if col not in ['Parent_Expense_Type']:
        a[col] = sorted(a[col], reverse=True)

x = [col for col in a.columns if col not in ['Parent_Expense_Type']]
graph_values = a.drop(['Parent_Expense_Type'], axis=1)



# for region  EMEA
pv1 = pd.pivot_table(df3, columns=['F_Qtr', 'F_Year'], index=["Parent_Expense_Type"], values=['Sum(Approved_Amount)'],
                    aggfunc=sum, fill_value=0)
r11 = pv1.droplevel(0, axis=1)
r11.columns = [str(col[1]) + '/Q' + str(col[0]) for col in r11.columns.values]
# print(r11)
a1 = r11.reset_index()

# below sort independently each column values
for col in a1.columns:
    if col not in ['Parent_Expense_Type']:
        a1[col] = sorted(a1[col], reverse=True)

x1 = [col for col in a1.columns if col not in ['Parent_Expense_Type']]
graph_values1 = a1.drop(['Parent_Expense_Type'], axis=1)

# for Region APAC
pv2 = pd.pivot_table(df4, columns=['F_Qtr', 'F_Year'], index=["Parent_Expense_Type"], values=['Sum(Approved_Amount)'],
                    aggfunc=sum, fill_value=0)
r12 = pv2.droplevel(0, axis=1)
r12.columns = [str(col[1]) + '/Q' + str(col[0]) for col in r12.columns.values]
# print(r12)
a2 = r12.reset_index()

# below sort independently each column values
for col in a2.columns:
    if col not in ['Parent_Expense_Type']:
        a2[col] = sorted(a2[col], reverse=True)

x2 = [col for col in a2.columns if col not in ['Parent_Expense_Type']]
graph_values2 = a2.drop(['Parent_Expense_Type'], axis=1)


from plotly import graph_objects as go
data = {
    "model_1": list(graph_values[0:1].values.flatten()),
    "model_2": list(graph_values[1:2].values.flatten()),
    "model_3": list(graph_values[2:3].values.flatten()),
    "model_4": list(graph_values[3:4].values.flatten()),
    "model_5": list(graph_values[4:5].values.flatten()),

    "model_E1": list(graph_values1[0:1].values.flatten()),
    "model_E2": list(graph_values1[1:2].values.flatten()),
    "model_E3": list(graph_values1[2:3].values.flatten()),
    "model_E4": list(graph_values1[3:4].values.flatten()),
    "model_E5": list(graph_values1[4:5].values.flatten()),

    "model_A1": list(graph_values2[0:1].values.flatten()),
    "model_A2": list(graph_values2[1:2].values.flatten()),
    "model_A3": list(graph_values2[2:3].values.flatten()),
    "model_A4": list(graph_values2[3:4].values.flatten()),
    "model_A5": list(graph_values2[4:5].values.flatten()),

    "labels": x
}

fig = go.Figure(
    data=[

        go.Bar(
            # name="NAmerica",
            x=data["labels"],
            y=data["model_1"],
            offsetgroup=0,
        ),
        go.Bar(
            # name="Parent Expense 2",
            x=data["labels"],
            y=data["model_2"],
            offsetgroup=0,
            base=data["model_1"],
        ),
        go.Bar(
            # name="Parent Expense 3",
            x=data["labels"],
            y=data["model_3"],
            offsetgroup=0,
            base=[val1 + val2 for val1, val2 in zip(data["model_1"], data["model_2"])],
        ),
        go.Bar(
            # name="Parent Expense 4",
            x=data["labels"],
            y=data["model_4"],
            offsetgroup=0,
            base=[val1 + val2 + val3 for val1, val2, val3 in zip(data["model_1"], data["model_2"], data["model_3"])],
        ),
        go.Bar(
            # name="Parent Expense 5",
            x=data["labels"],
            y=data["model_5"],
            offsetgroup=0,
            base=[val1 + val2 + val3 + val4 for val1, val2, val3, val4 in
                  zip(data["model_1"], data["model_2"], data["model_3"], data["model_4"])],
            #             base=data["model_4"],
        ),

        go.Bar(
            # name="EMEA",
            x=data["labels"],
            y=data["model_E1"],
            offsetgroup=1,
        ),
        go.Bar(
            # name="Parent Expense 2",
            x=data["labels"],
            y=data["model_E2"],
            offsetgroup=1,
            base=data["model_E1"],
        ),
        go.Bar(
            # name="Parent Expense 3",
            x=data["labels"],
            y=data["model_E3"],
            offsetgroup=1,
            base=[val1 + val2 for val1, val2 in zip(data["model_E1"], data["model_E2"])],
        ),
        go.Bar(
            # name="Parent Expense 4",
            x=data["labels"],
            y=data["model_E4"],
            offsetgroup=1,
            base=[val1 + val2 + val3 for val1, val2, val3 in zip(data["model_E1"], data["model_E2"], data["model_E3"])],
        ),
        go.Bar(
            # name="Parent Expense 5",
            x=data["labels"],
            y=data["model_E5"],
            offsetgroup=1,
            base=[val1 + val2 + val3 + val4 for val1, val2, val3, val4 in
                  zip(data["model_E1"], data["model_E2"], data["model_E3"], data["model_E4"])],
        ),

        go.Bar(
            # name="APAC",
            x=data["labels"],
            y=data["model_A1"],
            offsetgroup=2,
        ),
        go.Bar(
            # name="Parent Expense 2",
            x=data["labels"],
            y=data["model_A2"],
            offsetgroup=2,
            base=data["model_A1"],
        ),
        go.Bar(
            # name="Parent Expense 3",
            x=data["labels"],
            y=data["model_A3"],
            offsetgroup=2,
            base=[val1 + val2 for val1, val2 in zip(data["model_A1"], data["model_A2"])],
        ),
        go.Bar(
            # name="Parent Expense 4",
            x=data["labels"],
            y=data["model_A4"],
            offsetgroup=2,
            base=[val1 + val2 + val3 for val1, val2, val3 in zip(data["model_A1"], data["model_A2"], data["model_A3"])],
        ),
        go.Bar(
            # name="Parent Expense 5",
            x=data["labels"],
            y=data["model_A5"],
            offsetgroup=2,
            base=[val1 + val2 + val3 + val4 for val1, val2, val3, val4 in
                  zip(data["model_A1"], data["model_A2"], data["model_A3"], data["model_A4"])],
        ),


    ],
    layout=go.Layout(
        title_text="<b>"+"Selected Parent Expense Types Trend Analysis"+"</br>",
        title_x=0.5,
        yaxis_title="Total Amount (USD)",
        xaxis_title="Fiscal Quarters",
        #hovermode=False,
    )
)



import plotly
plotly.offline.plot(fig, filename='C:/AIVER/Dash/TestResultsForVisual/Test_08/Test_08_2.html', auto_open=False)
fig.show()





