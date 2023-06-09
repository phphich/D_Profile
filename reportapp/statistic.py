import datetime
from workapp.models import *
from baseapp.models import *
import pandas as pd

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
    dataFrameDiv = pd.DataFrame({'Division': listDivName, 'Count': listDivCountPersonnel}, columns=['Division', 'Count'])
    return dataFrameDiv

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
    dataFrameEdu = pd.DataFrame({'Level': educations, 'Count': educationCount}, columns=['Level', 'Count'])
    return dataFrameEdu

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
    dataFrameStatus = pd.DataFrame({'Status': statusName, 'Count': statusCount}, columns=['Status', 'Count'])
    return dataFrameStatus

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
    dataFrameGender = pd.DataFrame({'Gender': genderName, 'Count': genderCount}, columns=['Gender', 'Count'])
    return dataFrameGender
