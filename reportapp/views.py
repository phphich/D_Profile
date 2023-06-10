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

    figDiv = px.bar(dfDiv, x='Division', y='Count', title='บุคลากรแยกตามสาขา')
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
        print("a")
    elif 'budgetType' in request.POST:#มาจากเลือก Selecct box
        budgetType = request.POST['budgetType']
        fiscalYearStart = int(request.POST['fiscalYearStart'])
        fiscalYearEnd = int(request.POST['fiscalYearEnd'])
        if fiscalYearEnd < fiscalYearStart:
            fiscalYearEnd = fiscalYearStart
        reportType = request.POST['reportType']
        print("b")
    else:
        print("c")
        budgetType = None
        fiscalYearStart = fiscalYearResearchs[0]
        fiscalYearEnd = fiscalYearResearchs[0]
        reportType = 'dashboard'

    if budgetType is None or budgetType == '0':  # เลือกทั้งหมด
        print("d")
        count = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd).count()        
    else:
        print("e")
        count = Research.objects.filter(fiscalYear__gte=fiscalYearStart, fiscalYear__lte=fiscalYearEnd, budgetType=budgetType).count()

    #ปีงบประมาณ
    print("**************************")
    print('fiscalYearResearch')
    print(fiscalYearResearchs)
    print('budgetTypes')
    print(budgetTypes)
    print('budgetType')
    print(budgetType)
    print('fiscalYearStart')
    print(fiscalYearStart)
    print('fiscalYearEnd')
    print(fiscalYearEnd)
    print("count")
    print(count)
    print("**************************")

    dfResearchCount = statistic.getResearchCountSet(budgetType=budgetType, fiscalYearStart=fiscalYearStart,
                                                    fiscalYearEnd=fiscalYearEnd)
    # fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    # fig.show()
    #

    # dfDiv = statistic.getDivisionSet(division=division)
    # dfEdu = statistic.getEducationSet(division=division)
    # dfStatus = statistic.getStatusSet(division=division)
    # dfGender = statistic.getGenderSet(division=division)
    #
    figResearchCount = px.bar(dfResearchCount, x='Year', y='Count', title='งานวิจัยแยกตามปีงบประมาณ')
    figResearchCount.update_layout(autosize=False, width=450, height=350,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    # # paper_bgcolor="aliceblue")
    chartResearchCount = figResearchCount.to_html()

    # figEdu = px.pie(dfEdu, names='Level', values='Count', title='บุคลากรแยกตามระดับการศึกษา')
    # figEdu.update_layout(autosize=False, width=300, height=300,
    #                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    # chartEdu = figEdu.to_html()
    #
    # figStatus = px.pie(dfStatus, names='Status', values='Count', title='บุคลากรแยกตามตำแหน่งทางวิชาการ')
    # figStatus.update_layout(autosize=False, width=300, height=300,
    #                         margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    # chartStatus = figStatus.to_html()
    #
    # figGender = px.bar(dfGender, x='Gender', y='Count', title='บุคลากรแยกตามเพศ')
    # figGender.update_layout(autosize=False, width=300, height=300,
    #                         margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    # chartGender = figGender.to_html()
    #
    # context = {'divisions': divisions, 'division': division, 'dfDiv': dfDiv, 'dfEdu': dfEdu,
    #            'dfStatus': dfStatus, 'dfGender': dfGender,
    #            'chartDiv': chartDiv, 'chartEdu': chartEdu, 'chartStatus': chartStatus, 'chartGender': chartGender,
    #            'count': count, 'reportType': reportType}

    context = {'budgetTypes':budgetTypes, 'budgetType':budgetType,
               'fiscalYearResearch':fiscalYearResearchs,
               'fiscalYearStart':fiscalYearStart, 'fiscalYearEnd':fiscalYearEnd, 'reportType':reportType,
               'dfResearchCount':dfResearchCount,'chartResearchCount':chartResearchCount,
               'count':count,}
    return render(request, 'report/researchReport.html', context)