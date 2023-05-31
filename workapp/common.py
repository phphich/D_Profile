import datetime
from workapp.models import *
from django.contrib.auth.models import User, Group


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

def chkUpdateTime(documentDate): #ฟังก์ชันตรวจสอบวันสุดท้ายของการแก้ไขเอกสาร เทียบกับวันปัจจุบัน ว่าสามารถแก้ไขได้อยู่หรือไม่
    m= documentDate.month
    y = documentDate.year
    if m <= 8:
        lastUpdate = datetime.datetime(y, 8, 31, 23, 59, 59) # สิ้นเดือนสิงหาคมของปีปัจจุบัน
    else:
        lastUpdate = datetime.datetime(y+1, 8, 31, 23, 59, 59) # สิ้นเดือนสิงหาคมของปีถัดไป
    today = datetime.datetime.now()
    if today < lastUpdate:
        print(True)
        return True
    else:
        print(False)
        return False

def chkPermission(methodName, uType=None, uId=None, docType=None, docId=None):
    methodDenyStaff = ['facultyUpdate', 'divisionNew', 'divisionUpdate', 'divisionDelete',
                        'curriculumNew','curriculumUpdate','curriculumDelete',
                    ]
    methodDenyManager =['facultyUpdate', 'divisionNew', 'divisionUpdate', 'divisionDelete',
                        'curriculumNew','curriculumUpdate','curriculumDelete',
                        'personnelNew', 'personnelDelete',
                    ]
    methodDenyPersonnel =['facultyUpdate', 'divisionNew', 'divisionUpdate', 'divisionDelete',
                        'curriculumNew','curriculumUpdate','curriculumDelete',
                        'personnelNew', 'personnelDelete',
                    ]
    print('method: ' + methodName)
    print('type: ' + uType)
    if uType == 'Administrator':
       return True
    elif uType == 'Staff' and methodName in methodDenyStaff:
        return False
    elif uType == 'Manager' and methodName in methodDenyManager:
        return False
    elif uType == 'Personnel' and methodName in methodDenyPersonnel:
        return False
    elif uType == 'Personnel':
        # if str(methodName).find('Update') != -1:
        if docType == 'Personnel':
            userDocIds = Personnel.objects.filter(id=uId).only('id')
            if docId in userDocIds:
                return True
            else:
                return False
        elif docType == 'Leave':
            userDocIds = Leave.objects.filter(personnel_id=uId).only('id')
            if docId in userDocIds:
                return True
            else:
                return False
        elif docType == 'Training':
            userDocIds = Training.objects.filter(personnel_id=uId).only('id')
            if docId in userDocIds:
                return True
            else:
                return False
        elif docType == 'Performance':
            userDocIds = Performance.objects.filter(personnel_id=uId).only('id')
            if docId in userDocIds:
                return True
            else:
                return False
        else:
            return False
    elif uType == 'Manager':
        return True












