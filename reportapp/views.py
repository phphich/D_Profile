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

#ล็อกเอ๊าท์ผ่านระบบ Authen ของ Django
def personnelReport(request, reportType=None):
    divisions = Division.objects.all().order_by('name_th')
    if divisions is None:
        messages.add_message(request, messages.ERROR, 'ข้อมูลไม่เพียงพอต่อการนำเสนอรายงาน')
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    reportType = reportType
    if reportType is None:
        reportType = 'dashboard'

    divId = request.POST.get('divId')
    if divId == None or int(divId) == 0:
        division = None
    else:
        division = Division.objects.filter(id=divId).first()

    if division is None:
        count = Personnel.objects.all().count()
    else:
        count = Personnel.objects.filter(division=division).count()
    dataFrameDiv = statistic.getDivisionSet(division=division)
    dataFrameEdu = statistic.getEducationSet(division=division)
    dataFrameStatus = statistic.getStatusSet(division=division)
    dataFrameGender = statistic.getGenderSet(division=division)

    figDiv = px.bar(dataFrameDiv, x='Division', y='Count', title='บุคลากรแยกตามสาขา')
    figDiv.update_layout(autosize=False, width=450, height=350,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),paper_bgcolor="white")
                      # paper_bgcolor="aliceblue")
    chartDiv = figDiv.to_html()

    figEdu = px.pie(dataFrameEdu, names='Level', values='Count', title='บุคลากรแยกตามระดับการศึกษา')
    figEdu.update_layout(autosize=False, width=300, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
    chartEdu = figEdu.to_html()

    figStatus = px.pie(dataFrameStatus, names='Status', values='Count', title='บุคลากรแยกตามตำแหน่งทางวิชาการ')
    figStatus.update_layout(autosize=False, width=350, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),  paper_bgcolor="white")
    chartStatus = figStatus.to_html()

    figGender = px.bar(dataFrameGender, x='Gender', y='Count', title='บุคลากรแยกตามเพศ')
    figGender.update_layout(autosize=False, width=300, height=300,
                      margin=dict(l=10, r=10, b=10, t=50, pad=5, ),  paper_bgcolor="white")
    chartGender = figGender.to_html()

    context = {'divisions': divisions, 'division':division,  'dataFrameDiv':dataFrameDiv,  'dataFrameEdu': dataFrameEdu, 'dataFrameStatus':dataFrameStatus, 'dataFrameGender':dataFrameGender,
               'chartDiv': chartDiv, 'chartEdu': chartEdu, 'chartStatus':chartStatus, 'chartGender':chartGender,
               'count': count,  'reportType':reportType}
    return render(request, 'report/personnelReport.html', context)

