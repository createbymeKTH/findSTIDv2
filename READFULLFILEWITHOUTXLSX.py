import pandas as pd
import os,json
import matplotlib.pyplot as plt
import numpy as np
with open('config/config.json', 'r') as f:
    config = json.load(f)
with open('request/request.json', 'r') as f:
    request = json.load(f)
print(request['sets'])
if config['read'] == 'yes' and not request['sets']:
    whatdoyouwanttoread = os.listdir('store csv')
    get = input("ลำดับที่ต้องการอ่าน (ใส่เป็นจำนวนนับ): ")
    print(f"คุณเลือกไฟล์ที่ {whatdoyouwanttoread[int(get) - 1]}")
    df = pd.read_csv(f'store csv/{whatdoyouwanttoread[int(get) - 1]}')
    get = int(input("ใส่รหัสนักเรียน: "))
else:
    df = pd.read_csv(rf'{request['file']}')
    try:
        get = int(request['SID'])
    except:
        print("Invalid SID, please enter a valid number.")
print(df)
names = df.iloc[:, 0].tolist()
values = df.iloc[:, config["startvalue"]-1:].values
plt.figure("Matrix Plot with Values", figsize=(8, 6))
im = plt.imshow(values, cmap='YlOrRd', aspect='auto')
plt.colorbar(im, label="Value")
plt.xticks(
    ticks=np.arange(values.shape[1]), 
    labels=df.columns[config["startvalue"]-1:], 
    fontsize=8, 
    rotation=45, 
    ha='right'
)
plt.yticks(
    ticks=np.arange(len(names)), 
    labels=names, 
    fontsize=8
)
plt.title("Students vs Subjects", fontsize=10)
plt.xlabel("Subject", fontsize=9)
plt.ylabel("Student", fontsize=9)
for i in range(values.shape[0]):
    for j in range(values.shape[1]):
        plt.text(j, i, str(str(values[i, j])), ha='center', va='center', color='black', fontsize=7)
plt.tight_layout()
plt.show()