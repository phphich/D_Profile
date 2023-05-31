from datetime import datetime
from django.db.models import Max
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from baseapp.models import *
from baseapp.forms import *
from workapp.models import *

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
    print("uid in getsession"+ str(uId))
    print("utype in getsession" + str(uType))

def home(request):
    getSession(request, dtype='Personnel', did=23)
    print("uid in home " + str(uId))
    print("utype in home " + str(uType))
    print("dtype in home " + str(docType))
    print("did in home " + str(docId))

    faculty = Faculty.objects.first()
    if faculty is not None:
        request.session['sess_faculty'] = faculty.name_th
        request.session['sess_university'] = faculty.university
    else:
        request.session['sess_faculty'] = "Faculty: [N/A]"
        request.session['sess_university'] = "University: [N/A]"
    countPersonnel = Personnel.objects.all().count()
    if countPersonnel == 0:
        messages.add_message(request, messages.INFO, "นี่เป็นการเข้าใช้ระบบเป็นครั้งแรก จำเป็นต้องบันทึกข้อมูลผู้ดูแลระบบเพื่อบริหารจัดระบบในลำดับถัดไป...")
        return  redirect('personnelNew')
    else:
        return render(request, 'home.html')

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
            personnel = Personnel.objects.get(email=userName)
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
    if user is not None:  # มีบัญชีผู้ใช้ระบบจริง
        user.password = make_password('12345')
        user.save()
        messages.add_message(request, messages.SUCCESS, 'แก้ไขรหัสผ่านเรียบร้อย ระบบจะพาท่านเข้าระบบใหม่อีกครั้ง')
    else:
        messages.add_message(request, messages.ERROR, 'แก้ไขรหัสผ่านไม่สำเร็จ')
    return redirect('home')
def permissionerror(request):
    return  render(request, 'permissionerror.html')

@login_required(login_url='userAuthen')
def userChgPassword(request):
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
                    user.password = newPassword
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

#Factulty Data
def facultyDetail(request):
    if Personnel.objects.all().count() == 0:
        return redirect('home')
    faculty = Faculty.objects.first()
    context = {'faculty': faculty}
    return render(request, 'base/faculty/facultyDetail.html', context)

@login_required(login_url='userAuthen')
def facultyUpdate(request):
    getSession(request)
    if common.chkPermission(facultyUpdate.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR, msgErrorPermission)
        return redirect('home')
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
    divisions = Division.objects.all().order_by('name_th')
    context = {'divisions': divisions}
    return render(request, 'base/division/divisionList.html', context)

