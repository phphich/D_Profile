import datetime
from workapp.models import *
from baseapp.models import *
import pandas as pd

def getBudgetType():
    budgetTypes = ['งบประมาณแผ่นดิน', 'งบประมาณรายได้', 'งบประมาณภายนอก', 'งบประมาณส่วนตัว', 'ไม่ใช้งบประมาณ']
    return budgetTypes

def getMission():
    missions = ['การจัดการเรียนการสอน', 'การวิจัย', 'การบริการทางวิชาการแก่สังคม', 'การทำนุบำรุงศิลปวัฒนธรรม',
                'สนองโครงการอันเนื่องมาจากพระราชดำริ', 'งานอื่น ๆ ที่ได้รับมอบหมาย',
                ]
    return missions

def getLeavetype():
    leaveTypes=["ลาป่วย","ลากิจส่วนตัว", "ลาพักผ่อนประจำปี","ลาคลอดบุตร","ลาไปช่วยเหลือภริยาที่คลอดบุตร","ลาอุปสมบทหรือการลาไปประกอบพิธีฮัจย์",
                "ลาเข้ารับการตรวจเลือกหรือเข้ารับการเตรียมพล","ลาไปศึกษา/ฝึกอบรม/ปฏิบัติการวิจัย/ดูงาน","ลาไปปฏิบัติงานในองค์กรระหว่างประเทศ",
                ]
    return leaveTypes

# *********************** Personnel **********************
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

# *********************** Research ************************
def getResearchFiscalYears():
    fiscalYearDatas = Research.objects.all().values('fiscalYear').distinct().order_by('fiscalYear')
    fiscalYears = []  #ปีงบประมาณแบบไม่ซ้ำ
    for f in fiscalYearDatas:
        fiscalYears.append(f['fiscalYear'])
    return fiscalYears

def getResearchCountSet(budgetType, fiscalYearStart, fiscalYearEnd):
    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
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
    dfResearchCount = pd.DataFrame({'Year': researchYear, 'Count': researchCount}, columns=['Year', 'Count'])
    return dfResearchCount

def getResearchBudgetSet(budgetType, fiscalYearStart, fiscalYearEnd):
    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        researchss = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('fiscalYear').annotate(sum=Sum('budget'))\
            .order_by('fiscalYear')
    else:
        researchss = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             budgetType=budgetType).values('fiscalYear').annotate(sum=Sum('budget'))\
            .order_by('fiscalYear')
    researchYear = []
    researchSum = []
    if fiscalYearStart == fiscalYearEnd:  # ใส่ค่าล่วงหน้า 1 ปี มีค่าเป็น 0 สำหรับให้เ
        researchYear.append("0")
        researchSum.append(0.00)
    for research in researchss:
        researchYear.append(str(research['fiscalYear']))
        researchSum.append(research['sum'])
    dfResearchBudget = pd.DataFrame({'Year': researchYear, 'Budget': researchSum}, columns=['Year', 'Budget'])
    return dfResearchBudget

def getResearchBudgetTypeSet(budgetType, fiscalYearStart, fiscalYearEnd):
    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        researchs = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('budgetType').annotate(count=Count('budget'), sum=Sum('budget'))\
            .order_by('budgetType')
    else:
        researchs = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             budgetType=budgetType).values('budgetType').\
            annotate(count=Count('budget'), sum=Sum('budget')).order_by('budgetType')
    researchBudgetType = []
    researchCount = []
    researchSum = []
    for research in researchs:
        researchBudgetType.append(str(research['budgetType']))
        researchCount.append(research['count'])
        researchSum.append(research['sum'])
    dfResearchBudgetType = pd.DataFrame({'Type': researchBudgetType, 'Count':researchCount , 'Budget': researchSum},
                                        columns=['Type', 'Count',  'Budget'])
    return dfResearchBudgetType

#  ******************** Social Service *********************
def getSocialServiceFiscalYears():
    fiscalYearDatas = SocialService.objects.all().values('fiscalYear').distinct().order_by('fiscalYear')
    fiscalYears = []  #ปีงบประมาณแบบไม่ซ้ำ
    for f in fiscalYearDatas:
        fiscalYears.append(f['fiscalYear'])
    return fiscalYears

def getSocialServiceCountSet(budgetType, fiscalYearStart, fiscalYearEnd):
    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        socialservicess = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('fiscalYear').annotate(count=Count('fiscalYear'))\
            .order_by('fiscalYear')
    else:
        socialservicess = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             budgetType=budgetType).values('fiscalYear').annotate(count=Count('fiscalYear'))\
            .order_by('fiscalYear')
    socialserviceYear = []
    socialserviceCount = []
    for socialservice in socialservicess:
        socialserviceYear.append(str(socialservice['fiscalYear']))
        socialserviceCount.append(socialservice['count'])
    dfSocialServiceCount = pd.DataFrame({'Year': socialserviceYear, 'Count': socialserviceCount}, columns=['Year', 'Count'])
    return dfSocialServiceCount

