import pandas as pd
import os,json
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
with open('integrateconfig.json', 'r') as f:
    integrateconfig = json.load(f)
with open('request/request.json', 'r') as f:
    request = json.load(f)
startcount = integrateconfig['startcountdf']
numberofsubject = len(integrateconfig['subjects'])
sub = integrateconfig['subjects']
outputfilename = integrateconfig['outputfilename']
setting = integrateconfig['setting']
setudentID = setting['studentID']
studentname = setting['studentname']
studentclass = setting['studentclass']
if integrateconfig['read'] == 'yes' and not request['sets']:
    whatdoyouwanttoread = os.listdir('incsv')
    get = input("ลำดับที่ต้องการอ่าน (ใส่เป็นจำนวนนับ): ")
    print(f"คุณเลือกไฟล์ที่ {whatdoyouwanttoread[int(get) - 1]}")
    df = pd.read_csv(f'incsv/{whatdoyouwanttoread[int(get) - 1]}')
else:
    print(request['file'])
    df = pd.read_csv(f'incsv/{request['file']}.csv')
dfvalues = df.values
print(dfvalues)
subjectopoit = []
for i in range(0, numberofsubject):
    subsubjectpoit = []
    for name in dfvalues:
        value = name[[startcount-1+i]]
        subsubjectpoit.append(value)
    subjectopoit.append(subsubjectpoit)

subjectopoit = [[int(x[0]) for x in row] for row in subjectopoit]
print(subjectopoit)
percentilestore = []
zscorestore = []
for subject in subjectopoit:
    storesubject = []
    zs = []
    for xi in subject:
        data = subject
        mu = np.mean(data)
        sigma = np.std(data)
        z = (xi - mu) / sigma
        zs.append(z)
        percentile = stats.norm.cdf(z)
        print("Percentile =", percentile * 100, "%")          
        storesubject.append(percentile * 100)
    percentilestore.append(storesubject)
    zscorestore.append(zs)

data = []
totalpoint = np.sum(np.array(subjectopoit),axis=0)
todatacsv = []
todatarow = {}
for i, subd in enumerate(sub):
    jectname = subd["name"]
    todatarow[jectname] = []
    for index, ppl in enumerate(dfvalues):
        print(subd)
        row = {}
        
        if setudentID["show"]:
            row['Id'] = ppl[setudentID["column"]-1]
        if studentclass["show"]:
            row['Class'] = ppl[studentclass["column"]-1]
        if studentname["show"]:
            row['Name'] = ppl[studentname["column"]-1]
        if setting["xi"]:
            row[f'xi {subd["name"]}'] = np.round(subjectopoit[i][index],2)
        if setting["ximax"]:
            row[f'ximax {subd["name"]}'] = np.round(subd["max"],2)
        if setting["xipercent"]:
            row[f'xipercent {subd["name"]}'] = np.round(subjectopoit[i][index]/subd["max"]*100,2)
        if setting["percentile"]:
            row[f'percentile {subd["name"]}'] = np.round(percentilestore[i][index],2)
        if setting["zscore"]:
            row[f'zscore {subd["name"]}'] = np.round(zscorestore[i][index],2)
        data.append(row)
        todatarow[jectname].append(np.round(subjectopoit[i][index],2))
print(len(data))
print(totalpoint)
print(todatarow)
totalmax = 0
for subd in sub:
    totalmax += subd["max"]
totalpointpercent = (totalpoint/totalmax)*100

for index,dt in enumerate(data):
    if index <= len(data)/numberofsubject - 1:
        if setting["totalpoint"]:
            dt["totalpoint"] = np.round(totalpoint[index],2)
        if setting["totalmax"]:
            dt["totalmax"] = np.round(totalmax,2)
        if setting["totalpoint percent"]:
            dt["totalpoint percent"] = np.round(totalpointpercent[index],2)
        if setting["total percentile"]:
            datas = totalpoint
            mu = np.mean(datas)
            sigma = np.std(datas)
            z = (totalpoint[index] - mu) / sigma
            dt["total percentile"] = np.round(stats.norm.cdf(z),2)
        if setting["totalzscore"]:
            datas = totalpoint
            mu = np.mean(datas)
            sigma = np.std(datas)
            z = (totalpoint[index] - mu) / sigma
            dt["total z score"] = np.round(z,2)
