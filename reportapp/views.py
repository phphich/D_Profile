from django.shortcuts import render
from datetime import datetime
from django.db.models import Max
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from baseapp.models import *
# from baseapp.forms import *
from workapp.models import *
from reportapp import statistic

from django.contrib import messages
from django.core.paginator import (Paginator, EmptyPage,PageNotAnInteger,)
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from django.db.models import F, Sum, Q, Count


def personnelReport(request, divId=None, reportType=None):
    divisions = Division.objects.all().order_by('name_th')
    if divisions is None:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
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

def researchReport(request, budgetType=None, fiscalYearStart=None, fiscalYearEnd=None, reportType=None):
    researchCount = Research.objects.all().count()
    if researchCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
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
        print("c")
        budgetType = None
        fiscalYearStart = fiscalYearResearchs[len(fiscalYearResearchs)-1]
        fiscalYearEnd = fiscalYearResearchs[len(fiscalYearResearchs)-1]
        reportType = 'dashboard'

    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        count = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).count()
        rsum  = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).aggregate(sum=Sum('budget'))
        sum = rsum['sum']
    else:
        print("e")
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

def socialserviceReport(request, budgetType=None, fiscalYearStart=None, fiscalYearEnd=None, reportType=None):
    socialserviceCount = SocialService.objects.all().count()
    if socialserviceCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
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
        print("c")
        budgetType = None
        fiscalYearStart = fiscalYearSocialServices[len(fiscalYearSocialServices)-1]
        fiscalYearEnd = fiscalYearSocialServices[len(fiscalYearSocialServices)-1]
        reportType = 'dashboard'

    if budgetType is None or budgetType =='None' or budgetType == '0':  # เลือกทั้งหมด
        count = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).count()
        rsum  = SocialService.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).aggregate(sum=Sum('budget'))
        sum = rsum['sum']
    else:
        print("e")
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
    # print("**************************")
    # print('fiscalYearSocialService')
    # print(fiscalYearSocialServices)
    # print('budgetTypes')
    # print(budgetTypes)
    # print('budgetType')
    # print(budgetType)
    # print('fiscalYearStart')
    # print(fiscalYearStart)
    # print('fiscalYearEnd')
    # print(fiscalYearEnd)
    # print("count")
    # print(count)
    # print("**************************")
    #
    dfSocialServiceCount = statistic.getSocialServiceCountSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfSocialServiceBudget = statistic.getSocialServiceBudgetSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfSocialServiceBudgetType = statistic.getSocialServiceBudgetTypeSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)

    print('dfSocialServiceBudgetType')
    print(dfSocialServiceBudgetType)
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

