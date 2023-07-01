from django.shortcuts import render, redirect
from workapp.models import *
from reportapp import statistic

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
import plotly.express as px
from django.db.models import F, Sum, Q, Count
from workapp import common

def getSession(request, dtype=None, did=None):
    global uId
    global uType
    global docType
    global docId
    global msgErrorPermission
    msgErrorPermission='ท่านกำลังพยายามเข้าถึงข้อมูลหรือระบบย่อย ในส่วนที่ไม่ได้รับอนุญาตให้เข้าใช้งานได้!'

    docType = dtype
    docId = did
    if 'userId' in request.session:
        uId = request.session['userId']
    if 'userType' in request.session:
        uType = request.session['userType']

# ********************* บุคลากร ***********************
def personnelReport(request, divId=None, reportType=None):
    divisions = Division.objects.all().order_by('name_th')
    if divisions is None:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงานข้อมูลบุคลากร')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    if divId is not None:
        divId = divId
        reportType = reportType
    elif 'divId' in request.POST:
        divId = request.POST['divId']
        reportType = request.POST['reportType']

    if divId == None or int(divId) == 0:
        division = None
        if reportType is not None:
            reportType = reportType
        else:
            reportType = 'dashboard'
        count = Personnel.objects.all().count()
    else:
        division = Division.objects.filter(id=divId).first()
        count = Personnel.objects.filter(division=division).count()

    dfDiv = statistic.getDivisionSet(division=division)
    dfEdu = statistic.getEducationSet(division=division)
    dfStatus = statistic.getStatusSet(division=division)
    dfGender = statistic.getGenderSet(division=division)

    figDiv = px.bar(dfDiv, x='Division', y='Count', title='บุคลากรแยกตามสาขา/หน่วยงานย่อย')
    figDiv.update_layout(autosize=False, width=450, height=350,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),paper_bgcolor="white")
                      # paper_bgcolor="aliceblue")
    chartDiv = figDiv.to_html()

    figEdu = px.pie(dfEdu, names='Level', values='Count', title='บุคลากรแยกตามระดับการศึกษา')
    figEdu.update_layout(autosize=False, width=300, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartEdu = figEdu.to_html()

    figStatus = px.pie(dfStatus, names='Status', values='Count', title='บุคลากรแยกตามตำแหน่งทางวิชาการ')
    figStatus.update_layout(autosize=False, width=300, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),  paper_bgcolor="white")
    chartStatus = figStatus.to_html()

    figGender = px.bar(dfGender, x='Gender', y='Count', title='บุคลากรแยกตามเพศ')
    figGender.update_layout(autosize=False, width=300, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),  paper_bgcolor="white")
    chartGender = figGender.to_html()

    context = {'divisions': divisions, 'division':division, 'reportType':reportType, 'dfDiv':dfDiv,  'dfEdu': dfEdu, 'dfStatus':dfStatus, 'dfGender':dfGender,
               'chartDiv': chartDiv, 'chartEdu': chartEdu, 'chartStatus':chartStatus, 'chartGender':chartGender,
               'count': count}
    return render(request, 'report/personnelReport.html', context)