def getSocialServiceBudgetSet(budgetType, fiscalYearStart, fiscalYearEnd):
    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        socialservices = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('fiscalYear').annotate(sum=Sum('budget'))\
            .order_by('fiscalYear')
    else:
        socialservices = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             budgetType=budgetType).values('fiscalYear').annotate(sum=Sum('budget'))\
            .order_by('fiscalYear')
    socialserviceYear = []
    socialserviceSum = []
    if fiscalYearStart == fiscalYearEnd:  # ใส่ค่าล่วงหน้า 1 ปี มีค่าเป็น 0 สำหรับให้เ
        socialserviceYear.append("0")
        socialserviceSum.append(0.00)
    for socialservice in socialservices:
        socialserviceYear.append(str(socialservice['fiscalYear']))
        socialserviceSum.append(socialservice['sum'])
    dfSocialServiceBudget = pd.DataFrame({'Year': socialserviceYear, 'Budget': socialserviceSum}, columns=['Year', 'Budget'])
    return dfSocialServiceBudget

def getSocialServiceBudgetTypeSet(budgetType, fiscalYearStart, fiscalYearEnd):
    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        socialservices = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('budgetType').annotate(count=Count('budget'), sum=Sum('budget'))\
            .order_by('budgetType')
    else:
        socialservices = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             budgetType=budgetType).values('budgetType').\
            annotate(count=Count('budget'), sum=Sum('budget')).order_by('budgetType')
    socialserviceBudgetType = []
    socialserviceCount = []
    socialserviceSum = []
    for socialservice in socialservices:
        socialserviceBudgetType.append(str(socialservice['budgetType']))
        socialserviceCount.append(socialservice['count'])
        socialserviceSum.append(socialservice['sum'])
    dfSocialServiceBudgetType = pd.DataFrame({'Type': socialserviceBudgetType, 'Count':socialserviceCount , 'Budget': socialserviceSum},
                                        columns=['Type', 'Count',  'Budget'])
    return dfSocialServiceBudgetType

# *********************** Command ************************
def getCommandEduYears():
    eduYearDatas = Command.objects.all().values('eduYear').distinct().order_by('eduYear')
    eduYears = []  # ปีงบประมาณแบบไม่ซ้ำ
    for f in eduYearDatas:
        eduYears.append(f['eduYear'])
    return eduYears

def getCommandCountSet(mission, eduYearStart, eduYearEnd):
    if mission is None or mission == 'None' or mission == '0':  # เลือกทั้งหมด
        commands = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd
                                                       ).values('eduYear').annotate(count=Count('eduYear')) \
            .order_by('eduYear')
    else:
        commands = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd,
                                                       mission=mission).values('eduYear').annotate(
            count=Count('eduYear')).order_by('eduYear')
    commandYear = []
    commandCount = []
    for command in commands:
        commandYear.append(str(command['eduYear']))
        commandCount.append(command['count'])
    dfCommandCount = pd.DataFrame({'Year': commandYear, 'Count': commandCount}, columns=['Year', 'Count'])
    return dfCommandCount

# def getCommandBudgetSet(mission, eduYearStart, eduYearEnd):
#     if mission is None or mission == 'None' or mission == '0':  # เลือกทั้งหมด
#         commandss = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd
#                                                        ).values('eduYear').annotate(sum=Sum('budget')) \
#             .order_by('eduYear')
#     else:
#         commandss = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd,
#                                                        mission=mission).values('eduYear').annotate(
#             sum=Sum('budget')).order_by('eduYear')
#     commandYear = []
#     commandSum = []
#     if eduYearStart == eduYearEnd:  # ใส่ค่าล่วงหน้า 1 ปี มีค่าเป็น 0 สำหรับให้เ
#         commandYear.append("0")
#         commandSum.append(0.00)
#     for command in commandss:
#         commandYear.append(str(command['eduYear']))
#         commandSum.append(command['sum'])
#     dfCommandBudget = pd.DataFrame({'Year': commandYear, 'Budget': commandSum},
#                                          columns=['Year', 'Budget'])
#     return dfCommandBudget

def getCommandMissionSet(mission, eduYearStart, eduYearEnd):
    if mission is None or mission == 'None' or mission == '0':  # เลือกทั้งหมด
        commands = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd
                                                      ).values('mission').annotate(count=Count('mission')) \
            .order_by('mission')
    else:
        commands = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd,
                                                      mission=mission).values('mission'). \
            annotate(count=Count('mission')).order_by('mission')
    commandMission = []
    commandCount = []    
    for command in commands:
        commandMission.append(str(command['mission']))
        commandCount.append(command['count'])        
    dfCommandMission = pd.DataFrame({'Mission': commandMission, 'Count': commandCount},
        columns=['Mission', 'Count'])
    return dfCommandMission


