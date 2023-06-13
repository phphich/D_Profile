from datetime import datetime
from django.db.models import Max
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from baseapp.models import *
from baseapp.forms import *
from workapp.models import *
from workapp import common
from reportapp import statistic

from django.contrib import messages
from django.core.paginator import (Paginator, EmptyPage,PageNotAnInteger,)
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import os
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

iterm_per_page = 10
# Item.objects.filter(Q(field_a=123) | Q(field_b__in=(3, 4, 5, ))
msgErrorId = 'เป้าหมายที่ท่านระบุ ไม่ปรากฎในระบบหรือท่านไม่มีสิทธิ์ในการเข้าถึง!'

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
    # print("uid in getsession"+ str(uId))
    # print("utype in getsession" + str(uType))


def home(request):
    faculty = Faculty.objects.first()
    if faculty is not None:
        request.session['sess_faculty'] = faculty.name_th
        request.session['sess_university'] = faculty.university
    else:
        request.session['sess_faculty'] = "Faculty: [N/A]"
        request.session['sess_university'] = "University: [N/A]"
    countPersonnel = Personnel.objects.all().count()
    request.session['last_url']= request.path_info
    if countPersonnel == 0:
        messages.add_message(request, messages.INFO, "นี่เป็นการเข้าใช้ระบบเป็นครั้งแรก จำเป็นต้องบันทึกข้อมูลผู้ดูแลระบบเพื่อบริหารจัดระบบในลำดับถัดไป...")
        return  redirect('personnelNew')
    else:
        context = {}
        if Personnel.objects.all().count()> 0:
            count = Personnel.objects.all().count()
            dfDiv = statistic.getDivisionSet()
            figDiv = px.bar(dfDiv, x='Division', y='Count', title='บุคลากรแยกตามสาขา')
            figDiv.update_layout(autosize=False, width=450, height=350,
                                 margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
            chartDiv = figDiv.to_html()

            dfReserchYear = statistic.getResearchFiscalYears()
            yearStart=dfReserchYear[0]
            yearEnd=dfReserchYear[len(dfReserchYear)-1]
            dfResearchBudget = statistic.getResearchBudgetSet(budgetType=None, fiscalYearStart=yearStart, fiscalYearEnd=yearEnd)
            figResearchBudget = px.line(dfResearchBudget, x="Year", y="Budget", title='ทุนวิจัยแยกตามปีงบประมาณ')
            figResearchBudget.update_layout(autosize=False, width=400, height=300,
                                            margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
            chartResearchBudget = figResearchBudget.to_html()

            dfSocialServiceYear = statistic.getSocialServiceFiscalYears()
            yearStart=dfSocialServiceYear[0]
            yearEnd=dfSocialServiceYear[len(dfSocialServiceYear)-1]
            dfSocialService = statistic.getSocialServiceCountSet(budgetType=None, fiscalYearStart=yearStart, fiscalYearEnd=yearEnd)
            figSocialService = px.bar(dfSocialService, x='Year', y='Count', title='จำนวนโครงการบริการทางวิชาการแยกตามปีงบประมาณ')
            figSocialService.update_layout(autosize=False, width=300, height=300,
                                 margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
            chartSocialService= figSocialService.to_html()

            # divisions = Division.objects.all().order_by('name_th')
            dfStatus = statistic.getStatusSet(division=None)
            figStatus = px.pie(dfStatus, names='Status', values='Count', title='บุคลากรแยกตามตำแหน่งทางวิชาการ')
            figStatus.update_layout(autosize=False, width=350, height=350,
                                    margin=dict(l=10, r=10, b=10, t=50, pad=5, ), paper_bgcolor="white")
            chartStatus = figStatus.to_html()

            # dfEdu = statistic.getEducationSet()
            # dfStatus = statistic.getStatusSet()

            context = {'chartDiv': chartDiv, 'chartResearchBudget': chartResearchBudget,
                       'chartSocialService': chartSocialService,'chartStatus':chartStatus,
                       }
        return render(request, 'home.html', context)

# ตรวจสอบ Login
def userAuthen(request):
    if request.method == 'POST':
        form = AuthenForm(data=request.POST)
        userName = request.POST.get("userName")
        userPass = request.POST.get("userPass")
        ## login ด้วย ระบบล็อกอินของ Django
        user = authenticate(username=userName, password=userPass)
        if user is not None:
            login(request, user)
            personnel = Personnel.objects.filter(email=userName).first()
            request.session['userEmail'] = personnel.email
            request.session['userName'] = personnel.firstname_th + " " + personnel.lastname_th
            request.session['userType'] = str(user.groups.first())
            request.session['userId'] = personnel.id
            request.session['userPicture'] = personnel.picture.name
            messages.add_message(request, messages.SUCCESS, "ตรวจสอบสิทธิ์การเข้าใช้ระบบสำเร็จ, ยินดีต้อนรับ: " +
                                 personnel.status + ' ' + personnel.firstname_th + ' ' + personnel.lastname_th +
                                 ' เข้าสู่ระบบ.. ')
            return redirect('home')
        else:
            messages.add_message(request,messages.ERROR, "รหัสผู้ใช้หรือรหัสผ่านไม่ถูกต้อง.!!!")
            context = {'form':form}
            return render(request, 'userAuthen.html', context)
    else:
         form = AuthenForm()
         context = {'form': form}
         return render(request, 'userAuthen.html', context)

#ล็อกเอ๊าท์ผ่านระบบ Authen ของ Django
@login_required(login_url='userAuthen')
def userLogout(request):
    del request.session["userEmail"]
    del request.session["userName"]
    del request.session["userType"]
    del request.session["userId"]
    del request.session['userPicture']
    logout(request)
    return  redirect('userAuthen')

from django.contrib.auth.hashers import make_password
def helpme(request): # เมธอดพิเศษ
    user = User.objects.filter(email='phichayapak.ph@rmuti.ac.th').first()
    group = Group.objects.get_or_create(name='Personnel')
    group = Group.objects.get_or_create(name='Staff')
    group = Group.objects.get_or_create(name='Header')
    group = Group.objects.get_or_create(name='Manager')
    group = Group.objects.get_or_create(name='Administrator')
    if user is not None:  # มีบัญชีผู้ใช้ระบบจริง
        user.password = make_password('12345')
        user.save()
        messages.add_message(request, messages.SUCCESS, 'แก้ไขรหัสผ่านเรียบร้อย ระบบจะพาท่านเข้าระบบใหม่อีกครั้ง')
    else:
        messages.add_message(request, messages.ERROR, 'แก้ไขรหัสผ่านไม่สำเร็จ')
    return redirect('home')

def helpReset(request):
    users = User.objects.all()
    pgroup = Group.objects.filter(name='Personnel').first()
    sgroup = Group.objects.filter(name='Staff').first()
    hgroup = Group.objects.filter(name='Header').first()
    mgroup = Group.objects.filter(name='Manager').first()
    for user in users:
        if user.is_superuser != True: # groups.filter(name='Administrator').exists():
            user.groups.remove(sgroup)
            user.groups.remove(hgroup)
            user.groups.remove(mgroup)
            user.save()
            user.groups.add(pgroup)
    messages.add_message(request, messages.SUCCESS, 'รีเซตระบบเรียบร้อย...')
    return redirect('home')

def devteam(request):
    return  render(request, 'about/devteam.html')
def objective(request):
    return  render(request, 'about/objective.html')


def permissionerror(request):
    return  render(request, 'permissionerror.html')

@login_required(login_url='userAuthen')
def userChgPassword(request):
    # getSession(request)
    # if common.chkPermission(facultyUpdate.__name__, uType=uType) == False:
    #     messages.add_message(request, messages.ERROR, msgErrorPermission)
    #     return redirect('home')
    email = request.session['userEmail']
    personnel = Personnel.objects.filter(email=email).first()
    if request.method == 'POST':
        form = ChgPasswordForm(data=request.POST)
        email = request.POST['email']
        currentPassword =  request.POST['currentPassword']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']
        user = User.objects.filter(email=email).first()
        if user is not None: # มีบัญชีผู้ใช้ระบบจริง
            if user.check_password(currentPassword): # ป้อนรหัสผ่านเดิมถูกต้อง
                if newPassword == confirmPassword:
                    user.password = make_password(newPassword)
                    user.save()
                    messages.add_message(request, messages.SUCCESS,'แก้ไขรหัสผ่านเรียบร้อย ระบบจะพาท่านเข้าระบบใหม่อีกครั้ง')
                    return redirect('userLogout')
                else:
                    messages.add_message(request, messages.ERROR, 'ท่านระบุรหัสผ่านใหม่กับรหัสผ่านที่ยืนยันไม่ตรงกัน ')
            else:
                messages.add_message(request, messages.ERROR, 'ท่านระบุรหัสผ่านเดิมไม่ถูกต้อง ')
        else:
            messages.add_message(request, messages.ERROR, 'ไม่ปรากฏชื่อบัญชีผู้ใช้ระบบตามที่ระบุ ')
    else:
        form = ChgPasswordForm(initial={'email':personnel.email})
    context = {'form':form, 'personnel':personnel}
    return render(request, 'userChgPassword.html', context)

@login_required(login_url='userAuthen')
def userResetPassword(request, id):
    if request.session['userType'] != 'Administrator':
        # messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect('permissionerror')
    request.session['last_url'] = 'home'
    personnel = Personnel.objects.filter(id=id).first()
    getSession(request, dtype='Personnel', did=personnel.id)
    if common.chkPermission(userResetPassword.__name__, uType=uType, uId=uId) == False:
        messages.add_message(request, messages.ERROR, msgErrorPermission)
        return redirect('home')
    if request.method == 'POST':
        form = ChgPasswordForm(data=request.POST)
        email = request.POST['email']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']
        user = User.objects.filter(email=email).first()
        if user is not None: # มีบัญชีผู้ใช้ระบบจริง
            if newPassword == confirmPassword:
                user.password = make_password(newPassword)
                user.save()
                messages.add_message(request, messages.SUCCESS,
                                     'แก้ไขรหัสผ่านเรียบร้อย ระบบจะพาท่านเข้าระบบใหม่อีกครั้ง')
                return redirect('personnelDetail', id=personnel.id)
            else:
                messages.add_message(request, messages.ERROR, 'ท่านระบุรหัสผ่านใหม่กับรหัสผ่านที่ยืนยันไม่ตรงกัน ')
        else:
            messages.add_message(request, messages.ERROR, 'ไม่ปรากฏชื่อบัญชีผู้ใช้ระบบตามที่ระบุ ')
    else:
        form = ResetPasswordForm(initial={'email':personnel.email})
    context = {'form':form, 'personnel':personnel}
    return render(request, 'base/personnel/userResetPassword.html', context)

#Factulty Data
def facultyDetail(request):
    if Personnel.objects.all().count() == 0:
        return redirect('home')
    request.session['last_url']= request.path_info
    faculty = Faculty.objects.first()
    context = {'faculty': faculty}
    return render(request, 'base/faculty/facultyDetail.html', context)

@login_required(login_url='userAuthen')
def facultyUpdate(request):
    getSession(request)
    if common.chkPermission(facultyUpdate.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR, msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    faculty = Faculty.objects.first()
    form = FacultyForm(data=request.POST or None, instance=faculty)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลคณะเรียบร้อย')
            return redirect('facultyDetail')
    else:
        context = {'form':form}
        return render(request, 'base/faculty/facultyUpdate.html', context)

# Division CRUD.
def divisionList(request):
    if Personnel.objects.all().count() == 0:
        return redirect('home')
    request.session['last_url'] = request.path_info
    divisions = Division.objects.all().order_by('name_th')
    context = {'divisions': divisions}
    return render(request, 'base/division/divisionList.html', context)

@login_required(login_url='userAuthen')
def divisionNew(request):
    getSession(request)
    if common.chkPermission(divisionNew.__name__,uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    if request.method == 'POST':
        form = DivisionForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลสาขา/หน่วยงานย่อยใหม่เรียบร้อย')
            return redirect('divisionList')
        else:
            context = {'form': form}
            return render(request, 'base/division/divisionNew.html', context)
    else:
        form = DivisionForm()
        context = {'form': form}
        return render(request, 'base/division/divisionNew.html', context)

@login_required(login_url='userAuthen')
def divisionUpdate(request, id):
    division = Division.objects.filter(id=id).first()
    if division is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request)
    if common.chkPermission(divisionUpdate.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    form = DivisionForm(data=request.POST or None, instance=division)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'แก้ไขข้อมูลสาขา/หน่วยงานย่อยเรียบร้อย')
            return redirect('divisionList')
        else:
            context = {'form': form}
            return render(request, 'base/division/divisionUpdate.html')
    else:
        context = {'form': form}
        return render(request, 'base/division/divisionUpdate.html', context)

@login_required(login_url='userAuthen')
def divisionDelete(request, id):
    division = Division.objects.filter(id=id).first()
    if division is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request)
    if common.chkPermission(divisionDelete.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    form = DivisionForm(data=request.POST or None, instance=division)
    if request.method == 'POST':
        division.delete()
        messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลสาขา/หน่วยงานย่อยที่เลือกเรียบร้อย')
        return redirect('divisionList')
    else:
        if division.getCountPersonnel() > 0 or division.getCountCurriculum() > 0: #มีบุคลากร หรือหลักสูตรอยู่
            messages.add_message(request, messages.ERROR, 'ไม่สามารถลบข้อมูลสาขา/หน่วยงานย่อยที่เลือกได้ เนื่องจากมีบุคลากรหรือหลักสูตรในสาขา/หน่วยงานย่อยนี้')
            return redirect('divisionList')
        else:
            form.deleteForm()
            context = {'form': form, 'division': division}
            return render(request, 'base/division/divisionDelete.html', context)

# Curriculum CRUD.
def curriculumList(request):
    if Personnel.objects.all().count() == 0:
        return redirect('home')
    request.session['last_url'] = request.path_info
    curriculums = Curriculum.objects.all().order_by('name_th')
    context = {'curriculums': curriculums}
    return render(request, 'base/curriculum/curriculumList.html', context)

@login_required(login_url='userAuthen')
def curriculumNew(request):
    getSession(request)
    if common.chkPermission(curriculumNew.__name__, uType=uType) ==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    if request.method == 'POST':
        form = CurriculumForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'เพิ่มข้อมูลหลักสูตรใหม่เรียบร้อย')
            return redirect('curriculumList')
        else:
            context = {'form': form}
            return render(request, 'base/curriculum/curriculumNew.html', context)
    else:
        curriculumnYear = datetime.datetime.now().year + 543
        form = CurriculumForm(initial={'curriculumYear':curriculumnYear})
        context = {'form': form}
        return render(request, 'base/curriculum/curriculumNew.html', context)

@login_required(login_url='userAuthen')
def curriculumUpdate(request, id):
    curriculum = Curriculum.objects.filter(id=id).first()
    if curriculum is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request)
    if common.chkPermission(curriculumUpdate.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    form = CurriculumForm(data=request.POST or None, instance=curriculum)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'แก้ไขข้อมูลหลักสูตรเรียบร้อย')
            return redirect('curriculumList')
        else:
            context = {'form': form}
            return render(request, 'base/curriculum/curriculumUpdate.html')
    else:
        context = {'form': form}
        return render(request, 'base/curriculum/curriculumUpdate.html', context)

@login_required(login_url='userAuthen')
def curriculumDelete(request, id):
    curriculum = Curriculum.objects.filter(id=id).first()
    if curriculum is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request)
    if common.chkPermission(curriculumDelete.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    form = CurriculumForm(data=request.POST or None, instance=curriculum)
    if request.method == 'POST':
        if curriculum.getCountCurrAffiliation() > 0: #มีผู้รับผิดชอบหลักสูตรอยู่
            messages.add_message(request, messages.ERROR,'ไม่สามารถลบข้อมูลหลักสูตรที่เลือกได้ เนื่องจากได้กำหนดผู้รับผิดชอบหลักสูตรนี้ไว้แล้ว')
            return redirect('curriculumList')
        else:
            curriculum.delete()
            messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลหลักสูตรที่เลือกเรียบร้อย')
            return redirect('curriculumList')
    else:
        form.deleteForm()
        context = {'form': form, 'curriculum': curriculum}
        return render(request, 'base/curriculum/curriculumDelete.html', context)

# Personnel CRUD.
def personnelList(request, pageNo=None, divId=None):
    if Personnel.objects.all().count() == 0:
        return redirect('home')
    # if 'userType' not in request.session:
    #     return redirect('userAuthen')
    request.session['last_url'] = request.path_info
    if pageNo == None:
        pageNo = 1
    divId = request.POST.get('divId')
    if divId == None or int(divId)== 0:
        division=None
    else:
        division = Division.objects.filter(id=divId).first()
        pageNo = 1

    # if request.session['userType'] != 'Staff':
    onlyStaff = False
    if 'userType' not in request.session or request.session['userType'] != 'Staff':
        divisions = Division.objects.all().order_by('name_th')
        if division is None:
            personnels = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th')
        else:
            personnels = division.getPersonnels()
        personnels_page = Paginator(personnels, iterm_per_page)
        count = personnels.count()
        context = {'divisions':divisions, 'division':division, 'personnels': personnels_page.page(pageNo), 'count':count,}
    else:
        recorder = Personnel.objects.filter(id=request.session['userId']).first()
        divisions = recorder.getDivisionResponsible()
        outside = recorder.getOutsideResponsible()
        if outside == True:
            onlyStaff = True
            divisions.append(recorder.division)
        personnels = Personnel.objects.filter(division__in=divisions)
        personnels_page = Paginator(personnels, iterm_per_page)
        count = personnels.count()
        context = {'personnels': personnels_page.page(pageNo), 'count': count, 'onlyStaff':onlyStaff, 'recorder':recorder }
    return render(request, 'base/personnel/personnelList.html', context)

# @login_required(login_url='userAuthen')
def personnelNew(request):
    if 'userType' in request.session:
        recorder = Personnel.objects.filter(id=request.session['userId']).first()
        if request.session['userType'] == 'Staff':
            getSession(request, dtype='Personnel', did=recorder.id)
            if common.chkPermission(personnelNew.__name__, uType=uType, uId=uId)==False:
                messages.add_message(request, messages.ERROR,msgErrorPermission)
                return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    divisionCount = Division.objects.all().count()
    personnelCount = Personnel.objects.all().count()
    if personnelCount > 0:
        if 'userId' not in request.session:
            return redirect('userAuthen')
    else:
        recorder = None
    if divisionCount == 0:
        division = Division(name_th="สำนักงานคณะ", name_en="Office", name_sh="")
        division.save()
    if request.method == 'POST':
        if request.session['userType'] == 'Administrator' or personnelCount==0:
            form = PersonnelForm(data=request.POST or None, files=request.FILES)
        else:
            form = PersonnelForm(staffId=request.session['userId'], data=request.POST or None, files=request.FILES)
        passwd = request.POST['passwd']
        confpasswd = request.POST['confpasswd']

        if form.is_valid():
            if passwd != confpasswd:
                messages.add_message(request, messages.WARNING, "กำหนดรหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน!")
                context = {'form': form}
                return render(request, 'base/personnel/personnelNew.html', context)
            newForm = form.save(commit=False)
            email = newForm.email
            filepath = newForm.picture.name
            filepath = filepath.replace(' ', '_')
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = 'images/personnels/' + filenames[len(filenames) - 1]
            newForm.save()
            personnel = Personnel.objects.filter(email=email).first()
            newfilename = 'images/personnels/' + str(personnel.id) + ext
            personnel.picture.name = newfilename
            personnel.save()
            if personnelCount == 0: # กรณีบันทึกเป็นรายแรก  (Admin)
                personnel.recorderId = personnel.id
                personnel.editorId = personnel.id
                personnel.save()
                group = Group.objects.create(name='Personnel')
                group = Group.objects.create(name='Staff')
                group = Group.objects.create(name='Header')
                group = Group.objects.create(name='Manager')
                group = Group.objects.create(name='Administrator')
                # group.save()
            try:
                if os.path.exists('static/' + personnel.picture.name):
                    os.remove('static/' + personnel.picture.name)  # file exits, delete it
                os.rename('static/' + filename, 'static/' + personnel.picture.name)
            except:
                messages.add_message(request, messages.WARNING, 'มีปัญหาในการบันทึกรูปภาพของบุคลากร')
            # สร้าง user ในระบบ authen ของ Django ---
            id = personnel.email
            email = personnel.email
            password = passwd
            user = User.objects.create_user(id, email, password)
            user.first_name = personnel.firstname_en
            user.last_name = personnel.lastname_en
            if personnelCount == 0: # กรณีบันทึกเป็นรายแรก  (Admin)
                user.is_superuser = True
                user.is_staff = True
                group = Group.objects.get(name='Administrator')
                user.groups.add(group)
            else:
                user.is_superuser = False
                user.is_staff = True
                group = Group.objects.get(name='Personnel')
                user.groups.add(group)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลบุคลากรรายใหม่เรียบร้อย')
            return redirect('personnelList', pageNo=1)
        else:
            countPersonnel = Personnel.objects.all().count()
            if countPersonnel ==  0:
                firstTime = True
            else:
                firstTime = False
            context = {'form': form, 'fistTime':firstTime}
            return render(request, 'base/personnel/personnelNew.html', context)
    else:
        if request.session['userType'] == 'Administrator':
            form = PersonnelForm()
        else:
            form = PersonnelForm(userType=request.session['userType'],userId=request.session['userId'])
        countPersonnel = Personnel.objects.all().count()
        if countPersonnel == 0:
            firstTime = True
            division = Division.objects.first();
            form.initial={'division':division, 'recorderId':'0000', 'editorId':'0000'}
        else:
            firstTime = False
            form.initial = {'recorderId': recorder.id, 'editorId': recorder.id}
        context = {'form': form, 'firstTime':firstTime}
        return render(request, 'base/personnel/personnelNew.html', context)

@login_required(login_url='userAuthen')
def personnelDetail(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    if personnel is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Personnel', did=personnel.id)
    if common.chkPermission(personnelDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    context = {'personnel': personnel}
    return render(request, 'base/personnel/personnelDetail.html', context)

@login_required(login_url='userAuthen')
def personnelUpdate(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    if personnel is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
    getSession(request,dtype='Personnel', did=personnel.id)
    if common.chkPermission(personnelUpdate.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    oldpicture = personnel.picture.name  # รูปเดิม
    oldemail = personnel.email  # อีเมล์เดิม
    olddivision = personnel.division
    if request.method == 'POST':
        if request.session['userType'] == 'Administrator':
            form = PersonnelForm(data=request.POST, instance=personnel, files=request.FILES)
        else:
            form = PersonnelForm(userType=request.session['userType'], userId=request.session['userId'], data=request.POST, instance=personnel, files=request.FILES)
        if form.is_valid():
            updateForm = form.save(commit=False)
            updateDivision = request.POST['division']
            if str(updateDivision) != str(olddivision.id) and personnel.getHeader() is not None: # เป็นหัวหน้าแต่เปลี่ยนสาขา
                messages.add_message(request, messages.ERROR, 'มีการเปลี่ยนสาขา/หน่วยงานย่อยใหม่ให้แก่บุคลากร ในขณะที่บุคลากรรายนี้เป็นหัวหน้าสาขา/หน่วยงานปัจจุบันอยู่')
                return redirect(request.session['last_url'])
            id = updateForm.id
            if updateForm.picture.name != oldpicture:  # หากเลือกรูปใหม่
                if os.path.exists('static/' + oldpicture):  # delete older picture profile
                    os.remove('static/' + oldpicture)
                filepath = updateForm.picture.name
                filepath = filepath.replace(' ', '_')
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = 'images/personnels/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหลด
                updateForm.save()
                personnel = Personnel.objects.filter(id=id).first()
                newfilename = 'images/personnels/' + str(personnel.id) + ext  # ชื่อไฟล์ที่ระบบกำหนด
                personnel.picture.name = newfilename  # ต้องอัพเดท เผื่อกรณีที่เปลี่ยนชนิดไฟล์ภาพ
                personnel.save()
                os.rename('static/' + filename, 'static/' + personnel.picture.name)
            else:
                updateForm.save()
                personnel.editorId = recorder.id
                personnel.editDate = datetime.datetime.now()
                personnel.save()
                messages.add_message(request, messages.SUCCESS, 'แก้ไขข้อมูลบุคลากรเรียบร้อย')
            return redirect('personnelDetail', personnel.id)
        else:
            user = User.objects.filter(username=oldemail).first()
            userType = user.groups.first()
            context = {'form': form, 'personnel': personnel, 'userType':userType}
            return render(request, 'base/personnel/personnelUpdate.html', context)
    else:
        user = User.objects.filter(username=oldemail).first()
        user_group = user.groups.first()
        userType = str(user_group)
        if request.session['userType'] == 'Administrator':
            form = PersonnelForm(instance=personnel)
        else:
            form = PersonnelForm(userType=request.session['userType'], userId=request.session['userId'], instance=personnel)
        form.updateForm()
        context = {'form': form, 'personnel': personnel, 'userType':userType}
        return render(request, 'base/personnel/personnelUpdate.html', context)

@login_required(login_url='userAuthen')
def personnelDelete(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    if personnel is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Personnel', did=personnel.id)
    if common.chkPermission(personnelDelete.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    picturefile = personnel.picture.name
    form = PersonnelForm(data=request.POST or None, instance=personnel)
    if request.method == 'POST':
        error=False
        if personnel.getCountBasicTransaction()>0:
            error = True
        if Leave.getCountPersonLeave(personnel) > 0 or \
                Training.getCountPersonTraining(personnel)>0 or \
                Performance.getCountPersonPerformance(personnel)>0 or \
                Research.getCountPersonResearch(personnel) > 0 or \
                SocialService.getCountPersonSocialService(personnel) > 0 or \
                Command.getCountPersonCommand(personnel) > 0:
            error = True
        if error == True:
            messages.add_message(request, messages.ERROR,'ไม่สามารถลบข้อมูลบุคลากรที่เลือกได้ เนื่องจากได้ข้อมูลบุคลากรรายนี้ได้ถูกนำไปใช้ร่วมกันข้อมูลในส่วนอื่น ๆ แล้ว')
            return redirect(request.session['last_url'])
        else:
            if personnel.getHeader() is not None:
                messages.add_message(request, messages.ERROR, 'ไม่สามารถลบข้อมูลบุคลากรที่เลือกได้ เนื่องจากได้ข้อมูลบุคลากรรายนี้ถูกกำหนดให้เป็นหัวหน้าสาขา/หน่วยงานย่อยอยู่')
                return redirect(request.session['last_url'])
            elif personnel.getManager() is not None:
                messages.add_message(request, messages.ERROR, 'ไม่สามารถลบข้อมูลบุคลากรที่เลือกได้ เนื่องจากได้ข้อมูลบุคลากรรายนี้ถูกกำหนดให้เป็นผู้บริหารหน่วยงานย่อยอยู่')
                return redirect(request.session['last_url'])
            else:
                user = User.objects.filter(username=personnel.email).first()
                user.delete()
                pid = personnel.id
                admin = User.groups.filter(user_set__groups='Administrator').first()
                useRecorder = Personnel.objects.filter(recorderId=pid) #ดึงรายชื่อบุคลากรที่เคยถูกบันทึกข้อมูลด้วยบุคลากรรายที่จะลบ
                for use in useRecorder:
                    use.recorderId = use.id #เปลี่ยนข้อมูลคนบันทึกเป็นเจ้าของข้อมูล
                    use.save()
                useEditor = Personnel.objects.filter(editorId=pid)
                for use in useEditor:
                    use.editorId = use.id
                    use.save()
                personnel.delete()
                try:
                    if os.path.exists('static/' + picturefile):
                        os.remove('static/' + picturefile)  # file exits, delete it
                except:
                    messages.add_message(request, messages.SUCCESS, 'พบปัญหาการลบไฟล์รูปภาพของบุคลากร')
                messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลบุคลากรที่เลือกเรียบร้อย')
                return redirect('personnelList', pageNo=1)
    else:
        form.deleteForm()
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/personnel/personelDelete.html', context)
# *******************************
# Education CRUD.
@login_required(login_url='userAuthen')
def educationList(request, divisionId=None, personnelId=None):
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if request.session['userType'] == "Personnel":
        context = {'personnel': recorder}
    else:
        division = None
        personnel = None
        outside=False
        if request.session['userType'] == 'Staff':
            outside = recorder.getOutsideResponsible()
            divisions = recorder.getDivisionResponsible()
            if outside == True: #กรณีที่ผู้รับชอบข้อมูลไม่ได้อยู่ในสาขา/หน่วยงานย่อยที่รับผิดชอบ
                divisions.append(recorder.division)
            division = divisions[0]
        elif request.session['userType'] == 'Header':
            divisions = [recorder.division]
            division = recorder.division
        else: #Manager, Administrator
            divisions = Division.objects.all().order_by('name_th')
            division = divisions.first()

        onlyStaff = False
        if request.method == 'POST':
            if 'personnelId' in request.POST:
                personnelId = request.POST['personnelId']
                personnel = Personnel.objects.filter(id=personnelId).first()
                division = personnel.division
                if divisionId == recorder.division.id and outside == True: #ต้องแสดงชื่อเฉพาะ Staff
                    onlyStaff = True
            else:
                divisionId = request.POST['divisionId']
                division = Division.objects.filter(id=divisionId).first()
                if str(divisionId) == str(recorder.division.id) and outside == True: #ต้องแสดงชื่อเฉพาะ Staff
                    onlyStaff = True
                    personnel = recorder
                else:
                    personnel = division.getPersonnels().first()
        else: #เข้ามาครั้งแรก
            if divisionId is not None: # กรณี redirect มาจากการ New
                division = Division.objects.get(id=divisionId)
                personnel = Personnel.objects.get(id=personnelId)
            else:
                personnel = division.getPersonnels().first()
        context = {'divisions': divisions, 'division': division, 'personnel': personnel, 'onlyStaff':onlyStaff, 'recorder':recorder}
    return render(request, 'base/education/educationList.html', context)

@login_required(login_url='userAuthen')
def educationNew(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    if personnel is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Education', did=personnel.id)
    if common.chkPermission(educationNew.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if request.method == 'POST':
        form = EducationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลการศึกษาเรียบร้อย')
            return redirect('educationList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/education/educationNew.html', context)
    else:
        form = EducationForm(initial={'personnel': personnel, 'recorder': recorder, 'editor':recorder})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/education/educationNew.html', context)

@login_required(login_url='userAuthen')
def educationDetail(request, id):
    education = Education.objects.filter(id=id).first()
    if education is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Education', did=education.id)
    if common.chkPermission(educationDetail.__name__, uType=uType, uId=uId, docType=docType, docId=docId) == False:
        messages.add_message(request, messages.ERROR, msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    context = {'education': education}
    return render(request, 'base/education/educationDetail.html', context)

@login_required(login_url='userAuthen')
def educationUpdate(request, id):
    education = Education.objects.filter(id=id).first()
    if education is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Education', did=education.id)
    if common.chkPermission(educationUpdate.__name__, uType=uType, uId=uId, docType=docType, docId=docId) == False:
        messages.add_message(request, messages.ERROR, msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    personnel = education.personnel
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    form = EducationForm(data=request.POST or None, instance=education)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            education.editor = recorder
            education.editDate = datetime.datetime.now()
            education.save()
            messages.add_message(request, messages.SUCCESS, 'แก้ไขข้อมูลการศึกษาเรียบร้อย')
            return redirect('educationList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/education/educationUpdate.html', context)
    else:
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/education/educationUpdate.html', context)

@login_required(login_url='userAuthen')
def educationDelete(request, id):
    education =  Education.objects.filter(id=id).first()
    if education is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Education', did=education.id)
    if common.chkPermission(educationDelete.__name__, uType=uType, uId=uId, docType=docType, docId=docId) == False:
        messages.add_message(request, messages.ERROR, msgErrorPermission)
        return redirect(request.session['last_url'])
    personnel = education.personnel
    form = EducationForm(instance=education)
    if request.method == 'POST':
        divisions = Division.objects.all().order_by('name_th')
        education.delete()
        messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลการศึกษาที่เลือกเรียบร้อย')
        return redirect('educationList', divisionId=personnel.division.id, personnelId=personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'personnel': education.personnel}
        return render(request, 'base/education/educationDelete.html', context)

# Expertise CRUD.
@login_required(login_url='userAuthen')
def expertiseList(request, divisionId=None, personnelId=None):
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if request.session['userType'] == "Personnel":
        context = {'personnel': recorder}
    else:
        division = None
        personnel = None
        outside = False
        if request.session['userType'] == 'Staff':
            outside = recorder.getOutsideResponsible()
            divisions = recorder.getDivisionResponsible()
            if outside == True: #กรณีที่ผู้รับชอบข้อมูลไม่ได้อยู่ในสาขา/หน่วยงานย่อยที่รับผิดชอบ
                divisions.append(recorder.division)
            division = divisions[0]
        elif request.session['userType'] == 'Header':
            divisions = [recorder.division]
            division = recorder.division
        else: #Manager, Administrator
            divisions = Division.objects.all().order_by('name_th')
            division = divisions.first()

        onlyStaff = False
        if request.method == 'POST':
            if 'personnelId' in request.POST:
                personnelId = request.POST['personnelId']
                personnel = Personnel.objects.filter(id=personnelId).first()
                division = personnel.division
                if divisionId == recorder.division.id and outside == True: #ต้องแสดงชื่อเฉพาะ Staff
                    onlyStaff = True
            else:
                divisionId = request.POST['divisionId']
                division = Division.objects.filter(id=divisionId).first()
                if str(divisionId) == str(recorder.division.id) and outside == True: #ต้องแสดงชื่อเฉพาะ Staff
                    onlyStaff = True
                    personnel = recorder
                else:
                    personnel = division.getPersonnels().first()
        else: #เข้ามาครั้งแรก
            if divisionId is not None: # กรณี redirect มาจากการ New
                division = Division.objects.get(id=divisionId)
                personnel = Personnel.objects.get(id=personnelId)
            else:
                personnel = division.getPersonnels().first()
        context = {'divisions': divisions, 'division': division, 'personnel': personnel, 'onlyStaff':onlyStaff, 'recorder':recorder}
    return render(request, 'base/expertise/expertiseList.html', context)

@login_required(login_url='userAuthen')
def expertiseNew(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    if personnel is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Expertise', did=personnel.id)
    if common.chkPermission(expertiseNew.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if request.method == 'POST':
        form = ExpertiseForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลความเชี่ยวชาญเรียบร้อย')
            return redirect('expertiseList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/expertise/expertiseNew.html', context)
    else:
        form = ExpertiseForm(initial={'personnel': personnel, 'recorder': recorder, 'editor':recorder})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/expertise/expertiseNew.html', context)

@login_required(login_url='userAuthen')
def expertiseDetail(request, id):
    expertise= Expertise.objects.filter(id=id).first()
    if expertise is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Expertise', did=expertise.id)
    if common.chkPermission(expertiseDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    context = {'expertise': expertise}
    return render(request, 'base/expertise/expertiseDetail.html', context)

@login_required(login_url='userAuthen')
def expertiseUpdate(request, id):
    expertise = Expertise.objects.filter(id=id).first()
    if expertise is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Expertise', did=expertise.id)
    if common.chkPermission(expertiseUpdate.__name__, uType=uType, uId=uId, docType=docType, docId=docId) == False:
        messages.add_message(request, messages.ERROR, msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    personnel = expertise.personnel
    form = ExpertiseForm(data=request.POST or None, instance=expertise)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            expertise.editor = recorder
            expertise.editDate = datetime.datetime.now()
            expertise.save()
            messages.add_message(request, messages.SUCCESS, 'แก้ไขข้อมูลความเชี่ยวชาญเรียบร้อย')
            return redirect('expertiseList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')
            context = {'form': form, 'personnel': expertise}
            return render(request, 'base/expertise/expertiseUpdate.html', context)
    else:
        context = {'form': form, 'personnel': expertise}
        return render(request, 'base/expertise/expertiseUpdate.html', context)

@login_required(login_url='userAuthen')
def expertiseDelete(request, id):
    expertise = Expertise.objects.filter(id=id).first()
    personnel = expertise.personnel
    form = ExpertiseForm(instance=expertise)
    if request.method == 'POST':
        divisions = Division.objects.all().order_by('name_th')
        expertise.delete()
        messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลความเชี่ยวชาญที่เลือกเรียบร้อย')
        return redirect('expertiseList', divisionId=personnel.division.id, personnelId=personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'personnel': expertise.personnel}
        return render(request, 'base/expertise/expertiseDelete.html', context)

# CurrAffiliation CRUD.
@login_required(login_url='userAuthen')
def currAffiliationList(request, curriculumId = None):
    curriculum = None
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if request.method == 'POST':
        if 'action' in request.POST:
            form = CurrAffiliationForm(data=request.POST, initial={'recorder':recorder})
            if form.is_valid():
                newForm = form.save(commit=False)
                person = Personnel.objects.filter(id=newForm.personnel.id).first()
                curriculum = Curriculum.objects.filter(id=newForm.curriculum.id).first()
                currAffs  = curriculum.getCurrAffiliation()
                duplicate = False
                for currAff in currAffs:
                    if currAff.personnel == person :
                        messages.add_message(request, messages.ERROR, 'บุคลากรที่เลือกมีรายชื่อในการบริหารหลักสูตรนี้อยู่แล้ว')
                        duplicate = True
                        break
                if duplicate == False:
                    newForm.save()
                    messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลผู้บริหารหลักสูตรเรียบร้อย')
            else:
                messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')
    curriculums = Curriculum.objects.all().order_by('name_th')
    if request.method == 'POST':
        curriculumId = request.POST['curriculumId']
    if curriculumId is not None:
        curriculum = Curriculum.objects.filter(id=curriculumId).first()
    else:
        curriculum = curriculums.first()
    form = CurrAffiliationForm(initial={'curriculum': curriculum, 'recorder': recorder})
    context = {'curriculums': curriculums, 'curriculum': curriculum, 'form': form}
    return render(request, 'base/currAffiliation/currAffiliationList.html', context)

@login_required(login_url='userAuthen')
def currAffiliationDelete(request,id):
    currAffiliation = CurrAffiliation.objects.filter(id=id).first()
    curriculum = currAffiliation.curriculum
    currAffiliation.delete()
    messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลผู้บริหารหลักสูตรที่เลือกเรียบร้อย')
    return redirect('currAffiliationList', curriculumId=curriculum.id)

# Responsible CRUD.
@login_required(login_url='userAuthen')
def responsibleList(request, pageNo=None):
    if pageNo == None:
        pageNo = 1
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if request.method == 'POST':
        form = ResponsibleForm(data=request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            personnel = Personnel.objects.filter(id=newForm.personnel.id).first()
            division = Division.objects.filter(id=newForm.division.id).first()
            # responsibles = division.getResponsible()  # รายชื่อผู้รับผิดชอบทั้งหมดของสาขานั้นในระบบ
            responsibles = personnel.getDivisionResponsible()
            duplicate = False
            for responer in responsibles:
                if responer == division:
                    duplicate = True
                    break
            if duplicate == True:
                messages.add_message(request, messages.ERROR,
                                    'บุคลากรที่เลือกเป็นผู้มีรายชื่อรับผิดชอบข้อมูลสาขา/หน่วยงานย่อยนี้อยู่แล้ว')
            elif personnel.getHeader() is not None :  # บุคลากรคนนั้นเป็นหัวหน้าอยู่แล้ว
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกเป็นหัวหน้าสาขา/หน่วยงานย่อย')
            elif personnel.getManager() is not None:  # บุคลากรคนนั้นเป็นผู้บริหารอยู่แล้ว
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกเป็นผู้บริหารหน่วยงาน')
            else:
            # if duplicate == False:
                newForm.save()
                email = personnel.email
                user = User.objects.filter(email=email).first()
                user.is_superuser = False
                user.is_staff = True
                pgroup = Group.objects.get(name='Personnel')
                user.groups.remove(pgroup)
                hgroup = Group.objects.get(name='Staff')
                user.groups.add(hgroup)
                user.save()
                messages.add_message(request, messages.SUCCESS,
                                     'บันทึกข้อมูลผู้รับผิดชอบข้อมูลสาขา/หน่วยงานย่อยเรียบร้อย')
        else:
            messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')

    responsibles = Responsible.objects.all().order_by('personnel__firstname_th','personnel__lastname_th', 'division__name_th',)
    responsibles_page = Paginator(responsibles, iterm_per_page)
    count = responsibles.count
    form = ResponsibleForm(initial={'recorder': recorder})
    context = {'responsibles':responsibles_page.page(pageNo), 'count':count, 'form': form}
    return render(request, 'base/responsible/responsibleList.html', context)

@login_required(login_url='userAuthen')
def responsibleDelete(request,id):
    responsible = Responsible.objects.filter(id=id).first()
    user=User.objects.filter(email=responsible.personnel.email).first()
    personnel = Personnel.objects.filter(email=user.email).first()
    responsible.delete()
    if personnel.getDivisionResponsible() is None:
        rgroup = Group.objects.get(name='Staff')
        user.groups.remove(rgroup)
        pgroup = Group.objects.get(name='Personnel')  # ให้ group กลับคืนเป็นบุคลากร
        user.groups.add(pgroup)
    messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลผู้รับผิดชอบข้อมูลสาขา/หน่วยงานย่อยที่เลือกเรียบร้อย')
    return redirect('responsibleList')

# Header CRUD.
@login_required(login_url='userAuthen')
def headerList(request, pageNo=None):
    if pageNo == None:
        pageNo = 1
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if request.method == 'POST':
        form = HeaderForm(data=request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            division = Division.objects.filter(id=newForm.division.id).first()
            personnel = Personnel.objects.filter(id=newForm.personnel.id).first()
            if len(personnel.getDivisionResponsible()) !=0 :  # บุคลากรคนนั้นเป็นนผู้รับผิดชอบข้อมูล
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกเป็นเจ้าหน้าที่ผู้รับผิดชอบข้อมูลหัวหน้าสาขา/หน่วยงานย่อย')
            elif division.getHeader() is not None:  # สาขานั้นมีหัวหน้าแล้ว
                messages.add_message(request, messages.ERROR,
                                     'สาขา/หน่วยงานย่อยที่เลือกมีการกำหนดผู้เป็นหัวหน้าไปแล้ว')
            elif personnel.getHeader() is not None :  # บุคลากรคนนั้นเป็นหัวหน้าอยู่แล้ว
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกเป็นหัวหน้าสาขา/หน่วยงานย่อยอยู่แล้ว')
            elif personnel.getManager() is not None:  # บุคลากรคนนั้นเป็นผู้บริหารอยู่แล้ว
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกเป็นผู้บริหารหน่วยงาน')
            elif personnel.division != division:  # บุคลากรคนนั้นไม่ได้สังกัดสาขาที่เลือก
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกไม่ได้สังกัดในสาขาที่จะกำหนดให้เป็นหัวหน้า')
            else:
                newForm.save()
                email = personnel.email
                user = User.objects.filter(email=email).first()
                user.is_superuser = False
                user.is_staff = True
                pgroup = Group.objects.get(name='Personnel')
                user.groups.remove(pgroup)
                hgroup = Group.objects.get(name='Header')
                user.groups.add(hgroup)
                user.save()
                messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลหัวหน้าสาขา/หน่วยงานย่อยเรียบร้อย')
        else:
            messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')
    headers = Header.objects.all().order_by('division__name_th', 'personnel__firstname_th','personnel__lastname_th')
    headers_page = Paginator(headers, iterm_per_page)
    count = headers.count
    form = HeaderForm(initial={'recorder': recorder})
    context = {'headers':headers_page.page(pageNo), 'count':count, 'form': form}
    return render(request, 'base/header/headerList.html', context)

@login_required(login_url='userAuthen')
def headerDelete(request,id):
    header = Header.objects.filter(id=id).first()
    user = User.objects.filter(email=header.personnel.email).first()
    header.delete()
    hgroup = Group.objects.get(name='Header')
    user.groups.remove(hgroup)
    pgroup = Group.objects.get(name='Personnel') # ให้ group กลับคืนเป็นบุคลากร
    user.groups.add(pgroup)
    messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลหัวหน้าสาขา/หน่วยงานย่อยที่เลือกเรียบร้อย')
    return redirect('headerList')

# Header CRUD.
@login_required(login_url='userAuthen')
def managerList(request, pageNo=None):
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if request.method == 'POST':
        form = ManagerForm(data=request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            personnel = Personnel.objects.filter(id=newForm.personnel.id).first()
            if len(personnel.getDivisionResponsible()) !=0 :  # บุคลากรคนนั้นเป็นนผู้รับผิดชอบข้อมูล
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกเป็นเจ้าหน้าที่ผู้รับผิดชอบข้อมูลหัวหน้าสาขา/หน่วยงานย่อย')
            elif personnel.getHeader() is not None :  # บุคลากรคนนั้นเป็นหัวหน้าอยู่แล้ว
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกเป็นหัวหน้าสาขา/หน่วยงานย่อย')
            elif personnel.getManager() is not None:  # บุคลากรคนนั้นเป็นผู้บริหารอยู่แล้ว
                messages.add_message(request, messages.ERROR,
                                     'บุคลากรที่เลือกเป็นผู้บริหารหน่วยงานอยู่แล้ว')
            else:
                newForm.save()
                email = personnel.email
                user = User.objects.filter(email=email).first()
                user.is_superuser = False
                user.is_staff = True
                pgroup = Group.objects.get(name='Personnel')
                user.groups.remove(pgroup)
                mgroup = Group.objects.get(name='Manager')
                user.groups.add(mgroup)
                user.save()
                messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลผู้บริหารหน่วยงานเรียบร้อย')
        else:
            messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')
    managers = Manager.objects.all().order_by('personnel__firstname_th','personnel__lastname_th')
    count = managers.count
    form = ManagerForm(initial={'recorder': recorder})
    context = {'managers':managers, 'count':count, 'form': form}
    return render(request, 'base/manager/managerList.html', context)

@login_required(login_url='userAuthen')
def managerDelete(request,id):
    manager = Manager.objects.filter(id=id).first()
    user = User.objects.filter(email=manager.personnel.email).first()
    manager.delete()
    mgroup = Group.objects.get(name='Manager')
    user.groups.remove(mgroup)
    pgroup = Group.objects.get(name='Personnel')  # ให้ group กลับคืนเป็นบุคลากร
    user.groups.add(pgroup)
    messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลผู้บริหารที่เลือกเรียบร้อย')
    return redirect('managerList')

