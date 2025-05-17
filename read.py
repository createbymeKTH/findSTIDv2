import pandas as pd
import os,json
with open('config.json', 'r') as f:
    config = json.load(f)

if config['read'] == 'yes':
    whatdoyouwanttoread = os.listdir('store csv')
    get = input("ลำดับที่ต้องการอ่าน (ใส่เป็นจำนวนนับ): ")
    print(f"คุณเลือกไฟล์ที่ {whatdoyouwanttoread[int(get) - 1]}")
    df = pd.read_csv(f'store csv/{whatdoyouwanttoread[int(get) - 1]}')
else:
    df = pd.read_csv(f'store csv/{os.listdir('store csv')[len(os.listdir("store csv")) - 1]}')


get = int(input("ใส่รหัสนักเรียน: "))
if (df.iloc[:, 0] == get).any():
    matches = df[df.iloc[:, 0] == get]
    print(matches)
else:
    print("ไม่พบรหัสนักเรียนนี้ในไฟล์")