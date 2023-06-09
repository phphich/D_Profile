from django.shortcuts import render
from datetime import datetime
from django.db.models import Max
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from baseapp.models import *
# from baseapp.forms import *
from workapp.models import *
from workapp import common

from django.contrib import messages
from django.core.paginator import (Paginator, EmptyPage,PageNotAnInteger,)
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

# ******************** Report personnel ***********************

def getDivisionSet():
    divisions = Division.objects.all().order_by('name_th')
    listDivName = []
    listDivCountPersonnel = []
    for div in divisions:
        listDivName.append(div.name_th)
        listDivCountPersonnel.append(div.getCountPersonnel())
    dataFrame = pd.DataFrame({'สาขา': listDivName, 'จำนวน': listDivCountPersonnel}, columns=['สาขา', 'จำนวน'])
    return dataFrame

def getEducationSet():
    personnels = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th')
    levels = Education.objects.all().values('level').distinct()
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

def getStatusSet():
    personnels = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th')
    statuses = Personnel.objects.all().values('status').distinct().order_by('status')
    statusName = []
    statusCount = []
    for s in statuses:
        count = Personnel.objects.filter(status=s['status']).count()
        statusName.append(s['status'])
        statusCount.append(count)
    dataFrameStatus = pd.DataFrame({'Status': statusName, 'Count': statusCount}, columns=['Status', 'Count'])
    return dataFrameStatus

def getGenderSet():
    # personnels = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th')
    maleGender = Personnel.objects.filter(gender='ชาย').count()
    femaleGender = Personnel.objects.filter(gender='หญิง').count()
    # genderSet = [maleGender, femaleGender]
    genderName = []
    genderCount = []
    genderName.append('ชาย')
    genderName.append('หญิง')
    genderCount.append(maleGender)
    genderCount.append(femaleGender)
    dataFrameGender = pd.DataFrame({'Gender': genderName, 'Count': genderCount}, columns=['Gender', 'Count'])
    return dataFrameGender

#ล็อกเอ๊าท์ผ่านระบบ Authen ของ Django
def personnelReport(request, reportType=None):
    reportType = reportType
    if reportType is None:
        reportType = 'dashboard'

    count = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th').count()
    divisions = Division.objects.all().order_by('name_th')
    if divisions is None:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    dataFrame = getDivisionSet()
    fig = px.bar(dataFrame, x='สาขา', y='จำนวน', title='บุคลากรแยกตามสาขา')
    fig.update_layout(autosize=False, width=400, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),paper_bgcolor="white")
                      # paper_bgcolor="aliceblue")
    chart = fig.to_html()

    dataFrameEdu = getEducationSet()
    figEdu = px.pie(dataFrameEdu, names='Level', values='Count', title='บุคลากรแยกตามระดับการศึกษา')
    figEdu.update_layout(autosize=False, width=300, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartEdu = figEdu.to_html()

    dataFrameStatus = getStatusSet()
    figStatus = px.pie(dataFrameStatus, names='Status', values='Count', title='บุคลากรแยกตามตำแหน่งทางวิชาการ')
    figStatus.update_layout(autosize=False, width=350, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),  paper_bgcolor="white")
    chartStatus = figStatus.to_html()

    dataFrameGender = getGenderSet()
    figGender = px.bar(dataFrameGender, x='Gender', y='Count', title='บุคลากรแยกตามเพศ')
    # figGender = px.pie(dataFrameGender, names='Gender', values='Count', title='บุคลากรแยกตามเพศ')
    figGender.update_layout(autosize=False, width=300, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),  paper_bgcolor="white")
    chartGender = figGender.to_html()

    context = {'divisions': divisions, 'dataFrameEdu': dataFrameEdu, 'dataFrameStatus':dataFrameStatus, 'dataFrameGender':dataFrameGender,
               'chart': chart, 'chartEdu': chartEdu, 'chartStatus':chartStatus, 'chartGender':chartGender,
               'count': count,  'reportType':reportType}
    return render(request, 'report/personnelReport.html', context)

