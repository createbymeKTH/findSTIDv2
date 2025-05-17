import pandas as pd
import os,json
from scipy import stats
import numpy as np
with open('integrateconfig.json', 'r') as f:
    integrateconfig = json.load(f)
startcount = integrateconfig['startcountdf']
numberofsubject = len(integrateconfig['subjects'])
sub = integrateconfig['subjects']
outputfilename = integrateconfig['outputfilename']
setting = integrateconfig['setting']
if integrateconfig['read'] == 'yes':
    whatdoyouwanttoread = os.listdir('incsv')
    get = input("ลำดับที่ต้องการอ่าน (ใส่เป็นจำนวนนับ): ")
    print(f"คุณเลือกไฟล์ที่ {whatdoyouwanttoread[int(get) - 1]}")
    df = pd.read_csv(f'incsv/{whatdoyouwanttoread[int(get) - 1]}')
else:
    df = pd.read_csv(f'incsv/{os.listdir('incsv')[len(os.listdir("incsv")) - 1]}')
dfvalues = df.values
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
for i, subd in enumerate(sub):
    for index, ppl in enumerate(dfvalues):
        row = {
            'Id': ppl[0],
            'Name': ppl[1]}
        if setting["xi"]:
            row[f'xi {subd["name"]}'] = subjectopoit[i][index]
        if setting["xipercent"]:
            row[f'xipercent {subd["name"]}'] = subjectopoit[i][index]/subd["max"]*100
        if setting["percentile"]:
            row[f'percentile {subd["name"]}'] = percentilestore[i][index]
        if setting["zscore"]:
            row[f'zscore {subd["name"]}'] = zscorestore[i][index]
        data.append(row)
print(len(data))
print(totalpoint)
totalmax = 0
for subd in sub:
    totalmax += subd["max"]
totalpointpercent = (totalpoint/totalmax)*100

for index,dt in enumerate(data):
    if index <= len(data)/numberofsubject - 1:
        if setting["totalpoint"]:
            dt["totalpoint"] = totalpoint[index]
        if setting["totalpoint percent"]:
            dt["totalpoint percent"] = totalpointpercent[index]
        if setting["total percentile"]:
            datas = totalpoint
            mu = np.mean(datas)
            sigma = np.std(datas)
            z = (totalpoint[index] - mu) / sigma
            dt["total percentile"] = stats.norm.cdf(z)
        if setting["totalzscore"]:
            datas = totalpoint
            mu = np.mean(datas)
            sigma = np.std(datas)
            z = (totalpoint[index] - mu) / sigma
            dt["total z score"] = z
df = pd.DataFrame(data)
df_clean = df.groupby(['Id', 'Name'], as_index=False).first()
df_clean= df_clean.sort_values(by='totalpoint', ascending=False)
df_clean.to_csv(f'outcsv/{outputfilename}.csv', index=False)

SD = np.std(totalpoint)
mean = np.mean(totalpoint)
maximum = np.max(totalpoint)
minimum = np.min(totalpoint)
mode = stats.mode(totalpoint)
xbar = np.sum(totalpoint) / len(totalpoint)
data = []
for index,i in enumerate(subjectopoit):
    row = {
            "subject": sub[index]["name"],
            "Mean":np.mean(i),
            "Standard Deviation":np.std(i),
            "Maximum":np.max(i),
            "Minimum":np.min(i),
            "mode":stats.mode(i),
            "Xbar":np.sum(i) / len(i)
            }
    print(f"Mean:{np.mean(i)}")
    print(f"Standard Deviation:{np.std(i)}")
    print(f"Maximum:{np.max(i)}")
    print(f"Minimum:{np.min(i)}")
    print(f"Mode:{stats.mode(i)}")
    print(f"Xbar:{np.sum(i) / len(i)}")
    
    data.append(row)
data.append({"subject": "ALLSUBJECT",
             f"Standard Deviation": SD,
             f"Mean": mean,
             f"Maximum": maximum,
             f"Minimum": minimum,
             f"mode": mode,
             f"Xbar": xbar})
df = pd.DataFrame(data)
df.to_csv(f'outcsv/SDMODERANGEXBARMAXIMUMMINIMUM.csv', index=False)


print(f"Standard Deviation: {SD}")
print(f"Mean: {mean}")
print(f"Maximum: {maximum}")
print(f"Minimum: {minimum}")
print(f"Mode: {mode}")
print(f"Xbar: {xbar}")
