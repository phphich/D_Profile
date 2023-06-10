import datetime
from workapp.models import *
from baseapp.models import *
import pandas as pd

def getBudgetType():
    budgetTypes = ['งบประมาณแผ่นดิน', 'งบประมาณรายได้', 'งบประมาณภายนอก', 'งบประมาณส่วนตัว', 'ไม่ใช้งบประมาณ']
    return budgetTypes

def getLeavetype():
    leaveTypes=["ลาป่วย","ลากิจส่วนตัว", "ลาพักผ่อนประจำปี","ลาคลอดบุตร","ลาไปช่วยเหลือภริยาที่คลอดบุตร","ลาอุปสมบทหรือการลาไปประกอบพิธีฮัจย์",
                "ลาเข้ารับการตรวจเลือกหรือเข้ารับการเตรียมพล","ลาไปศึกษา/ฝึกอบรม/ปฏิบัติการวิจัย/ดูงาน","ลาไปปฏิบัติงานในองค์กรระหว่างประเทศ",
                ]
    return leaveTypes

def getDivisionSet(division=None):
    if division is None:
        divisions = Division.objects.all()
    else:
        divisions = Division.objects.filter(id=division.id)
    listDivName = []
    listDivCountPersonnel = []
    for div in divisions:
        listDivName.append(div.name_th)
        listDivCountPersonnel.append(div.getCountPersonnel())
    dfDiv = pd.DataFrame({'Division': listDivName, 'Count': listDivCountPersonnel}, columns=['Division', 'Count'])
    return dfDiv

def getEducationSet(division=None):
    if division is None:
        personnels = Personnel.objects.all()
        levels = Education.objects.all().values('level').distinct()
    else:
        personnels = Personnel.objects.filter(division=division)
        levels = Education.objects.filter(personnel__division=division).values('level').distinct()
    educations = []  #ระดับการศึกษาแบบไม่ซ้ำ
    for l in levels:
        educations.append(l['level'])
    educations.append('ไม่ระบุ')

    educationSet = [] #เก็บวุฒิการศึกษาสูงสุดของแต่ละคน
    for personnel in personnels:
        educationSet.append(personnel.getHighestEducation())

    educationCount = []
    for education in educations:
        countlevel = educationSet.count(education)
        educationCount.append(countlevel)
    dfEdu = pd.DataFrame({'Level': educations, 'Count': educationCount}, columns=['Level', 'Count'])
    return dfEdu

def getStatusSet(division=None):
    # personnels = Personnel.objects.all()
    statuses = Personnel.objects.all().values('status').distinct().order_by('status')
    statusName = []
    statusCount = []
    for s in statuses:
        if division is None:
            count = Personnel.objects.filter(status=s['status']).count()
        else:
            count = Personnel.objects.filter(division=division, status=s['status']).count()
        statusName.append(s['status'])
        statusCount.append(count)
    dfStatus = pd.DataFrame({'Status': statusName, 'Count': statusCount}, columns=['Status', 'Count'])
    return dfStatus

def getGenderSet(division=None):
    # personnels = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th')
    if division is None:
        maleGender = Personnel.objects.filter(gender='ชาย').count()
        femaleGender = Personnel.objects.filter(gender='หญิง').count()
    else:
        maleGender = Personnel.objects.filter(division=division, gender='ชาย').count()
        femaleGender = Personnel.objects.filter(division=division, gender='หญิง').count()
    # genderSet = [maleGender, femaleGender]
    genderName = []
    genderCount = []
    genderName.append('ชาย')
    genderName.append('หญิง')
    genderCount.append(maleGender)
    genderCount.append(femaleGender)
    dfGender = pd.DataFrame({'Gender': genderName, 'Count': genderCount}, columns=['Gender', 'Count'])
    return dfGender

def getResearchFiscalYears():
    fiscalYearDatas = Research.objects.all().values('fiscalYear').distinct().order_by('-fiscalYear')
    fiscalYears = []  #ปีงบประมาณแบบไม่ซ้ำ
    for f in fiscalYearDatas:
        fiscalYears.append(f['fiscalYear'])
    return fiscalYears

def getResearchCountSet(budgetType, fiscalYearStart, fiscalYearEnd):

    # for i in range(fiscalYearStart, fiscalYearEnd+1):
    #     researchYear.append(i)

    if budgetType is None or budgetType == '0':  # เลือกทั้งหมด
        researchss = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('fiscalYear').annotate(count=Count('fiscalYear'))\
            .order_by('fiscalYear')
    else:
        researchss = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             budgetType=budgetType).values('fiscalYear').annotate(count=Count('fiscalYear'))\
            .order_by('fiscalYear')
    researchYear = []
    researchCount = []
    for research in researchss:
        researchYear.append(str(research['fiscalYear']))
        researchCount.append(research['count'])
    df = pd.DataFrame({'Year': researchYear, 'Count': researchCount}, columns=['Year', 'Count'])
    return df
