import datetime
from workapp.models import *
# from baseapp.models import *
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
        lastUpdate = datetime.datetime(y, 9, 30, 23, 59, 59) # สิ้นเดือนกันยายนของปีปัจจุบัน
    else:
        lastUpdate = datetime.datetime(y+1, 9, 30, 23, 59, 59) # สิ้นเดือนกันยายนของปีถัดไป
    today = datetime.datetime.now()
    if today < lastUpdate:
        return True
    else:
        return False
def getDecorationName_sh(fullname):
    dic_name_sh = {
        "เหรียญเงินมงกุฏไทย": "ร.ง.ม.",
        "เหรียญเงินช้างเผือก": "ร.ง.ช.",
        "เหรียญทองมงกุฏไทย": "ร.ท.ม.",
        "เหรียญทองช้างเผือก": "ร.ท.ช.",
        "เบญจมาภรณ์มงกุฏไทย": "บ.ม.",
        "เบญจมาภรณ์ช้างเผือก": "บ.ช.",
        "จัตุรถาภรณ์มงกุฏไทย": "จ.ม.",
        "จัตุรถาภรณ์ช้างเผือก": "จ.ช.",
        "ตริตาภรณ์มงกุฏไทย": "ต.ม.",
        "ตริตาภรณ์ช้างเผือก": "ต.ช.",
        "ทวีติยาภรณ์มงกุฏไทย": "ท.ม.",
        "ทวีติยาภรณ์ช้างเผือก": "ท.ช.",
        "ประถมาภรณ์มงกุฏไทย": "ป.ม.",
        "ประถมาภรณ์ช้างเผือก": "ป.ช.",
        "มหาวชิรมงกุฏ": "ม.ว.ม.",
        "มหาปรมาภรณ์ช้างเผือก": "ม.ป.ช.",
        "เหรียญจักรพรรดิมาลา": "ร.จ.พ.",
    }
    shortName = dic_name_sh.get(fullname)
    return shortName
