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

#ล็อกเอ๊าท์ผ่านระบบ Authen ของ Django
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

    #ปีงบประมาณ
    fiscalYearResearchs = list(reversed(fiscalYearResearchs)) #กลับด้านลิสต์ จากมากไปน้อย
    dfResearchCount = statistic.getResearchCountSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfResearchBudget = statistic.getResearchBudgetSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    dfResearchBudgetType = statistic.getResearchBudgetTypeSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    print('dfResearchBudgetType')
    print(dfResearchBudgetType)
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
    elif 'budgetType' in request.POST: #กลับด้านลิสต์ จากมากไปน้อย
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
    figSocialServiceCount = px.bar(dfSocialServiceCount, x='Year', y='Count', title='จำนวนโครงการบริการฯ แยกตามปีงบประมาณ')
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

    figSocialServiceBudgetTypeCount = px.pie(dfSocialServiceBudgetType, names='Type', values='Count', title='จำนวนโครงการบริการฯ แยกตามประเภทงบประมาณ')
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
    fiscalYearTrainings = statistic.getTrainingFiscalYears() #ปีวิจัยที่มีในฐานข้อมูล
    divisions = Division.objects.all().order_by('name_th')


    # if divId == None or int(divId) == 0:
    #     division = None
    #     if reportType is not None:
    #         reportType = reportType
    #     else:
    #         reportType = 'dashboard'
    #     count = Personnel.objects.all().count()
    # else:
    #     division = Division.objects.filter(id=divId).first()
    #     count = Personnel.objects.filter(division=division).count()

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
