# Network-Device-Data-Collection-Script
 เป็นโปรแกรมที่ใช้ Python ในการเก็บ running config หรือสถานะของอุปกรณ์ต่างๆ ผ่านการ SSH, Telnet, Serial โดยจะสามารถบันทึกผลลัพธ์เป็นรูปภาพ หรือ txt ก็ได้ 

โดยคำสั่งที่จะส่งไปบนอุปกรณ์สามารถเลือกได้ หรือสามารถแก้ไขได้ในโฟเดอร์ command_template 
## บน Window สามารถรันไฟล์ exe ได้เลย
บน window จะต้อง clone ทั้ง git นี้ไปไว้ในโฟเดอร์เดียวกัน แล้วจากนั้นรันไฟล์ `NetCollector.exe` ได้เลย
## ถ้าหากต้องการ Debug หรือ Dev เพิ่มเติมแนะนำให้ใช้ Python Virtual Environment 

### Windows 
```
python -m venv .\.venv
.venv\Scripts\activate
pip install -r requirement.txt
```
### คำสั่ง deactivate
```
deactivate
```

### Mac, Linux ที่ใช้ Python3
คำส่งเหล้านี้ต้องรันโดยการเปิด terminal โดยจะต้องเป็น path เดียวกับโปรแกรม
```
python3 -m venv ./.venv
source .venv/bin/activate
python3 -m pip install -r requirement.txt  
```

## เริ่มการทำงานของโปรแกรมให้ใช้คำสั่ง 
## Windows 
```
python start.py
```
## Mac, Linux
```
python3 start.py
```