# ********************* Check Permission ***************************/
def chkPermission(methodName, uType=None, uId=None, docType=None, docId=None):
    methodDenyStaff = ['facultyUpdate', 'divisionNew', 'divisionUpdate', 'divisionDelete',
                        'curriculumNew','curriculumUpdate','curriculumDelete', 'personnelDelete',
                       'managerDelete', 'headerDelete', 'responsibleList', 'responsibleDelete',
                    ] # method ที่ไม่อนุญาตสำหรับ Staff
    methodDenyManager =['userResetPassword', 'facultyUpdate', 'divisionNew', 'divisionUpdate', 'divisionDelete',
                        'curriculumNew','curriculumUpdate','curriculumDelete',
                        'personnelNew', 'personnelDelete',
                        'managerDelete', 'headerDelete',  'responsibleDelete', 'responsibleList',
                    ] # method ที่ไม่อนุญาตสำหรับ Manager
    methodDenyHeader = ['userResetPassword', 'facultyUpdate', 'divisionNew', 'divisionUpdate', 'divisionDelete',
                         'curriculumNew', 'curriculumUpdate', 'curriculumDelete',
                         'personnelNew', 'personnelDelete',
                         'managerDelete', 'headerDelete', 'responsibleDelete', #'responsibleList',
                         ]  # method ที่ไม่อนุญาตสำหรับ Header
    methodDenyPersonnel =['userResetPassword', 'facultyUpdate', 'divisionNew', 'divisionUpdate', 'divisionDelete',
                        'curriculumNew','curriculumUpdate','curriculumDelete',
                        'personnelNew', 'personnelDelete',
                         'managerDelete', 'headerDelete', 'responsibleDelete', #'responsibleList',
                    ] # method ที่ไม่อนุญาตสำหรับ Personnel
    # print('method: ' + methodName)
    # print('type: ' + uType)

    if uType == 'Administrator':
       return True
    elif uType == 'Staff' and methodName in methodDenyStaff:
        return False
    elif uType == 'Manager' and methodName in methodDenyManager:
        return False
    elif uType == 'Header' and methodName in methodDenyHeader:
        return False
    elif uType == 'Personnel' and methodName in methodDenyPersonnel:
        return False
    elif uType == 'Personnel': #ถ้าเป็น Personnel
        if str(methodName).find('New') != -1: #ถ้า New ทุกกรณี
            userDocIds = Personnel.objects.filter(id=uId).only('id')  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
        elif docType == 'Personnel':
            userDocIds = Personnel.objects.filter(id=uId).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
        elif docType == 'Education':
            userDocIds = Education.objects.filter(personnel_id=uId).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
        elif docType == 'Decoration':
            userDocIds = Decoration.objects.filter(personnel_id=uId).only('id')  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
        elif docType == 'Expertise':
            userDocIds = Expertise.objects.filter(personnel_id=uId).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
        elif docType == 'Leave': #เอกสารข้อมูลการลา ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            userDocIds = Leave.objects.filter(personnel_id=uId).only('id')
        elif docType == 'Training': #เอกสารข้อมูลการอบรม ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            userDocIds = Training.objects.filter(personnel_id=uId).only('id')
        elif docType == 'Performance': #เอกสารข้อมูลผลงาน ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            userDocIds = Performance.objects.filter(personnel_id=uId).only('id')
        elif docType == 'Research':  # เอกสารข้อมูลผลงาน ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            if str(methodName).find('Update') != -1 or str(methodName).find('Delete') != -1:
                userDocIds = Research.objects.filter(recorder_id=uId).only('id')
            else:
                userDocIds1 = Research.objects.filter(recorder_id=uId).only('id')
                userDocIds2 = Research.objects.filter(researchperson__personnel_id=uId).only('id')
                userDocIds = userDocIds1.union(userDocIds2)
        elif docType == 'SocialService':  # เอกสารข้อมูลผลงาน ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            if str(methodName).find('Update') != -1 or str(methodName).find('Delete') != -1:
                userDocIds = SocialService.objects.filter(recorder_id=uId).only('id')
            else:
                userDocIds1 = SocialService.objects.filter(recorder_id=uId).only('id')
                userDocIds2 = SocialService.objects.filter(socialserviceperson__personnel_id=uId).only('id')
                userDocIds = userDocIds1.union(userDocIds2)
        elif docType == 'Command':  # เอกสารข้อมูลผลงาน ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                if str(methodName).find('Update') != -1 or str(methodName).find('Delete') != -1:
                    userDocIds = Command.objects.filter(recorder_id=uId).only('id')
                else:
                    userDocIds1 = Command.objects.filter(recorder_id=uId).only('id')
                    userDocIds2 = Command.objects.filter(commandperson__personnel_id=uId).only('id')
                    userDocIds = userDocIds1.union(userDocIds2)
        else:
            userDocIds = None
    elif uType == 'Manager':
        personnel = Personnel.objects.get(id=uId)
        userDocIds = personnel.id  # กรณีเพิ่มเอกสารของตนเอง
        division = personnel.division
        personnels = division.getPersonnels()
        if str(methodName).find('New') != -1:
            if docId != userDocIds:
                return False
            else:
                return True
        elif str(methodName).find('List') != -1 or str(methodName).find('Detail') != -1:  # ดูข้อมูลได้ทุกคนทุกสาขา
            return True
        elif str(methodName).find('Update') != -1 or str(methodName).find(
                'Delete') != -1:  # ถ้าเรียกใช้ method ในการแก้ไขหรือลบต้องเป็นการทำกับข้อมูลของตัวเองเท่านั้น
            if docType == 'Personnel':
                userDocIds = Personnel.objects.filter(id=uId).only('id')  # เอกสาร Personnel ส่วนตัว ที่มีสิทธิ์เข้าถึงทั้งหมด
            elif docType == 'Education':
                userDocIds = Education.objects.filter(personnel_id=uId).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Decoration':
                userDocIds = Decoration.objects.filter(personnel_id=uId).only('id')  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Expertise':
                userDocIds = Expertise.objects.filter(personnel_id=uId).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Leave':
                userDocIds = Leave.objects.filter(personnel_id=uId).only('id')
            elif docType == 'Training':
                userDocIds = Training.objects.filter(personnel_id=uId).only('id')
            elif docType == 'Performance':
                userDocIds = Performance.objects.filter(personnel_id=uId).only('id')
            elif docType == 'Command':  # เอกสารข้อมูลผลงาน ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                if str(methodName).find('Update') != -1 or str(methodName).find('Delete') != -1:
                    userDocIds = Command.objects.filter(recorder_id=uId).only('id')
                else:
                    userDocIds1 = Command.objects.filter(recorder_id=uId).only('id')
                    userDocIds2 = Command.objects.filter(commandperson__personnel_id=uId).only('id')
                    userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'Research':  # เอกสารข้อมูลผลงาน ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                if str(methodName).find('Update') != -1 or str(methodName).find('Delete') != -1:
                    userDocIds = Research.objects.filter(recorder_id=uId).only('id')
                else:
                    userDocIds1 = Research.objects.filter(recorder_id=uId).only('id')
                    userDocIds2 = Research.objects.filter(researchperson__personnel_id=uId).only('id')
                    userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'SocialService':  # เอกสารข้อมูลผลงาน ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                if str(methodName).find('Update') != -1 or str(methodName).find('Delete') != -1:
                    userDocIds = SocialService.objects.filter(recorder_id=uId).only('id')
                else:
                    userDocIds1 = SocialService.objects.filter(recorder_id=uId).only('id')
                    userDocIds2 = SocialService.objects.filter(socialserviceperson__personnel_id=uId).only('id')
                    userDocIds = userDocIds1.union(userDocIds2)
            else:
                userDocIds = None
    elif uType == 'Header':
        personnel = Personnel.objects.get(id=uId)
        userDocIds = personnel.id #กรณีเพิ่มเอกสารของตนเอง
        division = personnel.division
        personnels = division.getPersonnels()
        if str(methodName).find('New') != -1 :
            if docId == userDocIds:
                return True
            else:
                return False
        elif str(methodName).find('List') != -1 or str(methodName).find('Detail') != -1: # ดูข้อมูลได้ทุกคนในสาขา
            if docType == 'Personnel':
                userDocIds = Personnel.objects.filter(id__in=personnels) # เอกสาร Personnel ส่วนตัว ที่มีสิทธิ์เข้าถึงทั้งหมด
            elif docType == 'Education':
                userDocIds = Education.objects.filter(personnel__in=personnels).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Decoration':
                userDocIds = Decoration.objects.filter(personnel_id=uId).only('id')  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Expertise':
                userDocIds = Expertise.objects.filter(personnel__in=personnels).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Leave':
                userDocIds = Leave.objects.filter(personnel__in=personnels).only('id')
            elif docType == 'Training':
                userDocIds = Training.objects.filter(personnel__in=personnels).only('id')
            elif docType == 'Performance':
                userDocIds = Performance.objects.filter(personnel__in=personnels).only('id')
            elif docType == 'Command':
                userDocIds1 = Command.objects.filter(recorder__in=personnels).only('id')
                userDocIds2 = Command.objects.filter(commandperson__personnel__in=personnels).only('id')
                userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'Research':
                userDocIds1 = Research.objects.filter(recorder__in=personnels).only('id')
                userDocIds2 = Research.objects.filter(researchperson__personnel__in=personnels).only('id')
                userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'SocialService':
                userDocIds1 = SocialService.objects.filter(recorder__in=personnels).only('id')
                userDocIds2 = SocialService.objects.filter(socialserviceperson__personnel__in=personnels).only('id')
                userDocIds = userDocIds1.union(userDocIds2)
            else:
                userDocIds = None
        elif str(methodName).find('Update') != -1 or str(methodName).find('Delete') != -1:
            # ถ้าเรียกใช้ method ในการแก้ไขหรือลบต้องเป็นการทำกับข้อมูลของตัวเองเท่านั้น
            if docType == 'Personnel':
                userDocIds = Personnel.objects.filter(id=uId).only('id')  # เอกสาร Personnel ส่วนตัว ที่มีสิทธิ์เข้าถึงทั้งหมด
            elif docType == 'Education':
                userDocIds = Education.objects.filter(personnel_id=uId).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Decoration':
                userDocIds = Decoration.objects.filter(personnel_id=uId).only('id')  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Expertise':
                userDocIds = Expertise.objects.filter(personnel_id=uId).only('id')  #เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
            elif docType == 'Leave':
                userDocIds = Leave.objects.filter(personnel_id=uId).only('id')
            elif docType == 'Training':
                userDocIds = Training.objects.filter(personnel_id=uId).only('id')
            elif docType == 'Performance':
                userDocIds = Performance.objects.filter(personnel_id=uId).only('id')
            elif docType == 'Command':
                userDocIds = Command.objects.filter(recorder=personnel).only('id')
            elif docType == 'Research':
                userDocIds = Command.objects.filter(recorder=personnel).only('id')
            elif docType == 'SocialService':
                userDocIds = Command.objects.filter(recorder=personnel).only('id')
            else:
                userDocIds = None
    elif uType == 'Staff':
        # ถ้าเป็น List หรือ Detail เข้าดูบุคลากรได้ตามที่ได้รับมอบหมายหน้าที่
        personnel = Personnel.objects.get(id=uId)
        userDocIds = personnel.id #เพิ่มเอกสารใดๆ ของตนเอง
        divisions = personnel.getDivisionResponsible()
        personnel=[personnel]
        personnels = Personnel.objects.filter(division_id__in =divisions)
        if str(methodName).find('personnelNew') != -1:
            return True
        elif str(methodName).find('New') != -1:
            if docId == userDocIds:
                return True
            else:
                userDocIds=Personnel.objects.filter(id__in=personnels).only('id')  # เอกสารข้อมูลบุคลากรทุกคน ที่ได้รับสิทธิื์ให้เข้าถึงได้
        else: #Update and Delete
            if docType == 'Personnel':
                userDocIds=Personnel.objects.filter(Q(id__in=personnels) or Q(personnel_id=uId))  # เอกสารข้อมูลบุคลากรทุกคน ที่ได้รับสิทธิื์ให้เข้าถึงได้
            elif docType == 'Education':
                userDocIds1 = Education.objects.filter(personnel__in=personnels)  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                userDocIds2 = Education.objects.filter(personnel__in=personnel)  # เอกสารข้อมูลส่วนตัว
                userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'Decoration':
                userDocIds1 = Decoration.objects.filter(personnel__in=personnels)  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                userDocIds2 = Decoration.objects.filter(personnel__in=personnel)  # เอกสารข้อมูลส่วนตัว
                userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'Expertise':
                userDocIds1 = Expertise.objects.filter(personnel__in=personnels)  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                userDocIds2 = Expertise.objects.filter(personnel__in=personnel)  # เอกสารข้อมูลส่วนตัว
                userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'Leave':
                userDocIds1 = Leave.objects.filter(personnel__in=personnels)  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                userDocIds2 = Leave.objects.filter(personnel__in=personnel)  # เอกสารข้อมูลส่วนตัว
                userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'Training':
                userDocIds1 = Training.objects.filter(personnel__in=personnels)  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                userDocIds2 = Training.objects.filter(personnel__in=personnel)  # เอกสารข้อมูลส่วนตัว
                userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'Performance':
                userDocIds1 = Performance.objects.filter(personnel__in=personnels)  # เอกสารข้อมูลส่วนตัว ที่มีสิทธิ์เข้าถึงของตัวเองทั้งหมด
                userDocIds2 = Performance.objects.filter(personnel__in=personnel)  # เอกสารข้อมูลส่วนตัว
                userDocIds = userDocIds1.union(userDocIds2)
            elif docType == 'Command':
                if str(methodName).find('Detail') != -1:
                    return True
                userDocIds = Command.objects.filter(recorder__in=personnel)  # เอกสารทั้งหมดในระบบ Staff มองเห็นได้หมด
            elif docType == 'Research':
                if str(methodName).find('Detail') != -1:
                    return True
                userDocIds = Research.objects.filter(recorder__in=personnel)  # เอกสารทั้งหมดในระบบ Staff มองเห็นได้หมด
            elif docType == 'SocialService':
                if str(methodName).find('Detail') != -1:
                    return True
                userDocIds = SocialService.objects.filter(recorder__in=personnel)  # เอกสารทั้งหมดในระบบ Staff มองเห็นได้หมด
            else:
                userDocIds = None

    uDocId = []
    # print("docId: {}, uId: {}".format(docId, uId))
    if int(docId) == int(uId):
        return True
    for x in userDocIds:
        uDocId.append(int(x.id))
    if int(docId) not in uDocId:
        return False
    else:
        return True