# ********************* การฝึกอบรม/สัมมนา ***********************
def trainingReport(request, divId=None, fiscalYearStart=None, fiscalYearEnd=None, reportType=None):
    trainingCount = Training.objects.all().count()
    if trainingCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงานข้อมูลการฝึกอบรม/สัมมนา')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    fiscalYearTrainings = statistic.getTrainingFiscalYears() #ปีฝึกอบรมที่มีในฐานข้อมูล
    divisions = Division.objects.all().order_by('name_th')

    if divId is not None:#มาจากคลิ้กลิงก์
        divId=divId
        fiscalYearStart = int(fiscalYearStart)
        fiscalYearEnd = int(fiscalYearEnd)
        reportType = reportType
    elif 'divId' in request.POST:#มาจากเลือก Selecct box
        divId = request.POST['divId']
        fiscalYearStart = int(request.POST['fiscalYearStart'])
        fiscalYearEnd = int(request.POST['fiscalYearEnd'])
        if fiscalYearEnd < fiscalYearStart:
            fiscalYearEnd = fiscalYearStart
        reportType = request.POST['reportType']
    else:
        division = None
        fiscalYearStart = fiscalYearTrainings[len(fiscalYearTrainings)-1]
        fiscalYearEnd = fiscalYearTrainings[len(fiscalYearTrainings)-1]
        reportType = 'dashboard'
    if divId is None or divId =='None' or divId == '0' or divId == '':  # เลือกทั้งหมด
        division = None
        count = Training.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).count()
        rsum  = Training.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).aggregate(sum=Sum('budget'))
        sum = rsum['sum']
    else:
        division = Division.objects.filter(id=divId).first()
        count = Training.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd, personnel__division=division).count()
        rsum = Training.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                        personnel__division=division).aggregate(sum=Sum('budget'))
        sum = rsum['sum']

    if sum is not None:
        strsum = "{:,.2f}".format(sum/1000000)+"M."
    else:
        strsum = "0.00M."
        sum = 0.00

    #ปีงบประมาณ
    fiscalYearTrainings = list(reversed(fiscalYearTrainings)) #กลับด้านลิสต์ จากมากไปน้อย

    dfTrainingCount = statistic.getTrainingCountSet(division=division, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfTrainingBudget = statistic.getTrainingBudgetSet(division=division, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    figTrainingCount = px.bar(dfTrainingCount, x='Division', y='Count', title='จำนวนครั้งการฝึกอบรม/สัมมนาแยกตามสาขา')
    figTrainingCount.update_layout(autosize=False, width=450, height=350,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartTrainingCount = figTrainingCount.to_html()

    figTrainingBudget = px.line(dfTrainingBudget, x="Year", y="Budget", title='งบประมาณการฝึกอบรม/สัมมนาแยกตามปีงบประมาณ')
    figTrainingBudget.update_layout(autosize=False, width=400, height=300,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartTrainingBudget = figTrainingBudget.to_html()

    context = {'divisions':divisions, 'division':division,
               'fiscalYearTrainings':fiscalYearTrainings,
               'fiscalYearStart':fiscalYearStart, 'fiscalYearEnd':fiscalYearEnd, 'reportType':reportType,
               'dfTrainingCount':dfTrainingCount,'chartTrainingCount':chartTrainingCount,
               'dfTrainingBudget': dfTrainingBudget, 'chartTrainingBudget': chartTrainingBudget,
               'count':count,'sum':sum, 'strsum':strsum}
    return render(request, 'report/trainingReport.html', context)

# ********************* การลา **********************
def leaveReport(request, divId=None, fiscalYearStart=None, fiscalYearEnd=None, reportType=None):
    leaveCount = Leave.objects.all().count()
    if leaveCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงานข้อมูลการลา')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    fiscalYearLeaves = statistic.getLeaveFiscalYears() #ปีที่ลาที่มีในฐานข้อมูล
    divisions = Division.objects.all().order_by('name_th')

    if divId is not None:#มาจากคลิ้กลิงก์
        divId=divId
        fiscalYearStart = int(fiscalYearStart)
        fiscalYearEnd = int(fiscalYearEnd)
        reportType = reportType
    elif 'divId' in request.POST:#มาจากเลือก Selecct box
        divId = request.POST['divId']
        fiscalYearStart = int(request.POST['fiscalYearStart'])
        fiscalYearEnd = int(request.POST['fiscalYearEnd'])
        if fiscalYearEnd < fiscalYearStart:
            fiscalYearEnd = fiscalYearStart
        reportType = request.POST['reportType']
    else:
        division = None
        fiscalYearStart = fiscalYearLeaves[len(fiscalYearLeaves)-1]
        fiscalYearEnd = fiscalYearLeaves[len(fiscalYearLeaves)-1]
        reportType = 'dashboard'
    if divId is None or divId =='None' or divId == '0' or divId == '':  # เลือกทั้งหมด
        division = None
        count = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).count()
        rsum = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                        ).aggregate(sum=Sum('days'))
        sum = rsum['sum']
    else:
        division = Division.objects.filter(id=divId).first()
        count = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd, personnel__division=division).count()
        rsum = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                        personnel__division=division).aggregate(sum=Sum('days'))
        sum = rsum['sum']

    #ปีงบประมาณ
    fiscalYearLeaves = list(reversed(fiscalYearLeaves)) #กลับด้านลิสต์ จากมากไปน้อย

    dfLeaveCount = statistic.getLeaveCountSet(division=division, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfLeaveType = statistic.getLeaveTypeSet(division=division, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    figLeaveCount = px.bar(dfLeaveCount, x='Division', y='Count', title='จำนวนครั้งในการลาแยกตามสาขา')
    figLeaveCount.update_layout(autosize=False, width=450, height=350,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartLeaveCount = figLeaveCount.to_html()

    figLeaveType = px.pie(dfLeaveType, names="Type", values="Count", title='จำนวนครั้งในการลาแยกตามประเภท')
    figLeaveType.update_layout(autosize=False, width=350, height=350,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartLeaveType = figLeaveType.to_html()

    figLeaveDays = px.pie(dfLeaveType, names="Type", values="Days", title='จำนวนวันลาแยกตามประเภท')
    figLeaveDays.update_layout(autosize=False, width=350, height=350,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartLeaveDays = figLeaveDays.to_html()

    context = {'divisions':divisions, 'division':division,
               'fiscalYearLeaves':fiscalYearLeaves,
               'fiscalYearStart':fiscalYearStart, 'fiscalYearEnd':fiscalYearEnd, 'reportType':reportType,
               'dfLeaveCount':dfLeaveCount,'chartLeaveCount':chartLeaveCount,
               'dfLeaveType': dfLeaveType, 'chartLeaveType': chartLeaveType, 'chartLeaveDays': chartLeaveDays,

               'count':count, 'sum': sum}
    return render(request, 'report/leaveReport.html', context)

# ********************* การรับตำแหน่งผลงาน/รางวัล *********************
def performanceReport(request, divId=None, fiscalYearStart=None, fiscalYearEnd=None, reportType=None):
    performanceCount = Performance.objects.all().count()
    if performanceCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงานข้อมูลผลงานและรางวัล')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    fiscalYearPerformances = statistic.getPerformanceFiscalYears() #ปีรับผลงานที่มีในฐานข้อมูล
    divisions = Division.objects.all().order_by('name_th')

    if divId is not None:#มาจากคลิ้กลิงก์
        divId=divId
        fiscalYearStart = int(fiscalYearStart)
        fiscalYearEnd = int(fiscalYearEnd)
        reportType = reportType
    elif 'divId' in request.POST:#มาจากเลือก Selecct box
        divId = request.POST['divId']
        fiscalYearStart = int(request.POST['fiscalYearStart'])
        fiscalYearEnd = int(request.POST['fiscalYearEnd'])
        if fiscalYearEnd < fiscalYearStart:
            fiscalYearEnd = fiscalYearStart
        reportType = request.POST['reportType']
    else:
        division = None
        fiscalYearStart = fiscalYearPerformances[len(fiscalYearPerformances)-1]
        fiscalYearEnd = fiscalYearPerformances[len(fiscalYearPerformances)-1]
        reportType = 'dashboard'
    if divId is None or divId =='None' or divId == '0' or divId == '':  # เลือกทั้งหมด
        division = None
        count = Performance.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).count()
        rsum = Performance.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).aggregate(
            sum=Sum('budget'))
        sum = rsum['sum']
    else:
        division = Division.objects.filter(id=divId).first()
        count = Performance.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd, personnel__division=division).count()
        rsum = Performance.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                        personnel__division=division).aggregate(sum=Sum('budget'))
        sum = rsum['sum']

    if sum is not None:
        strsum = "{:,.2f}".format(sum/1000000)+"M."
    else:
        strsum = "0.00M."
        sum = 0.00
    #ปีงบประมาณ
    fiscalYearPerformances = list(reversed(fiscalYearPerformances)) #กลับด้านลิสต์ จากมากไปน้อย

    dfPerformanceCount = statistic.getPerformanceCountSet(division=division, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfPerformanceBudget = statistic.getPerformanceBudgetSet(division=division, fiscalYearStart=fiscalYearStart,
                                                      fiscalYearEnd=fiscalYearEnd)
    figPerformanceCount = px.bar(dfPerformanceCount, x='Division', y='Count', title='จำนวนครั้งที่ได้รับผลงานและรางวัล')
    figPerformanceCount.update_layout(autosize=False, width=450, height=350,
                                   margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartPerformanceCount = figPerformanceCount.to_html()

    figPerformanceBudget = px.line(dfPerformanceBudget, x="Year", y="Budget",
                                title='งบประมาณที่ใช้สำหรับการได้รับผลงานและรางวัล')
    figPerformanceBudget.update_layout(autosize=False, width=400, height=300,
                                    margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartPerformanceBudget = figPerformanceBudget.to_html()

    context = {'divisions': divisions, 'division': division,
               'fiscalYearPerformances': fiscalYearPerformances,
               'fiscalYearStart': fiscalYearStart, 'fiscalYearEnd': fiscalYearEnd, 'reportType': reportType,
               'dfPerformanceCount': dfPerformanceCount, 'chartPerformanceCount': chartPerformanceCount,
               'dfPerformanceBudget': dfPerformanceBudget, 'chartPerformanceBudget': chartPerformanceBudget,
               'count': count, 'sum':sum, 'strsum':strsum }
    return render(request, 'report/performanceReport.html', context)

# ********************* วิจัย ***********************
def researchReport(request, budgetType=None, fiscalYearStart=None, fiscalYearEnd=None, reportType=None):
    researchCount = Research.objects.all().count()
    if researchCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงานข้อมูลการวิจัย')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    fiscalYearResearchs = statistic.getResearchFiscalYears() #ปีวิจัยที่มีในฐานข้อมูล
    budgetTypes = statistic.getBudgetType()

    if budgetType is not None:#มาจากคลิ้กลิงก์
        budgetType=budgetType
        fiscalYearStart = int(fiscalYearStart)
        fiscalYearEnd = int(fiscalYearEnd)
        reportType = reportType
    elif 'budgetType' in request.POST:#มาจากเลือก Selecct box
        budgetType = request.POST['budgetType']
        fiscalYearStart = int(request.POST['fiscalYearStart'])
        fiscalYearEnd = int(request.POST['fiscalYearEnd'])
        if fiscalYearEnd < fiscalYearStart:
            fiscalYearEnd = fiscalYearStart
        reportType = request.POST['reportType']
    else:
        budgetType = None
        fiscalYearStart = fiscalYearResearchs[len(fiscalYearResearchs)-1]
        fiscalYearEnd = fiscalYearResearchs[len(fiscalYearResearchs)-1]
        reportType = 'dashboard'

    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        count = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).count()
        rsum  = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).aggregate(sum=Sum('budget'))
        sum = rsum['sum']
    else:
        count = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd, budgetType=budgetType).count()
        rsum = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                        budgetType=budgetType).aggregate(sum=Sum('budget'))
        sum = rsum['sum']

    if sum is not None:
        strsum = "{:,.2f}".format(sum/1000000)+"M."
    else:
        strsum = "0.00M."
        sum = 0.00

    #ปีงบประมาณ
    fiscalYearResearchs = list(reversed(fiscalYearResearchs)) #กลับด้านลิสต์ จากมากไปน้อย
    dfResearchCount = statistic.getResearchCountSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfResearchBudget = statistic.getResearchBudgetSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfResearchBudgetType = statistic.getResearchBudgetTypeSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)

    figResearchCount = px.bar(dfResearchCount, x='Year', y='Count', title='จำนวนโครงการวิจัยแยกตามปีงบประมาณ')
    figResearchCount.update_layout(autosize=False, width=450, height=350,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartResearchCount = figResearchCount.to_html()

    figResearchBudget = px.line(dfResearchBudget, x="Year", y="Budget", title='ทุนวิจัยแยกตามปีงบประมาณ')
    figResearchBudget.update_layout(autosize=False, width=400, height=300,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartResearchBudget = figResearchBudget.to_html()

    figResearchBudgetType = px.pie(dfResearchBudgetType, names='Type', values='Budget', title='ทุนวิจัยแยกตามประเภทงบประมาณ')
    figResearchBudgetType.update_layout(autosize=False, width=400, height=400,
                         margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartResearchBudgetType = figResearchBudgetType.to_html()

    figResearchBudgetTypeCount = px.pie(dfResearchBudgetType, names='Type', values='Count', title='จำนวนโครงการวิจัยแยกตามประเภทงบประมาณ')
    figResearchBudgetTypeCount.update_layout(autosize=False, width=350, height=350,
                         margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartResearchBudgetTypeCount = figResearchBudgetTypeCount.to_html()

    figSum = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sum,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ทุนวิจัยรวม'"}))
    figSum.update_layout(autosize=False, width=200, height=200,
                                             margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartSum = figSum.to_html()

    # dfResearchBudgetType = list(reversed(dfResearchBudgetType)) # กลับด้านลิสต์ จากมากไปน้อย

    context = {'budgetTypes':budgetTypes, 'budgetType':budgetType,
               'fiscalYearResearchs':fiscalYearResearchs,
               'fiscalYearStart':fiscalYearStart, 'fiscalYearEnd':fiscalYearEnd, 'reportType':reportType,
               'dfResearchCount':dfResearchCount,'chartResearchCount':chartResearchCount,
               'dfResearchBudget': dfResearchBudget, 'chartResearchBudget': chartResearchBudget,
               'dfResearchBudgetType': dfResearchBudgetType, 'chartResearchBudgetType': chartResearchBudgetType,
               'chartResearchBudgetTypeCount': chartResearchBudgetTypeCount,
               'count':count,'sum':sum, 'strsum':strsum,'chartSum':chartSum}
    return render(request, 'report/researchReport.html', context)

# ********************* บริการทางวิชาการ ***********************
def socialserviceReport(request, budgetType=None, fiscalYearStart=None, fiscalYearEnd=None, reportType=None):
    socialserviceCount = SocialService.objects.all().count()
    if socialserviceCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงานข้อมูลการบริการทางวิชาการแก่สังคม')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    fiscalYearSocialServices = statistic.getSocialServiceFiscalYears() #ปีวิจัยที่มีในฐานข้อมูล
    budgetTypes = statistic.getBudgetType()

    if budgetType is not None:#มาจากคลิ้กลิงก์
        budgetType=budgetType
        fiscalYearStart = int(fiscalYearStart)
        fiscalYearEnd = int(fiscalYearEnd)
        reportType = reportType
    elif 'budgetType' in request.POST: #มาจากเลือก Select
        budgetType = request.POST['budgetType']
        fiscalYearStart = int(request.POST['fiscalYearStart'])
        fiscalYearEnd = int(request.POST['fiscalYearEnd'])
        if fiscalYearEnd < fiscalYearStart:
            fiscalYearEnd = fiscalYearStart
        reportType = request.POST['reportType']
    else:
        budgetType = None
        fiscalYearStart = fiscalYearSocialServices[len(fiscalYearSocialServices)-1]
        fiscalYearEnd = fiscalYearSocialServices[len(fiscalYearSocialServices)-1]
        reportType = 'dashboard'

    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        count = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).count()
        rsum  = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).aggregate(sum=Sum('budget'))
        sum = rsum['sum']
    else:
        count = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd, budgetType=budgetType).count()
        rsum = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                        budgetType=budgetType).aggregate(sum=Sum('budget'))
        sum = rsum['sum']

    if sum is not None:
        strsum = "{:,.2f}".format(sum/1000000)+"M."
    else:
        strsum = "0.00M."
        sum = 0.00

    #ปีงบประมาณ
    fiscalYearSocialServices = list(reversed( fiscalYearSocialServices))

    dfSocialServiceCount = statistic.getSocialServiceCountSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfSocialServiceBudget = statistic.getSocialServiceBudgetSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfSocialServiceBudgetType = statistic.getSocialServiceBudgetTypeSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    figSocialServiceCount = px.bar(dfSocialServiceCount, x='Year', y='Count', title='จำนวนโครงการฯ แยกตามปีงบประมาณ')
    figSocialServiceCount.update_layout(autosize=False, width=450, height=350,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartSocialServiceCount = figSocialServiceCount.to_html()

    figSocialServiceBudget = px.line(dfSocialServiceBudget, x="Year", y="Budget", title='งบประมาณที่ใช้แยกตามปีงบประมาณ')
    figSocialServiceBudget.update_layout(autosize=False, width=400, height=300,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartSocialServiceBudget = figSocialServiceBudget.to_html()

    figSocialServiceBudgetType = px.pie(dfSocialServiceBudgetType, names='Type', values='Budget', title='งบประมาณที่ใช้แยกตามประเภทงบประมาณ')
    figSocialServiceBudgetType.update_layout(autosize=False, width=400, height=400,
                         margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartSocialServiceBudgetType = figSocialServiceBudgetType.to_html()

    figSocialServiceBudgetTypeCount = px.pie(dfSocialServiceBudgetType, names='Type', values='Count', title='จำนวนโครงการฯ แยกตามประเภทงบประมาณ')
    figSocialServiceBudgetTypeCount.update_layout(autosize=False, width=350, height=350,
                         margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartSocialServiceBudgetTypeCount = figSocialServiceBudgetTypeCount.to_html()

    figSum = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sum,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ทุนวิจัยรวม'"}))
    figSum.update_layout(autosize=False, width=200, height=200,
                                             margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartSum = figSum.to_html()
    context = {'budgetTypes':budgetTypes, 'budgetType':budgetType,
               'fiscalYearSocialServices':fiscalYearSocialServices,
               'fiscalYearStart':fiscalYearStart, 'fiscalYearEnd':fiscalYearEnd, 'reportType':reportType,
               'dfSocialServiceCount':dfSocialServiceCount,'chartSocialServiceCount':chartSocialServiceCount,
               'dfSocialServiceBudget': dfSocialServiceBudget, 'chartSocialServiceBudget': chartSocialServiceBudget,
               'dfSocialServiceBudgetType': dfSocialServiceBudgetType, 'chartSocialServiceBudgetType': chartSocialServiceBudgetType,
               'chartSocialServiceBudgetTypeCount': chartSocialServiceBudgetTypeCount,
               'count':count,'sum':sum, 'strsum':strsum, 'chartSum':chartSum}
    return render(request, 'report/socialserviceReport.html', context)

# ********************* คำสั่ง  ***********************
def commandReport(request, mission=None, eduYearStart=None, eduYearEnd=None, reportType=None):
    commandCount = Command.objects.all().count()
    if commandCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงานข้อมูลคำสั่ง')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    eduYearCommands = statistic.getCommandEduYears() #ปีออกคำสั้่งที่มีในฐานข้อมูล
    missions = statistic.getMission()

    if mission is not None:#มาจากคลิ้กลิงก์
        mission=mission
        eduYearStart = int(eduYearStart)
        eduYearEnd = int(eduYearEnd)
        reportType = reportType
    elif 'mission' in request.POST:
        mission = request.POST['mission']
        eduYearStart = int(request.POST['eduYearStart'])
        eduYearEnd = int(request.POST['eduYearEnd'])
        if eduYearEnd < eduYearStart:
            eduYearEnd = eduYearStart
        reportType = request.POST['reportType']
    else:
        mission = None
        eduYearStart = eduYearCommands[len(eduYearCommands)-1]
        eduYearEnd = eduYearCommands[len(eduYearCommands)-1]
        reportType = 'dashboard'

    if mission is None or mission =='None' or mission == '0':  # เลือกทั้งหมด
        count = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd).count()
    else:
        count = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd, mission=mission).count()

    #ปีการศึกษา
    eduYearCommands = list(reversed( eduYearCommands)) #กลับด้านลิสต์ จากมากไปน้อย
    dfCommandCount = statistic.getCommandCountSet(mission=mission, eduYearStart=eduYearStart,
                                                    eduYearEnd=eduYearEnd)
    # dfCommandBudget = statistic.getCommandBudgetSet(mission=mission, eduYearStart=eduYearStart,
    #                                                 eduYearEnd=eduYearEnd)
    dfCommandMission = statistic.getCommandMissionSet(mission=mission, eduYearStart=eduYearStart,
                                                    eduYearEnd=eduYearEnd)
    figCommandCount = px.bar(dfCommandCount, x='Year', y='Count', title='จำนวนคำสั่งแยกตามปีการศึกษา')
    figCommandCount.update_layout(autosize=False, width=450, height=350,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartCommandCount = figCommandCount.to_html()

    # figCommandBudget = px.line(dfCommandBudget, x="Year", y="Budget", title='งบประมาณที่ใช้แยกตามปีงบประมาณ')
    # figCommandBudget.update_layout(autosize=False, width=400, height=300,
    #                       margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    # chartCommandBudget = figCommandBudget.to_html()

    figCommandMission = px.pie(dfCommandMission, names='Mission', values='Count', title='จำนวนคำสั่งแยกตามพันธกิจ')
    figCommandMission.update_layout(autosize=False, width=450, height=450,
                         margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartCommandMission = figCommandMission.to_html()

    # figCommandMissionCount = px.pie(dfCommandMission, names='Type', values='Count', title='จำนวนโครงการบริการฯ แยกตามประเภทงบประมาณ')
    # figCommandMissionCount.update_layout(autosize=False, width=350, height=350,
    #                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    # chartCommandMissionCount = figCommandMissionCount.to_html()

    # figSum = go.Figure(go.Indicator(
    #     mode="gauge+number",
    #     value=sum,
    #     domain={'x': [0, 1], 'y': [0, 1]},
    #     title={'text': "ทุนวิจัยรวม'"}))
    # figSum.update_layout(autosize=False, width=200, height=200,
    #                                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    # chartSum = figSum.to_html()
    context = {'missions':missions, 'mission':mission,
               'eduYearCommands':eduYearCommands,
               'eduYearStart':eduYearStart, 'eduYearEnd':eduYearEnd, 'reportType':reportType,
               'dfCommandCount':dfCommandCount,'chartCommandCount':chartCommandCount,
               'dfCommandMission': dfCommandMission, 'chartCommandMission': chartCommandMission,
               'count':count}
    return render(request, 'report/commandReport.html', context)

# ********************* Sub Report - Personnel ******************** #
def reportSubPersonnel(request, subNo, divId, paraValue):
    request.session['last_url'] = request.path_info
    if subNo=='1': #บุคลากรตามรหัสสาขา
        name_th = paraValue
        division = Division.objects.filter(name_th=name_th).first()
        personnels = division.getPersonnels()
        count = personnels.count()
    elif subNo=='2':  #บุคลากรตามระดับการศึกษา
        level = paraValue
        if divId is None or divId == 'None' or  divId == '0':
            persons = Personnel.objects.all()
        else:
            division = Division.objects.filter(id = divId).first()
            persons = division.getPersonnels()
        personnels = []
        for personnel in persons:
            if personnel.getHighestEducation() == level:
                personnels.append(personnel)
        count = len(personnels) #list
    elif subNo == '3': #บุคลากรตามตำแหน่งทางวิชาการ
        status = paraValue
        if divId is None or divId == 'None' or divId == '0':
            personnels = Personnel.objects.filter(status=status)
        else:
            division = Division.objects.filter(id=divId).first()
            personnels = Personnel.objects.filter(status=status, division=division)
        count = personnels.count()
    else: #บุคลากรตามเพศ
        gender = paraValue
        if divId is None or divId == 'None' or divId == '0':
            personnels = Personnel.objects.filter(gender=gender)
        else:
            division = Division.objects.filter(id=divId).first()
            personnels = Personnel.objects.filter(gender=gender, division=division)
        count = personnels.count()

    context = {'personnels': personnels, 'subNo': subNo, 'parameter': paraValue, 'count':count}
    return render(request, 'report/personnelSubReport.html', context)

# ********************* Sub Report - Training ******************** #
def trainingSubReport(request, subNo, divName=None, paraValue=None):
    request.session['last_url'] = request.path_info
    if subNo=='1': # ปี/จำนวน
        name_th = divName
        fiscalYear = int(paraValue)
        division = Division.objects.filter(name_th=name_th).first()
        trainings = Training.objects.filter(fiscalYear=fiscalYear, personnel__division = division)
        count = trainings.count()
        context = {'trainings': trainings, 'subNo': subNo, 'parameter': paraValue, 'division': division, 'count': count}
    elif subNo=='2':  #บุคลากรตามระดับการศึกษา
        fiscalYear = int(paraValue)
        trainings = Training.objects.filter(fiscalYear=fiscalYear)
        count = trainings.count()
        context = {'trainings': trainings, 'subNo': subNo, 'parameter': paraValue, 'count': count}
    return render(request, 'report/trainingSubReport.html', context)

# ********************* Sub Report - Leave ******************** #
def leaveSubReport(request, subNo, name=None, paraValue=None):
    request.session['last_url'] = request.path_info
    if subNo=='1':
        name_th = name
        fiscalYear = int(paraValue)
        division = Division.objects.filter(name_th=name_th).first()
        leaves = Leave.objects.filter(fiscalYear=fiscalYear, personnel__division = division)
        count = leaves.count()
        context = {'leaves': leaves, 'subNo': subNo, 'parameter': paraValue, 'division': division, 'count': count}
    elif subNo=='2':  #บุคลากรตามระดับการศึกษา
        leaveType = name
        fiscalYear = int(paraValue)
        leaves = Leave.objects.filter(fiscalYear=fiscalYear, leaveType=leaveType)
        count = leaves.count()
        context = {'leaves': leaves, 'subNo': subNo, 'parameter': paraValue, 'leaveType':leaveType, 'count': count}
    return render(request, 'report/leaveSubReport.html', context)

# ********************* Sub Report - Performance ******************** #
def performanceSubReport(request, subNo, divName=None, paraValue=None):
    request.session['last_url'] = request.path_info
    if subNo=='1': # ปี/จำนวน
        name_th = divName
        fiscalYear = int(paraValue)
        division = Division.objects.filter(name_th=name_th).first()
        performances = Performance.objects.filter(fiscalYear=fiscalYear, personnel__division = division)
        count = performances.count()
        context = {'performances': performances, 'subNo': subNo, 'parameter': paraValue, 'division': division, 'count': count}
    elif subNo=='2':  #บุคลากรตามระดับการศึกษา
        fiscalYear = int(paraValue)
        performances = Performance.objects.filter(fiscalYear=fiscalYear)
        count = performances.count()
        context = {'performances': performances,  'subNo': subNo, 'parameter': paraValue, 'count': count}
    return render(request, 'report/performanceSubReport.html', context)

# ********************* Sub Report - Research ******************** #
def researchSubReport(request, subNo, budgetType, paraValue):
    request.session['last_url'] = request.path_info
    if subNo=='1': #วิจัย ปี/จำนวน
        fiscalYear = int(paraValue)
        researchs = Research.objects.filter(fiscalYear=fiscalYear)
        count = researchs.count()
        context = {'researchs': researchs, 'subNo': subNo, 'parameter': paraValue, 'count': count}
    elif subNo=='2':  #บุคลากรตามระดับการศึกษา
        fiscalYear = int(paraValue)
        researchs = Research.objects.filter(fiscalYear=fiscalYear, budgetType=budgetType)
        count = researchs.count()
        context = {'researchs': researchs, 'subNo': subNo, 'parameter': paraValue, 'budgetType':budgetType, 'count': count}
    return render(request, 'report/researchSubReport.html', context)

# ********************* Sub Report - SocialService ******************** #
def socialserviceSubReport(request, subNo, budgetType, paraValue):
    request.session['last_url'] = request.path_info
    if subNo=='1': #วิจัย ปี/จำนวน
        fiscalYear = int(paraValue)
        socialservices = SocialService.objects.filter(fiscalYear=fiscalYear)
        count = socialservices.count()
        context = {'socialservices': socialservices, 'subNo': subNo, 'parameter': paraValue, 'count': count}
    elif subNo=='2':  #บุคลากรตามระดับการศึกษา
        fiscalYear = int(paraValue)
        socialservices = SocialService.objects.filter(fiscalYear=fiscalYear, budgetType=budgetType)
        count = socialservices.count()
        context = {'socialservices': socialservices, 'subNo': subNo, 'parameter': paraValue, 'budgetType':budgetType, 'count': count}
    return render(request, 'report/socialserviceSubReport.html', context)

# ********************* Sub Report - Command ******************** #
def commandSubReport(request, subNo, mission, paraValue):
    request.session['last_url'] = request.path_info
    if subNo=='1': #วิจัย ปี/จำนวน
        eduYear = int(paraValue)
        commands = Command.objects.filter(eduYear=eduYear)
        count = commands.count()
        context = {'commands': commands, 'subNo': subNo, 'parameter': paraValue, 'count': count}
    elif subNo=='2':  #วิจัยตามประเภทงบประมาณ
        eduYear = int(paraValue)
        commands = Command.objects.filter(eduYear=eduYear, mission=mission)
        count = commands.count()
        context = {'commands': commands, 'subNo': subNo, 'parameter': paraValue, 'mission':mission, 'count': count}
    return render(request, 'report/commandSubReport.html', context)

# *************************** Personnel Detail Report ************************
def personnelDetailReport(request, personnelId):
    if 'clickBack' in request.POST:
        return redirect(request.session['last_url'])
    getSession(request, dtype='Personnel', did=personnelId)
    if common.chkPermission(personnelDetailReport.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    personnel = Personnel.objects.filter(id=personnelId).first()
    educations = Education.objects.filter(personnel_id=personnelId).order_by('-yearGraduate')
    expertises = Expertise.objects.filter(personnel_id=personnelId)
    curraffs = CurrAffiliation.objects.filter(personnel__id=personnelId)

    trainings = Training.objects.filter(personnel_id=personnelId).order_by('-fiscalYear')
    leaves = Leave.objects.filter(personnel_id=personnelId).order_by('-fiscalYear')
    performances = Performance.objects.filter(personnel_id=personnelId).order_by('-fiscalYear')
    # researchs = Research.objects.filter(researchperson__personnel__id=personnelId).order_by('-fiscalYear')
    researchpersons = ResearchPerson.objects.filter(personnel__id=personnelId).order_by('-research__fiscalYear')
    socialservices = SocialService.objects.filter(socialserviceperson__personnel__id=personnelId).order_by('-fiscalYear')
    commands = Command.objects.filter(commandperson__personnel__id=personnelId).order_by('-fiscalYear')
    choices = None
    if 'choices' in request.POST:
        choices = request.POST.getlist('choices')

    context = {'personnel':personnel, 'educations':educations, 'expertises':expertises, 'curraffs':curraffs,
               'trainings':trainings, 'researchpersons':researchpersons, 'socialservices':socialservices,
               'performances':performances,'leaves':leaves, 'commands':commands, 'choices': choices,
               }
    return render(request, 'report/personnelDetailReport.html', context)

# *************************** Training Detail Report ************************
def trainingDetailReport(request, trainingId):
    getSession(request, dtype='Training', did=trainingId)
    if common.chkPermission(trainingDetailReport.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    training = Training.objects.filter(id=trainingId).first()
    context = {'training':training }
    return render(request, 'report/trainingDetailReport.html', context)

# *************************** Leave Detail Report ************************
def leaveDetailReport(request, leaveId):
    getSession(request, dtype='Leave', did=leaveId)
    if common.chkPermission(leaveDetailReport.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    leave = Leave.objects.filter(id=leaveId).first()
    context = {'leave':leave }
    return render(request, 'report/leaveDetailReport.html', context)

# *************************** Performance Detail Report ************************
def performanceDetailReport(request, performanceId):
    getSession(request, dtype='Performance', did=performanceId)
    if common.chkPermission(performanceDetailReport.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    performance = Performance.objects.filter(id=performanceId).first()
    context = {'performance':performance }
    return render(request, 'report/performanceDetailReport.html', context)

# *************************** Research Detail Report ************************
def researchDetailReport(request, researchId):
    getSession(request, dtype='Research', did=researchId)
    if common.chkPermission(researchDetailReport.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    research = Research.objects.filter(id=researchId).first()
    researchers = ResearchPerson.objects.filter(research=research)
    context = {'research':research, 'researchers':researchers }
    return render(request, 'report/researchDetailReport.html', context)

# *************************** SocialService Detail Report ************************
def socialserviceDetailReport(request, socialserviceId):
    getSession(request, dtype='SocialService', did=socialserviceId)
    if common.chkPermission(socialserviceDetailReport.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    request.session['last_url'] = request.path_info
    socialservice = SocialService.objects.filter(id=socialserviceId).first()
    operators = SocialServicePerson.objects.filter(socialservice=socialservice)
    context = {'socialservice':socialservice, 'operators':operators }
    return render(request, 'report/socialserviceDetailReport.html', context)

# *************************** Command Detail Report ************************
def commandDetailReport(request, commandId):
    getSession(request, dtype='Command', did=commandId)
    if common.chkPermission(commandDetailReport.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    command = Command.objects.filter(id=commandId).first()
    operators = CommandPerson.objects.filter(command=command)
    context = {'command':command, 'operators':operators }
    return render(request, 'report/commandDetailReport.html', context)

def search(request):
    if request.method == 'POST':
        keyword= request.POST['keyword']
        group = request.POST['group']
    if group == 'personnel':
        strgroup = "บุคลากร"
        results = Personnel.objects.filter(Q(firstname_th__icontains=keyword) | Q(lastname_th__icontains=keyword) |
                                           Q(firstname_en__icontains=keyword) | Q(lastname_en__icontains=keyword)).order_by('firstname_th','lastname_th')
    elif group == 'education':
        strgroup = "คุณวุฒิทางการศึกษา"
        results = Education.objects.filter(Q(degree_th__icontains=keyword) | Q(degree_en__icontains=keyword) |
                                           Q(degree_th_sh__icontains=keyword) | Q(degree_en_sh__icontains=keyword)
                                            ).order_by('degree_th')
    elif group == 'expertise':
        strgroup = "ความเชี่ยวชาญ"
        results = Expertise.objects.filter(Q(topic__icontains=keyword)| Q(experience__icontains=keyword)).order_by('topic')

    elif group == 'training':
        strgroup = "การฝึกอบรม/สัมมนา"
        results = Training.objects.filter(Q(topic__icontains=keyword) or Q (place__icontains=keyword)).order_by('topic')
    elif group == 'performance':
        strgroup = "ผลงานและรางวัล"
        results = Performance.objects.filter(Q(topic__icontains=keyword) or Q(source__icontains=keyword)).order_by('topic')
    elif group == 'research':
        strgroup = "การวิจัย"
        results = Research.objects.filter(Q(title_th__icontains=keyword) or Q(title_en__icontains=keyword) or
                                          Q(objective__icontains=keyword)|Q(keyword__icontains=keyword)).order_by('title_th')
    elif group == 'socialservice':
        strgroup = "การบริการทางวิชาการแก่สังคม"
        results = SocialService.objects.filter(Q(topic__icontains=keyword) or Q(place__icontains=keyword) or
                                          Q(receiver__icontains=keyword)).order_by('topic')
    elif group == 'command':
        strgroup = "คำสั่ง"
        results = Command.objects.filter(Q(topic__icontains=keyword) or Q(mission__icontains=keyword)).order_by('topic')
    if results is not None:
        count = results.count()
    else:
        count = 0
    # results = SocialService.objects.all()
    context = {'keyword':keyword, 'group':group, 'strgroup':strgroup, 'results':results, 'count':count}
    # return render(request, 'report/resultSearch.html', context)
    return  render(request, 'home.html', context)