@login_required(login_url='userAuthen')
def divisionNew(request):
    uType=request.session['userType']
    if common.chkPermission(divisionNew.__name__,uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
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
    getSession(request)
    if common.chkPermission(divisionUpdate.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
    division = get_object_or_404(Division, id=id)
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
    getSession(request)
    if common.chkPermission(divisionDelete.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
    division = get_object_or_404(Division, id=id)
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
    curriculums = Curriculum.objects.all().order_by('name_th')
    context = {'curriculums': curriculums}
    return render(request, 'base/curriculum/curriculumList.html', context)

@login_required(login_url='userAuthen')
def curriculumNew(request):
    getSession(request)
    if common.chkPermission(curriculumNew.__name__, uType=uType) ==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
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
        curriculumnYear = datetime.datetime.year + 543
        form = CurriculumForm(initial={'curriculumYear':curriculumnYear})
        context = {'form': form}
        return render(request, 'base/curriculum/curriculumNew.html', context)

@login_required(login_url='userAuthen')
def curriculumUpdate(request, id):
    getSession(request)
    if common.chkPermission(curriculumUpdate.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
    curriculum = get_object_or_404(Curriculum, id=id)
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
    getSession(request)
    if common.chkPermission(curriculumDelete.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
    curriculum = get_object_or_404(Curriculum, id=id)
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
def personnelList(request, pageNo=None):
    if Personnel.objects.all().count() == 0:
        return redirect('home')
    if pageNo == None:
        pageNo = 1
    division = Division.objects.all().order_by('name_th')
    listDivName = []
    listDivCountPersonnel=[]
    if division.count() != 0:
        for div in division:
            listDivName.append(div.name_th)
            listDivCountPersonnel.append(div.getCountPersonnel())
            dataFrame = pd.DataFrame({'สาขา':listDivName, 'จำนวน':listDivCountPersonnel}, columns=['สาขา','จำนวน'])

        fig = px.bar(dataFrame, x='สาขา', y='จำนวน', title='จำนวนบุคลากรแยกตามสาขา')
        fig.update_layout(autosize=False, width=600, height=400,
                          margin=dict(l=10, r=10, b=10, t=50, pad=5, ),
                          paper_bgcolor = "aliceblue")
        chart = fig.to_html()
    else:
        chart=None
    personnels = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th')
    personnels_page = Paginator(personnels, iterm_per_page)
    count = Personnel.objects.all().count()
    cm = Personnel.objects.filter(gender='ชาย').count()
    cfm = Personnel.objects.filter(gender='หญิง').count()
    context = {'personnels': personnels_page.page(pageNo), 'chart':chart, 'count':count, 'countmale':cm, 'countfemale':cfm}
    return render(request, 'base/personnel/personnelList.html', context)

# @login_required(login_url='userAuthen')
def personnelNew(request):
    getSession(request)
    if common.chkPermission(personnelNew.__name__, uType=uType)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
    divisionCount = Division.objects.all().count()
    personnelCount = Personnel.objects.all().count()
    if personnelCount > 0:
        if 'userId' not in request.session:
            return redirect('home')
        else:
            recorder = Personnel.objects.filter(id=request.session['userId']).first()
    else:
        recorder = None
    if divisionCount == 0:
        division = Division(name_th="สำนักงานคณะ", name_en="Office", name_sh="")
        division.save()
    if request.method == 'POST':
        form = PersonnelForm(data=request.POST or None, files=request.FILES)
        passwd = request.POST['passwd']
        confpasswd = request.POST['confpasswd']
        userType  = request.POST['userType']
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
            personnel = get_object_or_404(Personnel, email=email)
            newfilename = 'images/personnels/' + str(personnel.id) + ext
            personnel.picture.name = newfilename
            personnel.save()
            if personnelCount == 0: # กรณีบันทึกเป็นรายแรก  (Admin)
                personnel.recorderId = personnel.id
                personnel.editorId = personnel.id
                personnel.save()
            if os.path.exists('static/' + personnel.picture.name):
                os.remove('static/' + personnel.picture.name)  # file exits, delete it
            os.rename('static/' + filename, 'static/' + personnel.picture.name)
            # สร้าง user ในระบบ authen ของ Django ---
            id = personnel.email
            email = personnel.email
            password = passwd
            user = User.objects.create_user(id, email, password)
            user.first_name = personnel.firstname_en
            user.last_name = personnel.lastname_en
            if userType == 'Administrator':
                user.is_superuser = True
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = True
            group, created = Group.objects.get_or_create(name=userType)
            if group is not None:
                user.groups.add(group)
            else:
                user.groups.add (created)
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
        form = PersonnelForm()
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
    getSession(request, dtype='Personnel', did=personnel.id)
    if common.chkPermission(personnelDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
    context = {'personnel': personnel}
    return render(request, 'base/personnel/personnelDetail.html', context)

@login_required(login_url='userAuthen')
def personnelUpdate(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    getSession(request,dtype='Personnel', did=personnel.id)
    if common.chkPermission(personnelUpdate.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    oldpicture = personnel.picture.name  # รูปเดิม
    oldemail = personnel.email  # อีเมล์เดิม
    if request.method == 'POST':
        form = PersonnelForm(data=request.POST, instance=personnel, files=request.FILES)
        userType = request.POST['userType']
        if form.is_valid():
            updateForm = form.save(commit=False)
            id = updateForm.id
            if updateForm.picture.name != oldpicture:  # หากเลือกรูปใหม่
                filepath = updateForm.picture.name
                filepath = filepath.replace(' ', '_')
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = 'images/personnels/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหลด
                updateForm.save()
                personnel = get_object_or_404(Personnel, id=id)
                newfilename = 'images/personnels/' + str(personnel.id) + ext  # ชื่อไฟล์ที่ระบบกำหนด
                personnel.picture.name = newfilename  # ต้องอัพเดท เผื่อกรณีที่เปลี่ยนชนิดไฟล์ภาพ
                personnel.save()
                if os.path.exists('static/' + oldpicture):  # delete older picture profile
                    os.remove('static/' + oldpicture)
                os.rename('static/' + filename, 'static/' + personnel.picture.name)
            else:
                updateForm.save()
                personnel.editorId = recorder.id
                personnel.editDate = datetime.datetime.now()
                personnel.save()
                messages.add_message(request, messages.SUCCESS, 'แก้ไขข้อมูลบุคลากรเรียบร้อย')
            # อัพเดท user
            user = User.objects.filter(username=oldemail).first()
            user.username = personnel.email
            user.email = personnel.email
            user.first_name = personnel.firstname_en
            user.last_name = personnel.lastname_en
            group, created = Group.objects.get_or_create(name=userType)
            user.groups.clear()
            user.groups.add(group)
            user.save()
            return redirect('personnelDetail', personnel.id)
        else:
            user = User.objects.filter(username=oldemail).first()
            userType = user.groups.first()
            context = {'form': form, 'personnel': personnel, 'userType':userType}
            return render(request, 'base/personnel/personnelUpdate.html', context)
    else:
        user = User.objects.filter(username=oldemail).first()
        userType = user.groups.first()
        userType = str(userType)
        form = PersonnelForm(instance=personnel)
        form.updateForm()
        context = {'form': form, 'personnel': personnel, 'userType':userType}
        return render(request, 'base/personnel/personnelUpdate.html', context)

@login_required(login_url='userAuthen')
def personnelDelete(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    getSession(request, dtype='Personnel', did=personnel.id)
    if common.chkPermission(personnelDelete.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect('home')
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
            return redirect('personnelList', pageNo=1)
        else:
            user = User.objects.filter(username=personnel.email).first()
            user.delete()
            pid = personnel.id
            useRecorder = Personnel.objects.filter(recorderId=pid)
            for use in useRecorder:
                use.recorderId = use.id
                use.save()
            useEditor = Personnel.objects.filter(editorId=pid)
            for use in useEditor:
                use.editorId = use.id
                use.save()
            personnel.delete()
            # delete picture file
            if os.path.exists('static/' + picturefile):
                os.remove('static/' + picturefile)  # file exits, delete it
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
    if 'userType' not in request.session:
        return redirect('userAuthen')
    if request.session['userType'] == "Personnel":
            personnel = Personnel.objects.filter(id=request.session['userId'] ).first()
            context = {'personnel': personnel}
    else:
        division = None
        personnel = None
        divisions = Division.objects.all().order_by('name_th')
        if request.method == 'POST':
            divisionId = request.POST['divisionId']
            personnelId = request.POST['personnelId']
        if divisionId is not None:
            division = Division.objects.filter(id=divisionId).first()
            if personnelId != "":
                personnel = Personnel.objects.filter(id=personnelId).first()
            else:
                personnel = division.getPersonnels().first()
        else:
            division = Division.objects.all().order_by('name_th').first()
            personnel = division.getPersonnels().first()

        context = {'divisions': divisions, 'division': division, 'personnel': personnel}
    return render(request, 'base/education/educationList.html', context)

@login_required(login_url='userAuthen')
def educationNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
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
    context = {'education': education}
    return render(request, 'base/education/educationDetail.html', context)

@login_required(login_url='userAuthen')
def educationUpdate(request, id):
    education = get_object_or_404(Education, id=id)
    personnel = education.personnel
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    form = EducationForm(data=request.POST or None, instance=education)
    if request.method == 'POST':
        if form.is_valid():
            # divisions = Division.objects.all().order_by('name_th')
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
    education = get_object_or_404(Education, id=id)
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
    if 'userType' not in request.session:
        return redirect('userAuthen')
    if request.session['userType'] == "Personnel":
        personnel = Personnel.objects.filter(id=request.session['userId'] ).first()
        context = {'personnel': personnel}
    else:
        division = None
        personnel = None
        divisions = Division.objects.all().order_by('name_th')
        if request.method == 'POST':
            divisionId = request.POST['divisionId']
            personnelId = request.POST['personnelId']
        if divisionId is not None:
            division = Division.objects.filter(id=divisionId).first()
            if personnelId != "":
                personnel = Personnel.objects.filter(id=personnelId).first()
            else:
                personnel = division.getPersonnels().first()
        else:
            division = Division.objects.all().order_by('name_th').first()
            personnel =  division.getPersonnels().first()
        context = {'divisions': divisions, 'division': division, 'personnel': personnel}
    return render(request, 'base/expertise/expertiseList.html', context)

@login_required(login_url='userAuthen')
def expertiseNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
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
    expertise = Expertise.objects.filter(id=id).first()
    context = {'expertise': expertise}
    return render(request, 'base/expertise/expertiseDetail.html', context)

@login_required(login_url='userAuthen')
def expertiseUpdate(request, id):
    expertise = get_object_or_404(Expertise, id=id)
    personnel = expertise.personnel
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
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
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/expertise/expertiseUpdate.html', context)
    else:
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/expertise/expertiseUpdate.html', context)

@login_required(login_url='userAuthen')
def expertiseDelete(request, id):
    expertise = get_object_or_404(Expertise, id=id)
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
    form = CurrAffiliationForm(type='สายวิชาการ', initial={'curriculum': curriculum, 'recorder': recorder})
    context = {'curriculums': curriculums, 'curriculum': curriculum, 'form': form}
    return render(request, 'base/currAffiliation/currAffiliationList.html', context)

@login_required(login_url='userAuthen')
def currAffiliationDelete(request,id):
    currAffiliation = get_object_or_404(CurrAffiliation, id=id)
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
        if 'action' in request.POST:
            form = ResponsibleForm(data=request.POST)
            if form.is_valid():
                newForm = form.save(commit=False)
                person = Personnel.objects.filter(id=newForm.personnel.id).first()
                division = Division.objects.filter(id=newForm.division.id).first()
                responsibles = division.getResponsible() #รายชื่อผู้รับผิดชอบทั้งหมดของสาขานั้นในระบบ
                duplicate = False
                for responer in responsibles:
                    if responer.personnel == person:
                        messages.add_message(request, messages.ERROR,
                                             'บุคลากรที่เลือกเป็นผู้มีรายชื่อรับผิดชอบข้อมูลสาขา/หน่วยงานย่อยนี้อยู่แล้ว')
                        duplicate = True
                        break
                if duplicate == False:
                    newForm.save()
                    messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลผู้รับผิดชอบข้อมูลสาขา/หน่วยงานย่อยเรียบร้อย')
            else:
                messages.add_message(request, messages.WARNING, 'ข้อมูลไม่สมบูรณ์')

    responsibles = Responsible.objects.all().order_by('division__name_th', 'personnel__firstname_th','personnel__lastname_th')
    responsibles_page = Paginator(responsibles, iterm_per_page)
    count = responsibles_page.count
    names = responsibles_page.page(pageNo)
    for name in names:
        print(name)
    form = ResponsibleForm(initial={'recorder': recorder})
    context = {'responsibles':responsibles_page.page(pageNo), 'count':count, 'form': form}
    return render(request, 'base/responsible/responsibleList.html', context)

@login_required(login_url='userAuthen')
def responsibleDelete(request,id):
    responsible = get_object_or_404(Responsible, id=id)
    responsible.delete()
    messages.add_message(request, messages.SUCCESS, 'ลบข้อมูลผู้รับผิดชอบข้อมูลสาขา/หน่วยงานย่อยที่เลือกเรียบร้อย')
    return redirect('responsibleList')