# *********************** Trainning ************************
def getTrainingFiscalYears():
    fiscalYearDatas = Training.objects.all().values('fiscalYear').distinct().order_by('fiscalYear')
    fiscalYears = []  #ปีงบประมาณแบบไม่ซ้ำ
    for f in fiscalYearDatas:
        fiscalYears.append(f['fiscalYear'])
    return fiscalYears

def getTrainingCountSet(division, fiscalYearStart, fiscalYearEnd):
    if division is None or division =='None' or division == '0':  # เลือกทั้งหมด
        trainings = Training.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('personnel__division__name_th').annotate(count=Count('personnel__division'))\
            .order_by('personnel__division__name_th')
    else:
        trainings = Training.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             personnel__division=division).values('personnel__division__name_th').\
            annotate(count=Count('personnel__division'))\
            .order_by('personnel__division__name_th')
    trainingDivision = []
    trainingCount = []
    for training in trainings:
        trainingDivision.append(str(training['personnel__division__name_th']))
        trainingCount.append(training['count'])
    dfTrainingCount = pd.DataFrame({'Division': trainingDivision, 'Count': trainingCount}, columns=['Division', 'Count'])
    return dfTrainingCount

def getTrainingBudgetSet(division, fiscalYearStart, fiscalYearEnd):
    if division is None or division =='None' or division == '0':  # เลือกทั้งหมด
        trainings = Training.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('fiscalYear').annotate(count=Count('fiscalYear'), sum=Sum('budget'))\
            .order_by('fiscalYear')
    else:
        trainings = Training.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             personnel__division=division).values('fiscalYear').annotate(count=Count('fiscalYear'),sum=Sum('budget'))\
            .order_by('fiscalYear')
    trainingYear = []
    trainingCount = []
    trainingSum = []
    if fiscalYearStart == fiscalYearEnd:  # ใส่ค่าล่วงหน้า 1 ปี มีค่าเป็น 0 สำหรับให้เ
        trainingYear.append("0")
        trainingCount.append((0))
        trainingSum.append(0.00)
    elif trainings.count() == 1:
        trainingYear.append(str(fiscalYearStart))
        trainingCount.append(0)
        trainingSum.append(0.00)
    for training in trainings:
        trainingYear.append(str(training['fiscalYear']))
        trainingCount.append(training['count'])
        trainingSum.append(training['sum'])
    dfTrainingBudget = pd.DataFrame({'Year': trainingYear, 'Count': trainingCount,  'Budget': trainingSum}, columns=['Year', 'Count', 'Budget'])
    return dfTrainingBudget

# *********************** Leave ************************
def getLeaveFiscalYears():
    fiscalYearDatas = Leave.objects.all().values('fiscalYear').distinct().order_by('fiscalYear')
    fiscalYears = []  #ปีงบประมาณแบบไม่ซ้ำ
    for f in fiscalYearDatas:
        fiscalYears.append(f['fiscalYear'])
    return fiscalYears

def getLeaveCountSet(division, fiscalYearStart, fiscalYearEnd):
    if division is None or division =='None' or division == '0':  # เลือกทั้งหมด
        leaves = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('personnel__division__name_th').annotate(count=Count('personnel__division'))\
            .order_by('personnel__division__name_th')
    else:
        leaves = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             personnel__division=division).values('personnel__division__name_th').\
            annotate(count=Count('personnel__division'))\
            .order_by('personnel__division__name_th')
    leaveDivision = []
    leaveCount = []
    for leave in leaves:
        leaveDivision.append(str(leave['personnel__division__name_th']))
        leaveCount.append(leave['count'])
    dfLeaveCount = pd.DataFrame({'Division': leaveDivision, 'Count': leaveCount}, columns=['Division', 'Count'])
    return dfLeaveCount

def getLeaveTypeSet(division, fiscalYearStart, fiscalYearEnd):
    if division is None or division =='None' or division == '0':  # เลือกทั้งหมด
        leaveTypes = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd
                                             ).values('leaveType').annotate(count=Count('leaveType'), days=Sum('days'))\
            .order_by('leaveType')
    else:
        leaveTypes = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                             personnel__division=division).values('leaveType').annotate(count=Count('leaveType'), days=Sum('days'))\
            .order_by('leaveType')
    leaveType = []
    leaveCount = []
    leaveDays = []
    for leave in leaveTypes:
        leaveType.append(str(leave['leaveType']))
        leaveCount.append(leave['count'])
        leaveDays.append(leave['days'])
    dfLeaveBudget = pd.DataFrame({'Type': leaveType, 'Count': leaveCount, 'Days' : leaveDays}, columns=['Type', 'Count', 'Days'])
    return dfLeaveBudget
