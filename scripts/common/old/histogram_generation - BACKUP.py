import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('C:/AIVER/Results/TEST_01/OR_1_1_4.csv')
data['Per_Attendee_Amount'] = data['Per_Attendee_Amount'].replace('[\$,]', '', regex=True).astype(float)

per_attendee_amount = data['Per_Attendee_Amount']

# Histogram
plt.rcParams.update({'font.size': 10})
plt.figure(figsize=(10, 5))
title_font = {'size': '14', 'color': 'black', 'fontweight': 'bold'}
axis_font = {'size': '12', 'fontweight': 'bold'}
n1, bins1, patches1 = plt.hist(per_attendee_amount, bins=[0, 100, 500, 1000, 10000], edgecolor='black', linewidth=1.2)

# To display bin values
nseries = pd.Series(n1)
for index, v in enumerate(n1):
    i = 0
    i = i + bins1[index]
    if i > 0:
        plt.autoscale(enable=True, axis='x', tight=True)  # use axis='x' to only set the x axis tight
        plt.plot([0, i], [int(v), int(v)], color='k',linewidth=0.5)
    i = i + 50
    

plt.xticks([100, 500, 1000, 10000])

plt.title("Frequency Distribution Per Attendee Amount", **title_font)
plt.xlabel("Per Attendee Amount (USD)", **axis_font)
plt.ylabel("Frequency Count", **axis_font)
# FIXME: In HTML, Local Project Path is referred as "<img width="400" height="390" src="/AIVER/visualization/test_01/histo_4bins_wf.png">"
plt.savefig('C:/AIVER/Dash/TestResultsForVisual/Test_01/histo_4bins_wf.png')
# plt.show()

plt.rcParams.update({'font.size': 10})
plt.figure(figsize=(10, 5))
title_font = {'size': '14', 'color': 'black', 'fontweight': 'bold'}
axis_font = {'size': '12', 'fontweight': 'bold'}
n, bins, patches = plt.hist(per_attendee_amount, range=(0, 500), edgecolor='black', linewidth=1.2, color='orange')

# To display bin values
n_series = pd.Series(n)
i = 100
for v in enumerate(n_series):
    if int(v[1]) > 0:
        plt.autoscale(enable=True, axis='x', tight=True)  # use axis='x' to only set the x axis tight
        plt.plot([0, i], [int(v[1]), int(v[1])], color='k',linewidth=0.5)
        plt.xlim(75)
        i = i + 50
plt.xticks([100,150,200,250,300,350,400,450,500])
plt.title("Frequency Distribution Per Attendee Amount less than $500", **title_font)
plt.xlabel("Per Attendee Amount (USD)", **axis_font)
plt.ylabel("Frequency Count", **axis_font)
# FIXME: In HTML, Local Project Path is referred as "<img width="400" height="390" src="/AIVER/visualization/test_01/hist_0_500_wf.png">"
plt.savefig('C:/AIVER/Dash/TestResultsForVisual/Test_01/hist_0_500_wf.png')
# plt.show()