# ********************* การฝึกอบรม/สัมมนา ***********************
def trainingReport(request, divId=None, fiscalYearStart=None, fiscalYearEnd=None, reportType=None):
    trainingCount = Training.objects.all().count()
    if trainingCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
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
        print("c")
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
        print("e")
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
    print("**************************")
    print('fiscalYearSocialService')
    print(fiscalYearTrainings)
    print('division')
    print(division)
    print('fiscalYearStart')
    print(fiscalYearStart)
    print('fiscalYearEnd')
    print(fiscalYearEnd)
    print("count")
    print(count)
    print("**************************")

    dfTrainingCount = statistic.getTrainingCountSet(division=division, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    print('dfTrainingCount')
    print(dfTrainingCount)
    dfTrainingBudget = statistic.getTrainingBudgetSet(division=division, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    print('dfTrainingBudget')
    print(dfTrainingBudget)
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
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
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
        print("c")
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
        print("e")
        division = Division.objects.filter(id=divId).first()
        count = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd, personnel__division=division).count()
        rsum = Leave.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd,
                                        personnel__division=division).aggregate(sum=Sum('days'))
        sum = rsum['sum']

    #ปีงบประมาณ
    fiscalYearLeaves = list(reversed(fiscalYearLeaves)) #กลับด้านลิสต์ จากมากไปน้อย
    print("**************************")
    print('fiscalYearSocialService')
    print(fiscalYearLeaves)
    print('division')
    print(division)
    print('fiscalYearStart')
    print(fiscalYearStart)
    print('fiscalYearEnd')
    print(fiscalYearEnd)
    print("count")
    print(count)
    print('sum')
    print(sum)

    print("**************************")

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
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
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
        print("c")
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
        print("e")
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
    print("**************************")
    print('fiscalYearSocialService')
    print(fiscalYearPerformances)
    print('division')
    print(division)
    print('fiscalYearStart')
    print(fiscalYearStart)
    print('fiscalYearEnd')
    print(fiscalYearEnd)
    print("count")
    print(count)

    print("**************************")

    dfPerformanceCount = statistic.getPerformanceCountSet(division=division, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    print('dfPerformanceCount')
    print(dfPerformanceCount)
    dfPerformanceBudget = statistic.getPerformanceBudgetSet(division=division, fiscalYearStart=fiscalYearStart,
                                                      fiscalYearEnd=fiscalYearEnd)
    print('dfPerformanceBudget')
    print(dfPerformanceBudget)
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

# ********************* คำสั่ง  ***********************
def commandReport(request, mission=None, eduYearStart=None, eduYearEnd=None, reportType=None):
    commandCount = Command.objects.all().count()
    if commandCount == 0:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
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
        print("c")
        mission = None
        eduYearStart = eduYearCommands[len(eduYearCommands)-1]
        eduYearEnd = eduYearCommands[len(eduYearCommands)-1]
        reportType = 'dashboard'

    if mission is None or mission =='None' or mission == '0':  # เลือกทั้งหมด
        count = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd).count()
    else:
        print("e")
        count = Command.objects.filter(eduYear__gte=eduYearStart, eduYear__lte=eduYearEnd, mission=mission).count()

    #ปีการศึกษา
    eduYearCommands = list(reversed( eduYearCommands)) #กลับด้านลิสต์ จากมากไปน้อย
    # print("**************************")
    # print('eduYearCommand')
    # print(eduYearCommands)
    # print('missions')
    # print(missions)
    # print('mission')
    # print(mission)
    # print('eduYearStart')
    # print(eduYearStart)
    # print('eduYearEnd')
    # print(eduYearEnd)
    # print("count")
    # print(count)
    # print("**************************")
    #
    dfCommandCount = statistic.getCommandCountSet(mission=mission, eduYearStart=eduYearStart,
                                                    eduYearEnd=eduYearEnd)
    # dfCommandBudget = statistic.getCommandBudgetSet(mission=mission, eduYearStart=eduYearStart,
    #                                                 eduYearEnd=eduYearEnd)
    dfCommandMission = statistic.getCommandMissionSet(mission=mission, eduYearStart=eduYearStart,
                                                    eduYearEnd=eduYearEnd)
    print('dfCommandCount')
    print(dfCommandCount)
    print('dfCommandMission')
    print(dfCommandMission)
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
    personnel = Personnel.objects.filter(id=personnelId).first()
    educations = Education.objects.filter(personnel_id=personnelId)
    expertises = Expertise.objects.filter(personnel_id=personnelId)
    curraffs = CurrAffiliation.objects.filter(personnel__id=personnelId)

    trainings = Training.objects.filter(personnel_id=personnelId).order_by('-fiscalYear')
    leaves = Leave.objects.filter(personnel_id=personnelId).order_by('-fiscalYear')
    performances = Performance.objects.filter(personnel_id=personnelId).order_by('-fiscalYear')
    researchs = Research.objects.filter(researchperson__personnel__id=personnelId).order_by('-fiscalYear')
    socialservices = SocialService.objects.filter(socialserviceperson__personnel__id=personnelId).order_by('-fiscalYear')
    commands = Command.objects.filter(commandperson__personnel__id=personnelId).order_by('-fiscalYear')
    choices = None
    if 'choices' in request.POST:
        choices = request.POST.getlist('choices')
        print('choices')
        print(choices)

    context = {'personnel':personnel, 'educations':educations, 'expertises':expertises, 'curraffs':curraffs,
               'trainings':trainings, 'researchs':researchs, 'socialservices':socialservices,
               'performances':performances,'leaves':leaves, 'commands':commands, 'choices': choices,
               }
    return render(request, 'report/personnelDetailReport.html', context)

# *************************** Research Detail Report ************************
def researchDetailReport(request, researchId):
    request.session['last_url'] = request.path_info
    research = Research.objects.filter(id=researchId).first()
    researchers = ResearchPerson.objects.filter(research=research)
    context = {'research':research, 'researchers':researchers }
    return render(request, 'report/researchDetailReport.html', context)

# *************************** SocialService Detail Report ************************
def socialserviceDetailReport(request, socialserviceId):
    request.session['last_url'] = request.path_info
    socialservice = SocialService.objects.filter(id=socialserviceId).first()
    operators = SocialServicePerson.objects.filter(socialservice=socialservice)
    context = {'socialservice':socialservice, 'operators':operators }
    return render(request, 'report/socialserviceDetailReport.html', context)

# *************************** Command Detail Report ************************
def commandDetailReport(request, commandId):
    request.session['last_url'] = request.path_info
    command = Command.objects.filter(id=commandId).first()
    staffs = CommandPerson.objects.filter(command=command)
    context = {'command':command, 'staffs':staffs }
    return render(request, 'report/commandDetailReport.html', context)

# *************************** Training Detail Report ************************
def trainingDetailReport(request, trainingId):
    request.session['last_url'] = request.path_info
    training = Training.objects.filter(id=trainingId).first()
    context = {'training':training }
    return render(request, 'report/trainingDetailReport.html', context)

# *************************** Performance Detail Report ************************
def performanceDetailReport(request, performanceId):
    request.session['last_url'] = request.path_info
    performance = Performance.objects.filter(id=performanceId).first()
    context = {'performance':performance }
    return render(request, 'report/performanceDetailReport.html', context)

# *************************** Leave Detail Report ************************
def leaveDetailReport(request, leaveId):
    request.session['last_url'] = request.path_info
    leave = Leave.objects.filter(id=leaveId).first()
    context = {'leave':leave }
    return render(request, 'report/leaveDetailReport.html', context)

