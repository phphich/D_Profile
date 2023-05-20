import datetime

# ฟังก์ชันสำหรับตัดอักขระจากชื่อไฟล์ที่ระบบไม่รองรับ
def fileNameCleansing(filename):
    find = [' ', '+', '%', '#','$','@','!', '^','&','*',',',
            'ั', '่','้','๊','๋','์',
            'ิ','ี','ึ', 'ื','ุ','ู',
            '(',')','[',']','{','}',
            ]
    for f in find:
        if f == ' ':
            filename = filename.replace(f, '_')
        else:
            filename = filename.replace(f, '')
    return filename

# ฟังก์ชันสำหรับอ่านปีงบประมาณปัจจุบัน
def getCurrentFiscalYear():
    today = datetime.date.today()
    fiscalYear = today.year
    if today.year < 2500:
        fiscalYear += 543
    month = today.month
    if month > 8:
        fiscalYear += 1
    return  fiscalYear

# ฟังก์ชันสำหรับอ่านปีการศึกษาปัจจุบัน
def getCurrentEduYear():
    today = datetime.date.today()
    eduYear = today.year
    if today.year < 2500:
        eduYear += 543
    month = today.month
    if month < 6:
        eduYear -= 1
    return eduYear

# ฟังก์ชันสำหรับอ่านภาคเรียนัจจุบัน
def getCurrentEduSemeter():
    month = datetime.date.today().month
    if month in [6,7,8,9,10]:
        eduSemeter = "1"
    elif month in [11,12,1,2,3]:
        eduSemeter = "2"
    else:
        eduSemeter = "ฤดูร้อน"
    return eduSemeter

# ฟังก์ชันสำหรับอ่านวันที่ปัจจุบันและเปลี่ยน คศ. เป็น พศ.
def getCurrentDate():
    today = datetime.date.today()
    m = str.zfill(str(today.month),2)
    d = str.zfill(str(today.day),2)
    y = today.year
    if today.year < 2500:
        y += 543
    y=str(y)
    currentDay = y + "-" + m + "-" + d
    return currentDay