df = pd.DataFrame(data)
df_clean = df.groupby(['Id', 'Name'], as_index=False).first()
df_clean= df_clean.sort_values(by='totalpoint', ascending=False)
df_clean.to_csv(f'store csv/{outputfilename}.csv', index=False)

SD = np.std(totalpoint)
mean = np.mean(totalpoint)
maximum = np.max(totalpoint)
minimum = np.min(totalpoint)
mode = stats.mode(totalpoint)[0]
modeamount = stats.mode(totalpoint)[1]
xbar = np.sum(totalpoint) / len(totalpoint)
data = []
for index,i in enumerate(subjectopoit):
    row = {
            "subject": sub[index]["name"],
            "Mean":np.round(np.mean(i),2),
            "Standard Deviation":np.round(np.std(i),2),
            "Maximum":np.round(np.max(i),2),
            "Minimum":np.round(np.min(i),2),
            "mode":stats.mode(i)[0],
            "mode amount":stats.mode(i)[1],
            "Xbar":np.round(np.sum(i) / len(i),2)
            }
    print(f"Mean:{np.mean(i)}")
    print(f"Standard Deviation:{np.std(i)}")
    print(f"Maximum:{np.max(i)}")
    print(f"Minimum:{np.min(i)}")
    print(f"Mode:{stats.mode(i)}")
    print(f"Xbar:{np.round(np.sum(i) / len(i),2)}")
    
    data.append(row)
data.append({"subject": "ALLSUBJECT",
             f"Standard Deviation": np.round(SD,2),
             f"Mean": mean,
             f"Maximum": maximum,
             f"Minimum": minimum,
             f"mode": mode,
            f"mode amount": modeamount,
             f"Xbar": np.round(xbar,2)})
df = pd.DataFrame(data)
df.to_csv(f'outcsv/SDMODERANGEXBARMAXIMUMMINIMUM.csv', index=False)

print(f"Standard Deviation: {SD}")
print(f"Mean: {mean}")
print(f"Maximum: {maximum}")
print(f"Minimum: {minimum}")
print(f"Mode: {mode}")
print(f"Xbar: {xbar}")
df = df = pd.DataFrame(todatarow)
df.to_csv(f'outcsv/data.csv', index=False)
dff = pd.read_csv(f'outcsv/data.csv')
df = pd.read_csv("outcsv/SDMODERANGEXBARMAXIMUMMINIMUM.csv")
print(df)
names = df.iloc[:, 0].tolist()
values = df.iloc[:, 1:].values
plt.figure("Matrix Plot with Values", figsize=(8, 6))
im = plt.imshow(values, cmap='YlOrRd', aspect='auto')
plt.colorbar(im, label="Value")
plt.xticks(
    ticks=np.arange(values.shape[1]), 
    labels=df.columns[1:], 
    fontsize=8, 
    rotation=45, 
    ha='right'
)
plt.yticks(
    ticks=np.arange(len(names)), 
    labels=names, 
    fontsize=8
)
plt.title("People vs Features", fontsize=10)
plt.xlabel("Feature", fontsize=9)
plt.ylabel("Person", fontsize=9)
for i in range(values.shape[0]):
    for j in range(values.shape[1]):
        plt.text(j, i, str(np.round(values[i, j],2)), ha='center', va='center', color='black', fontsize=7)
df = pd.DataFrame(dff)
for i,subject in enumerate(df.columns):
    plt.figure(subject)
    plt.hist(df[subject], bins=range(0, 101, 5), color='skyblue', edgecolor='black')
    plt.title(f"Histogram of {subject} Scores")
    plt.xlabel("Score")
    plt.ylabel("Number of Students")
    plt.xticks(range(0, 101, 5))
    plt.xlim(0, sub[i]["max"])
plt.tight_layout()
plt.show()
