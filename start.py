import subprocess
import os
import tkinter,json
print(3)
window = tkinter.Tk()
window.title("Start")
window.geometry("400x400")
window.configure(bg="white")
with open('request/request.json', 'r') as f:
        request = json.load(f)
with open('request/request.json', 'r') as f:
        request = json.load(f)
def startintegrate():
    request["SID"] = input_text.get("1.0", "end-1c")
    request["file"] = input_text1.get("1.0", "end-1c")
    current_directory = os.getcwd()
    print(current_directory)

    script_path = os.path.join(current_directory, "integrate.py")
    with open('request/request.json', 'w') as f:
            json.dump(request,f,indent=4)
    subprocess.Popen(["python", script_path])

    
def read():
    current_directory = os.getcwd()
    print(current_directory)
    #request["SID"] = input_text.get("1.0", "end-1c")
    request["file"] = input_text2.get("1.0", "end-1c")
    with open('request/request.json', 'w') as f:
        json.dump(request,f,indent=4)
    script_path = os.path.join(current_directory, "read.py")
    subprocess.Popen(["python", script_path])
def readfully():
    current_directory = os.getcwd()
    print(current_directory)
    #request["SID"] = input_text.get("1.0", "end-1c")
    request["file"] = input_text2.get("1.0", "end-1c")
    with open('request/request.json', 'w') as f:
        json.dump(request,f,indent=4)
    script_path = os.path.join(current_directory, "READFULLFILEWITHOUTXLSX.py")
    subprocess.Popen(["python", script_path])
def close_window():
    window.destroy()
def sets():
    
    request["sets"] = not request["sets"]
    print(request["sets"])

    with open('request/request.json', 'w') as f:
        json.dump(request,f,indent=4)
seta = tkinter.Button(window, text=f"{request["sets"]}", command=sets)
seta.pack(pady=0)

integrate_button = tkinter.Button(window, text="calculate", command=startintegrate)
integrate_button.pack(pady=0)

close_button = tkinter.Button(window, text="Close", command=close_window)
close_button.pack(pady=0)

read_button = tkinter.Button(window, text="read", command=read)
read_button.pack(pady=0)

read_button = tkinter.Button(window, text="readfully", command=readfully)
read_button.pack(pady=0)

label = tkinter.Label(window, text="รหัสนักเรียน ที่อยากดูข้อมูล", bg="white")
label.pack(pady=0)
input_text = tkinter.Text(window, height=1, width=30)
input_text.pack(pady=0)
label = tkinter.Label(window, text="ชื่อไฟล์ที่อยากเเปลงข้อมูล ใน folder incsv (ปุ่ม calculate)", bg="white")
label.pack(pady=0)
input_text1 = tkinter.Text(window, height=1, width=30)
input_text1.pack(pady=0)
label = tkinter.Label(window, text="ชื่อไฟล์ที่อยากดู ใน folder store csv (ปุ่ม read , readfully)", bg="white")
label.pack(pady=0)
input_text2 = tkinter.Text(window, height=1, width=30)
input_text2.pack(pady=0)
window.mainloop()