import datetime

from django.db.models import Max
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from workapp.models import *
from workapp.forms import *
from baseapp.models import *
from baseapp.forms import *
from django.contrib import messages
from django.core.paginator import (Paginator, EmptyPage,PageNotAnInteger,)
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from workapp import common

iterm_per_page = 10
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

#Leave CRUD
@login_required(login_url='userAuthen')
def leaveList(request, divisionId=None, personnelId=None, pageNo=None):
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        leaves = Leave.objects.filter(personnel=recorder).order_by('-startDate')
        leaves_page = Paginator(leaves, iterm_per_page)
        count = leaves.count()
        context = {'personnel': recorder,'leaves': leaves_page.page(pageNo), 'count': count}
    else:
        division = None
        personnel = None
        outside = False
        if request.session['userType'] == 'Staff':
            outside = recorder.getOutsideResponsible()
            divisions = recorder.getDivisionResponsible()
            if outside == True:  # กรณีที่ผู้รับชอบข้อมูลไม่ได้อยู่ในสาขา/หน่วยงานย่อยที่รับผิดชอบ
                divisions.append(recorder.division)
            division = divisions[0]
        elif request.session['userType'] == 'Header':
            divisions = [recorder.division]
            division = divisions[0]
        else: #Manager, Administrator
            divisions = Division.objects.all().order_by('name_th')
            division = divisions.first()

        recorderOnly = False
        if request.method == 'POST':
            if 'personnelId' in request.POST:
                personnelId = request.POST['personnelId']
                personnel = Personnel.objects.filter(id=personnelId).first()
                division = personnel.division
                if divisionId == recorder.division.id and outside == True:  # ต้องแสดงชื่อเฉพาะ Staff
                    recorderOnly = True
            else:
                divisionId = request.POST['divisionId']
                division = Division.objects.filter(id=divisionId).first()
                if str(divisionId) == str(recorder.division.id) and outside == True:  # ต้องแสดงชื่อเฉพาะ Staff
                    recorderOnly = True
                    personnel = recorder
                else:
                    personnel = division.getPersonnels().first()
        else: #เข้ามาครั้งแรก
            if divisionId is not None: # กรณี redirect มาจากการ New
                division = Division.objects.filter(id=divisionId).first()
                personnel = Personnel.objects.filter(id=personnelId).first()
            else:
                personnel = division.getPersonnels().first()

        leaves = Leave.objects.filter(personnel=personnel).order_by('-startDate')
        count = leaves.count()
        leaves_page = Paginator(leaves, iterm_per_page)
        context = {'divisions': divisions, 'division': division, 'personnel': personnel,
                   'leaves': leaves_page.page(pageNo), 'count':count,'recorderOnly':recorderOnly, 'recorder':recorder}
    return render(request, 'work/leave/leaveList.html', context)

@login_required(login_url='userAuthen')
def leaveDetail(request, id):
    leave = Leave.objects.filter(id=id).first()
    if leave is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Leave', did=leave.id)
    if common.chkPermission(leaveDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        fileForm = LeaveFileForm(request.POST, request.FILES)
        urlForm = LeaveURLForm(request.POST)
        if request.POST['action'] == 'uploadfile':
            if fileForm.is_valid():
                files = request.FILES.getlist("file")
                newFileForm = fileForm.save(commit=False)
                success = True
                fileerror=""
                for f in files:
                    filepath = common.fileNameCleansing(f.name)
                    point = filepath.rfind('.')
                    ext = filepath[point:]
                    filenames = filepath.split('/')
                    filename = 'documents/leave/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหล
                    lf, created = LeaveFile.objects.get_or_create(file=f, leave=leave, recorder=recorder, filetype=ext[1:])
                    lf.save()
                    leaveFile = LeaveFile.objects.last()
                    newfilename = '['+ str(leave.id) + '_' + str(leaveFile.id)+ ']-' + filenames[len(filenames) - 1]   # ชื่อไฟล์ที่ระบบกำหนด
                    leaveFile.file.name = newfilename
                    leaveFile.save()
                    try:
                        os.rename('static/' + filename, 'static/documents/leave/' + leaveFile.file.name)
                    except:
                        fileerror = fileerror + leaveFile.file.name + ", "
                        leaveFile.delete()
                        success=False
                if success==True:
                    messages.add_message(request, messages.SUCCESS, "อัพโหลดไฟล์เอกสารเรียบร้อย")
                else:
                    messages.add_message(request, messages.WARNING, "ไม่สามารถอัพโหลดไฟล์เอกสารบางไฟล์ได้ [" + fileerror+"]")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'leave': leave}
                return render(request, 'work/leave/leaveDetail.html', context)
        else: # upload link
            if urlForm.is_valid():
                urlForm.save()
                messages.add_message(request, messages.SUCCESS, "บันทึกลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'leave': leave}
                return render(request, 'work/leave/leaveDetail.html', context)
    # else:
    timeUpdate =  common.chkUpdateTime(leave.recordDate)
    fileForm = LeaveFileForm(initial={'leave':leave, 'filetype':'Unknow', 'recorder':recorder})
    urlForm = LeaveURLForm(initial={'leave':leave, 'recorder':recorder})
    context={'fileForm': fileForm, 'urlForm':urlForm, 'leave': leave, 'timeUpdate':timeUpdate}
    return render(request, 'work/leave/leaveDetail.html', context)

@login_required(login_url='userAuthen')
def leaveNew(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    if personnel is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Leave', did=personnel.id)
    if common.chkPermission(leaveNew.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        form = LeaveForm(data=request.POST)
        if form.is_valid():
            form.save()
            leave = Leave.objects.last()
            messages.add_message(request, messages.SUCCESS, "บันทึกข้อมูลการลาเรียบร้อย")
            return redirect('leaveDetail', id=leave.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': personnel}
            return render(request, 'work/leave/leaveNew.html', context)
    else:
        fiscalYear = common.getCurrentFiscalYear()
        eduYear = common.getCurrentEduYear()
        currentDate = common.getCurrentDate()
        form = LeaveForm(initial={'personnel': personnel, 'recorder': recorder,'editor':recorder, 'fiscalYear':fiscalYear, 'eduYear':eduYear,
                                  'startDate':currentDate, 'endDate':currentDate,'days':1})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/leave/leaveNew.html', context)

@login_required(login_url='userAuthen')
def leaveUpdate(request, id):
    leave = Leave.objects.filter(id=id).first()
    if leave is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Leave', did=leave.id)
    if common.chkPermission(leaveUpdate.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    personnel = leave.personnel
    form = LeaveForm(data=request.POST or None, instance=leave)
    if request.method == 'POST':
        if form.is_valid():
            updateForm = form.save(commit=False)
            updateForm.recorder = recorder
            updateForm.save()
            leave.editor = recorder
            leave.editDate = datetime.datetime.now()
            leave.save()
            messages.add_message(request, messages.SUCCESS, "แก้ไขข้อมูลการลาเรียบร้อย")
            return redirect('leaveDetail', id=leave.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': personnel}
            return render(request, 'work/leave/leaveUpdate.html', context)
    else:
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/leave/leaveUpdate.html', context)

@login_required(login_url='userAuthen')
def leaveDelete(request, id):
    leave = Leave.objects.filter(id=id).first()
    if leave is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Leave', did=leave.id)
    if common.chkPermission(leaveDelete.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    form = LeaveForm(data=request.POST or None, instance=leave)
    if request.method == 'POST':
        #ลบไฟล์
        fileList = LeaveFile.objects.filter(leave=leave)
        for f in fileList:
            fname = f.file.name
            if os.path.exists('static/documents/leave/' + fname):
                try:
                    os.remove('static/documents/leave/' +fname)  # file exits, delete it
                except:
                    messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
                finally:
                    f.delete()
        urlList = LeaveURL.objects.filter(leave=leave)
        for u in urlList:
            u.delete()
        leave.delete()
        messages.add_message(request, messages.SUCCESS, "ลบข้อมูลการลาที่เลือกเรียบร้อย")
        return redirect('leaveList', divisionId=leave.personnel.division.id, personnelId=leave.personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'leave':leave, 'personnel': leave.personnel}
        return render(request, 'work/leave/leaveDelete.html', context)

@login_required(login_url='userAuthen')
def leaveDeleteFile(request, id):
    leaveFile = LeaveFile.objects.filter(id=id).first()
    leave = leaveFile.leave
    fname = leaveFile.file.name
    if os.path.exists('static/documents/leave/' + fname):
        try:
            os.remove('static/documents/leave/' + fname)  # file exits, delete it
            messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารเรียบร้อย")
        except:
            messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
    leaveFile.delete()
    return redirect('leaveDetail', id=leave.id)

@login_required(login_url='userAuthen')
def leaveDeleteFileAll(request, id):
    leave = Leave.objects.filter(id=id).first()
    leaveFiles = leave.getLeaveFiles()
    success = True
    fileerror = ""
    for leaveFile in leaveFiles:
        fname = leaveFile.file.name
        if os.path.exists('static/documents/leave/' + fname):
            try:
                os.remove('static/documents/leave/' + fname)  # file exits, delete it
            except:
                success=False
                fileerror = fileerror +  fname + ", "
            finally:
                leaveFile.delete()
    if success==True:
        messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารทั้งหมดเรียบร้อย")
    else:
        messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารบางไฟล์ได้ [" + fileerror+"]")
    return redirect('leaveDetail', id=leave.id)

@login_required(login_url='userAuthen')
def leaveDeleteURL(request, id):
    leaveURL = LeaveURL.objects.filter(id=id).first()
    leave = leaveURL.leave
    leaveURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
    return redirect('leaveDetail', id=leave.id)

@login_required(login_url='userAuthen')
def leaveDeleteURLAll(request, id):
    leave = Leave.objects.filter(id=id).first()
    leaveURLs = leave.getLeaveURLs()
    for leaveURL in leaveURLs:
        leaveURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('leaveDetail', id=leave.id)

#Training CRUD
@login_required(login_url='userAuthen')
def trainingList(request, divisionId=None, personnelId=None, pageNo=None):
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        trainings = Training.objects.filter(personnel=recorder).order_by('-startDate')
        training_page = Paginator(trainings, iterm_per_page)
        count = trainings.count()
        context = {'personnel': recorder, 'trainings': training_page.page(pageNo), 'count': count}
    else:
        division = None
        personnel = None
        outside = False
        if request.session['userType'] == 'Staff':
            outside = recorder.getOutsideResponsible()
            divisions = recorder.getDivisionResponsible()
            if outside == True:  # กรณีที่ผู้รับชอบข้อมูลไม่ได้อยู่ในสาขา/หน่วยงานย่อยที่รับผิดชอบ
                divisions.append(recorder.division)
            division = divisions[0]
        elif request.session['userType'] == 'Header':
            divisions = [recorder.division]
            division = divisions[0]
        else: #Manager, Administrator
            divisions = Division.objects.all().order_by('name_th')
            division = divisions.first()

        recorderOnly = False
        if request.method == 'POST':
            if 'personnelId' in request.POST:
                personnelId = request.POST['personnelId']
                personnel = Personnel.objects.filter(id=personnelId).first()
                division = personnel.division
                if divisionId == recorder.division.id and outside == True: #ต้องแสดงชื่อเฉพาะ Staff
                    recorderOnly = True
            else:
                divisionId = request.POST['divisionId']
                division = Division.objects.filter(id=divisionId).first()
                if str(divisionId) == str(recorder.division.id) and outside == True: #ต้องแสดงชื่อเฉพาะ Staff
                    recorderOnly = True
                    personnel = recorder
                else:
                    personnel = division.getPersonnels().first()
        else: #เข้ามาครั้งแรก
            if divisionId is not None: # กรณี redirect มาจากการ New
                division = Division.objects.filter(id=divisionId).first()
                personnel = Personnel.objects.filter(id=personnelId).first()
            else:
                personnel = division.getPersonnels().first()

        trainings = Training.objects.filter(personnel=personnel).order_by('-fiscalYear', '-startDate')
        count = trainings.count()
        trainings_page = Paginator(trainings, iterm_per_page)
        context = {'divisions': divisions, 'division': division, 'personnel': personnel,
                   'trainings':trainings_page.page(pageNo),  'count':count, 'recorderOnly':recorderOnly, 'recorder':recorder}
    return render(request, 'work/training/trainingList.html', context)

@login_required(login_url='userAuthen')
def trainingDetail(request, id):
    training = Training.objects.filter(id=id).first()
    if training is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Training', did=training.id)
    if common.chkPermission(trainingDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        fileForm = TrainingFileForm(request.POST, request.FILES)
        urlForm = TrainingURLForm(request.POST)
        if request.POST['action'] == 'uploadfile':
            if fileForm.is_valid():
                files = request.FILES.getlist("file")
                newFileForm = fileForm.save(commit=False)
                success = True
                fileerror=""
                for f in files:
                    filepath = common.fileNameCleansing(f.name)
                    point = filepath.rfind('.')
                    ext = filepath[point:]
                    filenames = filepath.split('/')
                    filename = 'documents/training/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหล
                    lf, created = TrainingFile.objects.get_or_create(file=f, training=training, recorder=recorder, filetype=ext[1:])
                    lf.save()
                    trainingFile = TrainingFile.objects.last()
                    newfilename = '['+ str(training.id) + '_' + str(trainingFile.id)+ ']-' + filenames[len(filenames) - 1]   # ชื่อไฟล์ที่ระบบกำหนด
                    trainingFile.file.name = newfilename
                    trainingFile.save()
                    try:
                        os.rename('static/' + filename, 'static/documents/training/' + trainingFile.file.name)
                    except:
                        fileerror = fileerror + trainingFile.file.name + ", "
                        trainingFile.delete()
                        success=False
                if success==True:
                    messages.add_message(request, messages.SUCCESS, "อัพโหลดไฟล์เอกสารเรียบร้อย")
                else:
                    messages.add_message(request, messages.WARNING, "ไม่สามารถอัพโหลดไฟล์เอกสารบางไฟล์ได้ [" + fileerror+"]")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'training': training}
                return render(request, 'work/training/trainingDetail.html', context)
        else: # upload link
            if urlForm.is_valid():
                urlForm.save()
                messages.add_message(request, messages.SUCCESS, "บันทึกลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'training': training}
                return render(request, 'work/training/trainingDetail.html', context)
    # else:
    timeUpdate = common.chkUpdateTime(training.recordDate)
    fileForm = TrainingFileForm(initial={'training':training, 'filetype':'Unknow', 'recorder':recorder})
    urlForm = TrainingURLForm(initial={'training':training, 'recorder':recorder})
    context={'fileForm': fileForm, 'urlForm':urlForm, 'training': training, 'timeUpdate':timeUpdate}
    return render(request, 'work/training/trainingDetail.html', context)

@login_required(login_url='userAuthen')
def trainingNew(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    if personnel is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Training', did=personnel.id)
    if common.chkPermission(trainingNew.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        form = TrainignForm(data=request.POST)
        if form.is_valid():
            form.save()
            training = Training.objects.last()
            messages.add_message(request, messages.SUCCESS, "บันทึกข้อมูลการฝึกอบรม/สัมมนาเรียบร้อย")
            return redirect('trainingDetail', id=training.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': personnel}
            return render(request, 'work/training/trainingNew.html', context)
    else:
        fiscalYear = common.getCurrentFiscalYear()
        eduYear = common.getCurrentEduYear()
        eduSemeter = common.getCurrentEduSemeter()
        currentDate = common.getCurrentDate()
        form = TrainignForm(initial={'personnel': personnel, 'recorder': recorder, 'editor':recorder, 'fiscalYear':fiscalYear,
                                     'eduYear':eduYear, 'eduSemeter':eduSemeter, 'startDate':currentDate, 'endDate':currentDate,
                                     'days':1})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/training/trainingNew.html', context)

@login_required(login_url='userAuthen')
def trainingUpdate(request, id):
    training = Training.objects.filter(id=id).first()
    if training is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Training', did=training.id)
    if common.chkPermission(trainingUpdate.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    personnel = training.personnel
    form = TrainignForm(data=request.POST or None, instance=training)
    if request.method == 'POST':
        if form.is_valid():
            updateForm = form.save(commit=False)
            updateForm.recorder = recorder
            updateForm.save()
            training.editor = recorder
            training.editDate = datetime.datetime.now()
            training.save()
            messages.add_message(request, messages.SUCCESS, "แก้ไขข้อมูลฝึกอบรม/สัมมนาเรียบร้อย")
            return redirect('trainingDetail', id=training.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': personnel}
            return render(request, 'work/training/trainingUpdate.html', context)
    else:
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/training/trainingUpdate.html', context)

@login_required(login_url='userAuthen')
def trainingDelete(request, id):
    training = Training.objects.filter(id=id).first()
    if training is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Training', did=training.id)
    if common.chkPermission(trainingDelete.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    form = TrainignForm(data=request.POST or None, instance=training)
    if request.method == 'POST':
        #ลบไฟล์
        fileList = TrainingFile.objects.filter(training=training)
        for f in fileList:
            fname = f.file.name
            if os.path.exists('static/documents/training/' + fname):
                try:
                    os.remove('static/documents/training/' +fname)  # file exits, delete it
                except:
                    messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
                finally:
                    f.delete()
        urlList =TrainingURL.objects.filter(training=training)
        for u in urlList:
            u.delete()
        training.delete()
        messages.add_message(request, messages.SUCCESS, "ลบข้อมูลการฝึกอบรม/สัมมนาที่เลือกเรียบร้อย")
        return redirect('trainingList', divisionId=training.personnel.division.id, personnelId=training.personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'training':training, 'personnel': training.personnel}
        return render(request, 'work/training/trainingDelete.html', context)

@login_required(login_url='userAuthen')
def trainingDeleteFile(request, id):
    trainingFile = TrainingFile.objects.filter(id=id).first()
    training = trainingFile.training
    fname = trainingFile.file.name
    if os.path.exists('static/documents/training/' + fname):
        try:
            os.remove('static/documents/training/' + fname)  # file exits, delete it
            messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารเรียบร้อย")
        except:
            messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
    trainingFile.delete()
    return redirect('trainingDetail', id=training.id)

@login_required(login_url='userAuthen')
def trainingDeleteFileAll(request, id):
    training = Training.objects.filter(id=id).first()
    trainingFiles = training.getTrainingFiles()
    success = True
    fileerror = ""
    for trainingFile in trainingFiles:
        fname = trainingFile.file.name
        if os.path.exists('static/documents/training/' + fname):
            try:
                os.remove('static/documents/training/' + fname)  # file exits, delete it
            except:
                success=False
                fileerror = fileerror +  fname + ", "
            finally:
                trainingFile.delete()
    if success==True:
        messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารทั้งหมดเรียบร้อย")
    else:
        messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารบางไฟล์ได้ [" + fileerror+"]")
    return redirect('trainingDetail', id=training.id)

@login_required(login_url='userAuthen')
def trainingDeleteURL(request, id):
    trainingURL = TrainingURL.objects.filter(id=id).first()
    training = trainingURL.training
    trainingURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารที่เลือกเรียบร้อย")
    return redirect('trainingDetail', id=training.id)

@login_required(login_url='userAuthen')
def trainingDeleteURLAll(request, id):
    training = Training.objects.filter(id=id).first()
    trainingURLs = training.getTrainingURLs()
    for trainingURL in trainingURLs:
        trainingURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('trainingDetail', id=training.id)

# Performance CRUD
@login_required(login_url='userAuthen')
def performanceList(request, divisionId=None, personnelId=None, pageNo=None):
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        performances = Performance.objects.filter(personnel=recorder).order_by('-getDate')
        performance_page = Paginator(performances, iterm_per_page)
        count = performances.count()
        context = {'personnel': recorder, 'performances': performance_page.page(pageNo), 'count': count}
    else:
        division = None
        personnel = None
        outside = False
        if request.session['userType'] == 'Staff':
            outside = recorder.getOutsideResponsible()
            divisions = recorder.getDivisionResponsible()
            if outside == True:  # กรณีที่ผู้รับชอบข้อมูลไม่ได้อยู่ในสาขา/หน่วยงานย่อยที่รับผิดชอบ
                divisions.append(recorder.division)
            division = divisions[0]
        elif request.session['userType'] == 'Header':
            divisions = [recorder.division]
            division = divisions[0]
        else: #Manager, Administrator
            divisions = Division.objects.all().order_by('name_th')
            division = divisions.first()

        recorderOnly = False
        if request.method == 'POST':
            if 'personnelId' in request.POST:
                personnelId = request.POST['personnelId']
                personnel = Personnel.objects.filter(id=personnelId).first()
                division = personnel.division
                if divisionId == recorder.division.id and outside == True:  # ต้องแสดงชื่อเฉพาะ Staff
                    recorderOnly = True
            else:
                divisionId = request.POST['divisionId']
                division = Division.objects.filter(id=divisionId).first()
                if str(divisionId) == str(recorder.division.id) and outside == True: #ต้องแสดงชื่อเฉพาะ Staff
                    recorderOnly = True
                    personnel = recorder
                else:
                    personnel = division.getPersonnels().first()
        else: #เข้ามาครั้งแรก
            if divisionId is not None: # กรณี redirect มาจากการ New
                division = Division.objects.filter(id=divisionId).first()
                personnel = Personnel.objects.filter(id=personnelId).first()
            else:
                personnel = division.getPersonnels().first()

        performances = Performance.objects.filter(personnel=personnel).order_by('-fiscalYear', '-getDate')
        count = performances.count()
        performances_page = Paginator(performances, iterm_per_page)
        context = {'divisions': divisions, 'division': division, 'personnel': personnel,
                   'performances': performances_page.page(pageNo), 'count':count, 'recorderOnly': recorderOnly, 'recorder':recorder}
    return render(request, 'work/performance/performanceList.html', context)

@login_required(login_url='userAuthen')
def performanceDetail(request, id):
    performance = Performance.objects.filter(id=id).first()
    if performance is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Performance', did=performance.id)
    if common.chkPermission(performanceDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        fileForm = PerformanceFileForm(request.POST, request.FILES)
        urlForm = PerformanceURLForm(request.POST)
        if request.POST['action'] == 'uploadfile':
            if fileForm.is_valid():
                files = request.FILES.getlist("file")
                newFileForm = fileForm.save(commit=False)
                success = True
                fileerror = ""
                for f in files:
                    filepath = common.fileNameCleansing(f.name)
                    point = filepath.rfind('.')
                    ext = filepath[point:]
                    filenames = filepath.split('/')
                    filename = 'documents/performance/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหล
                    lf, created = PerformanceFile.objects.get_or_create(file=f, performance=performance, recorder=recorder, filetype=ext[1:])
                    lf.save()
                    performanceFile = PerformanceFile.objects.last()
                    newfilename = '[' + str(performance.id) + '_' + str(performanceFile.id) + ']-' + filenames[
                        len(filenames) - 1]  # ชื่อไฟล์ที่ระบบกำหนด
                    performanceFile.file.name = newfilename
                    performanceFile.save()
                    try:
                        os.rename('static/' + filename, 'static/documents/performance/' + performanceFile.file.name)
                    except:
                        fileerror = fileerror + performanceFile.file.name + ", "
                        performanceFile.delete()
                        success = False
                if success == True:
                    messages.add_message(request, messages.SUCCESS, "อัพโหลดไฟล์เอกสารเรียบร้อย")
                else:
                    messages.add_message(request, messages.WARNING,
                                         "ไม่สามารถอัพโหลดไฟล์เอกสารบางไฟล์ได้ [" + fileerror + "]")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'performance': performance}
                return render(request, 'work/performance/performanceDetail.html', context)
        else:  # upload link
            if urlForm.is_valid():
                urlForm.save()
                messages.add_message(request, messages.SUCCESS, "บันทึกลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'performance': performance}
                return render(request, 'work/performance/performanceDetail.html', context)
    # else:
    timeUpdate =  common.chkUpdateTime(performance.recordDate)
    fileForm = PerformanceFileForm(initial={'performance': performance, 'filetype': 'Unknow','recorder':recorder})
    urlForm = PerformanceURLForm(initial={'performance': performance, 'recorder':recorder})
    context = {'fileForm': fileForm, 'urlForm': urlForm, 'performance': performance, 'timeUpdate':timeUpdate}
    return render(request, 'work/performance/performanceDetail.html', context)

@login_required(login_url='userAuthen')
def performanceNew(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    if personnel is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Performance', did=personnel.id)
    if common.chkPermission(performanceNew.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        form = PerformanceForm(data=request.POST)
        if form.is_valid():
            form.save()
            performance = Performance.objects.last()
            messages.add_message(request, messages.SUCCESS, "บันทึกข้อมูลผลงาน/รางวัลเรียบร้อย")
            return redirect('performanceDetail', id=performance.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': personnel}
            return render(request, 'work/performance/performanceNew.html', context)
    else:
        fiscalYear = common.getCurrentFiscalYear()
        eduYear = common.getCurrentEduYear()
        eduSemeter = common.getCurrentEduSemeter()
        currentDate = common.getCurrentDate()
        form = PerformanceForm(
            initial={'personnel': personnel, 'recorder': recorder, 'editor':recorder,'fiscalYear': fiscalYear, 'eduYear': eduYear, 'eduSemeter':eduSemeter,
                     'getDate':currentDate})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/performance/performanceNew.html', context)

@login_required(login_url='userAuthen')
def performanceUpdate(request, id):
    performance = Performance.objects.filter(id=id).first()
    if performance is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Performance', did=performance.id)
    if common.chkPermission(performanceUpdate.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    personnel = performance.personnel
    form = PerformanceForm(data=request.POST or None, instance=performance)

    if request.method == 'POST':
        if form.is_valid():
            updateForm = form.save(commit=False)
            updateForm.recorder = recorder
            updateForm.save()
            performance.editor = recorder
            performance.editDate = datetime.datetime.now()
            performance.save()
            messages.add_message(request, messages.SUCCESS, "แก้ไขข้อมูลฝึกอบรม/สัมมนาเรียบร้อย")
            return redirect('performanceDetail', id=performance.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel':personnel}
            return render(request, 'work/performance/performanceUpdate.html', context)
    else:
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/performance/performanceUpdate.html', context)

@login_required(login_url='userAuthen')
def performanceDelete(request, id):
    performance = Performance.objects.filter(id=id).first()
    if performance is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Performance', did=performance.id)
    if common.chkPermission(performanceDelete.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    form = PerformanceForm(data=request.POST or None, instance=performance)

    if request.method == 'POST':
        # ลบไฟล์
        fileList = PerformanceFile.objects.filter(performance=performance)
        for f in fileList:
            fname = f.file.name
            if os.path.exists('static/documents/performance/' + fname):
                try:
                    os.remove('static/documents/performance/' + fname)  # file exits, delete it
                except:
                    messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
                finally:
                    f.delete()
        urlList = PerformanceURL.objects.filter(performance=performance)
        for u in urlList:
            u.delete()
        performance.delete()
        messages.add_message(request, messages.SUCCESS, "ลบข้อมูลการฝึกอบรม/สัมมนาที่เลือกเรียบร้อย")
        return redirect('performanceList', divisionId=performance.personnel.division.id, personnelId=performance.personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'performance': performance, 'personnel': performance.personnel}
        return render(request, 'work/performance/performanceDelete.html', context)

@login_required(login_url='userAuthen')
def performanceDeleteFile(request, id):
    performanceFile = PerformanceFile.objects.filter(id=id).first()
    performance = performanceFile.performance
    fname = performanceFile.file.name
    if os.path.exists('static/documents/performance/' + fname):
        try:
            os.remove('static/documents/performance/' + fname)  # file exits, delete it
            messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารที่เลือกเรียบร้อย")
        except:
            messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารที่เลือกได้")
    performanceFile.delete()
    return redirect('performanceDetail', id=performance.id)

@login_required(login_url='userAuthen')
def performanceDeleteFileAll(request, id):
    performance = Performance.objects.filter(id=id).first()
    performanceFiles = performance.getPerformanceFiles()
    success = True
    fileerror = ""
    for performanceFile in performanceFiles:
        fname = performanceFile.file.name
        if os.path.exists('static/documents/performance/' + fname):
            try:
                os.remove('static/documents/performance/' + fname)  # file exits, delete it
            except:
                success = False
                fileerror = fileerror + fname + ", "
            finally:
                performanceFile.delete()
    if success == True:
        messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารทั้งหมดเรียบร้อย")
    else:
        messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารบางไฟล์ได้ [" + fileerror + "]")
    return redirect('performanceDetail', id=performance.id)

@login_required(login_url='userAuthen')
def performanceDeleteURL(request, id):
    performanceURL = PerformanceURL.objects.filter(id=id).first()
    performance = performanceURL.performance
    performanceURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
    return redirect('performanceDetail', id=performance.id)

@login_required(login_url='userAuthen')
def performanceDeleteURLAll(request, id):
    performance = Performance.objects.filter(id=id).first()
    performanceURLs = performance.getPerformanceURLs()
    for performanceURL in performanceURLs:
        performanceURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('performanceDetail', id=performance.id)

# CRUD. Command
@login_required(login_url='userAuthen')
def commandList(request, pageNo=None):
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    personnel = [recorder]
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        commands1 = Command.objects.filter(commandperson__personnel=recorder).order_by('-eduYear', '-eduSemeter', '-comDate') #คำสั่งที่ได้รับมอบหมาย
        commands2 = Command.objects.filter(recorder_id__in=personnel) #คำสั่งที่เป็นคนบันทึกไว้เอง
        commands = commands1.union(commands2)
        commands_page = Paginator(commands, iterm_per_page)
        count = commands.count()
        context = {'personnel': recorder,'commands': commands_page.page(pageNo), 'count': count}
    elif request.session['userType'] == "Header":
        division = recorder.getHeader().division #หน่วยงานที่เป็นหัวหน้า
        personnels = division.getPersonnels()
        commands1 = Command.objects.filter(commandperson__personnel__in=personnels).distinct().order_by('-eduYear', '-eduSemeter', '-comDate') #คำสั่งที่ได้รับมอบหมาย
        commands2 = Command.objects.filter(recorder_id=recorder) #คำสั่งที่เป็นคนบันทึกไว้เอง
        commands =  commands1.union(commands2).order_by('-eduYear', '-eduSemeter', '-comDate')
        commands_page = Paginator(commands, iterm_per_page)
        count = commands.count()
        context = {'personnel': recorder, 'commands': commands_page.page(pageNo), 'count': count}
    else: # request.session['userType'] in ['Administrator', 'Staff', 'Manager'] :
        commands = Command.objects.all().order_by('-eduYear', '-eduSemeter', '-comDate')
        commands_page = Paginator(commands, iterm_per_page)
        count = commands.count()
        context = {'commands': commands_page.page(pageNo), 'count': count}
    return render(request, 'work/command/commandList.html', context)

@login_required(login_url='userAuthen')
def commandDetail(request, id):
    command = Command.objects.filter(id=id).first()
    if command is None:
        messages.add_message(request, messages.ERROR,msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Command', did=command.id)
    if common.chkPermission(commandDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        fileForm = CommandFileForm(request.POST, request.FILES)
        urlForm = CommandURLForm(request.POST)
        if request.POST['action'] == 'uploadfile':
            if fileForm.is_valid():
                files = request.FILES.getlist("file")
                success = True
                fileerror = ""
                for f in files:
                    filepath = common.fileNameCleansing(f.name)
                    point = filepath.rfind('.')
                    ext = filepath[point:]
                    filenames = filepath.split('/')
                    filename = 'documents/command/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหล
                    lf, created = CommandFile.objects.get_or_create(file=f, command=command, recorder=recorder, filetype=ext[1:])
                    lf.save()
                    commandFile = CommandFile.objects.last()
                    newfilename = '[' + str(command.id) + '_' + str(commandFile.id) + ']-' + filenames[
                        len(filenames) - 1]  # ชื่อไฟล์ที่ระบบกำหนด
                    commandFile.file.name = newfilename
                    commandFile.recorder = recorder
                    commandFile.save()
                    try:
                        os.rename('static/' + filename, 'static/documents/command/' + commandFile.file.name)
                    except:
                        fileerror = fileerror + commandFile.file.name + ", "
                        commandFile.delete()
                        success = False
                if success == True:
                    messages.add_message(request, messages.SUCCESS, "อัพโหลดไฟล์เอกสารเรียบร้อย")
                else:
                    messages.add_message(request, messages.WARNING,
                                         "ไม่สามารถอัพโหลดไฟล์เอกสารบางไฟล์ได้ [" + fileerror + "]")
                command.editor = recorder
                command.editDate = datetime.datetime.now()
                command.save()
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
        elif request.POST['action']=='uploadLink':  # upload link
            if urlForm.is_valid():
                urlForm.save()
                command.editor = recorder
                command.editDate = datetime.datetime.now()
                command.save()
                messages.add_message(request, messages.SUCCESS, "บันทึกลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
        else: # save uploadPersonnel
            # id = request.POST['command']
            # command = Command.objects.filter(id=id).first()
            status = request.POST['status']
            status = status.strip()
            personnelIdList = request.POST.getlist('personnel')
            msg = "บุคลากรที่มีหน้าที่เดียวกันปรากฏซ้ำในระบบสำหรับคำสั่งนี้อยู่แล้ว :"
            error = False
            for pid in personnelIdList:
                person = Personnel.objects.filter(id=pid).first()
                find = CommandPerson.objects.filter(command=command, personnel=person).first()
                if find is None:
                    commandPerson = CommandPerson(command=command, personnel=person, status=status,
                                                  recorder=recorder)
                    commandPerson.save()
                else:
                    error = True
                    msg = msg + str(person)
            command.editor = recorder
            command.editDate = datetime.datetime.now()
            command.save()
            if error == True:
                messages.add_message(request, messages.WARNING, msg + " ["+ status + "]")
    fileForm = CommandFileForm(initial={'command': command, 'filetype': 'Unknow', 'recorder':recorder})
    urlForm = CommandURLForm(initial={'command': command, 'recorder':recorder})
    if request.session['userType'] == 'Header':
        commandPersonForm = CommandPersonForm(command=command, division=recorder.division, initial={'command':command, 'recorder':recorder, })
    elif request.session['userType'] == 'Staff':
        commandPersonForm = CommandPersonForm(command=command, division=recorder.division, staff=recorder,
                                              initial={'command': command, 'recorder': recorder, })
    else:
        commandPersonForm = CommandPersonForm(command=command, initial={'command':command, 'recorder':recorder, })

    context = {'fileForm': fileForm, 'urlForm': urlForm, 'commandPersonForm':commandPersonForm ,
               'command': command,'personnel':recorder}
    return render(request, 'work/command/commandDetail.html', context)

@login_required(login_url='userAuthen')
def commandNew(request):
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    getSession(request, dtype='Command', did=recorder.id)
    if common.chkPermission(commandNew.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    if request.method == 'POST':
        form = CommandForm(data=request.POST)
        if form.is_valid():
            form.save()
            command = Command.objects.last()
            if(request.session["userType"]=="Personnel"):
                status = request.POST['status']
                commandPerson = CommandPerson(command=command, personnel=recorder, recorder=recorder, status=status)
                commandPerson.status = status
                commandPerson.save()
            messages.add_message(request, messages.SUCCESS, "บันทึกข้อมูลคำสั่งเรียบร้อย")
            return redirect('commandDetail', id=command.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form}
            return render(request, 'work/command/commandNew.html', context)
    else:
        fiscalYear = common.getCurrentFiscalYear()
        eduYear = common.getCurrentEduYear()
        eduSemeter = common.getCurrentEduSemeter()
        currentDate = common.getCurrentDate()
        form = CommandForm(
            initial={'fiscalYear': fiscalYear, 'eduYear': eduYear, 'eduSemeter':eduSemeter,
                     'comDate':currentDate, 'recorder': recorder, 'editor':recorder })
        context = {'form': form, 'personnel':recorder}
        return render(request, 'work/command/commandNew.html', context)

@login_required(login_url='userAuthen')
def commandUpdate(request, id):
    command = Command.objects.filter(id=id).first()
    if command is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Command', did=command.id)
    if common.chkPermission(commandUpdate.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    form = CommandForm(data=request.POST or None, instance=command)
    if request.method == 'POST':
        if form.is_valid():
            updateForm = form.save(commit=False)
            updateForm.recorder = recorder
            updateForm.save()
            command.editor = recorder
            command.editDate = datetime.datetime.now()
            command.save()
            messages.add_message(request, messages.SUCCESS, "แก้ไขข้อมูลคำสั่งเรียบร้อย")
            return redirect('commandDetail', id=command.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': recorder, 'command':command}
            return render(request, 'work/command/commandUpdate.html', context)
    else:
        context = {'form': form, 'personnel': recorder,'command':command}
        return render(request, 'work/command/commandUpdate.html', context)

@login_required(login_url='userAuthen')
def commandDelete(request, id):
    command = Command.objects.filter(id=id).first()
    if command is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Command', did=command.id)
    if common.chkPermission(commandDelete.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    form = CommandForm(data=request.POST or None, instance=command)
    if request.method == 'POST':
        commandPersonnels = command.getCommandPerson()
        complete = False
        if len(commandPersonnels) == 0:
            complete = True
        elif len(commandPersonnels) == 1:
            commandPerson = commandPersonnels.first()
            if commandPerson.recorder == recorder:
                complete = True
            else:
                messages.add_message(request, messages.ERROR,
                             "คำสั่งที่เลือกมีรายชื่อบุคลากรที่ได้รับมอบหมายในการปฏิบัติหน้าที่ตามคำสั่งนี้อยู่ ไม่สามารถลบได้")
        else:
            messages.add_message(request, messages.ERROR,
                                 "คำสั่งที่เลือกมีรายชื่อบุคลากรที่ได้รับมอบหมายในการปฏิบัติหน้าที่ตามคำสั่งนี้อยู่ ไม่สามารถลบได้")
        if complete == False:
            return redirect(request.session['last_url'])
        else:
            #ลบคน กรณีเป็นเจ้าของคำสั่ง
            for commandPerson in commandPersonnels:
                commandPerson.delete()
            # ลบไฟล์
            fileList = CommandFile.objects.filter(command=command)
            for f in fileList:
                fname = f.file.name
                if os.path.exists('static/documents/command/' + fname):
                    try:
                        os.remove('static/documents/command/' +fname)  # file exits, delete it
                    except:
                        messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
                    finally:
                        f.delete()
            urlList =CommandURL.objects.filter(command=command)
            for u in urlList:
                u.delete()
            command.delete()
            messages.add_message(request, messages.SUCCESS, "ลบข้อมูลคำสั่งเรียบร้อย")
            return redirect('commandList')
    else:
        form.deleteForm()
        context = {'form': form, 'command':command, 'personnel': command.recorder}
        return render(request, 'work/command/commandDelete.html', context)

@login_required(login_url='userAuthen')
def commandDeleteFile(request, id):
    commandFile = CommandFile.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    command = commandFile.command
    fname = commandFile.file.name
    if os.path.exists('static/documents/command/' + fname):
        try:
            os.remove('static/documents/command/' + fname)  # file exits, delete it
            messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารที่เลือกเรียบร้อย")
        except:
            messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
    commandFile.delete()
    command.editor = recorder
    command.editDate = datetime.datetime.now()
    command.save()
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteFileAll(request, id):
    command = Command.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    commandFiles = command.getCommandFiles()
    success = True
    fileerror = ""
    for commandFile in commandFiles:
        fname = commandFile.file.name
        if os.path.exists('static/documents/command/' + fname):
            try:
                os.remove('static/documents/command/' + fname)  # file exits, delete it
            except:
                success = False
                fileerror = fileerror + fname + ", "
            finally:
                commandFile.delete()
    if success == True:
        messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารทั้งหมดเรียบร้อย")
    else:
        messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารบางไฟล์ได้ [" + fileerror + "]")
    command.editor = recorder
    command.editDate = datetime.datetime.now()
    command.save()
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteURL(request, id):
    commandURL = CommandURL.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    command = commandURL.command
    commandURL.delete()
    command.editor = recorder
    command.editDate = datetime.datetime.now()
    command.save()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารที่เลือกเรียบร้อย")
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteURLAll(request, id):
    command = Command.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    commandURLs = command.getCommandURLs()
    for commandURL in commandURLs:
        commandURL.delete()
    command.editor = recorder
    command.editDate = datetime.datetime.now()
    command.save()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteCommandPerson(request, id):
    commandPerson = CommandPerson.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    command = commandPerson.command
    commandPerson.delete()
    command.editor = recorder
    command.editDate = datetime.datetime.now()
    command.save()
    messages.add_message(request, messages.SUCCESS, "ลบบุคลากรที่เลือกออกจากคำสั่งเรียบร้อย")
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteCommandPersonAll(request, id):
    command = Command.objects.filter(id=id).first()
    commandPersons = command.getCommandPerson()
    recorder = command.recorder
    personnel = Personnel.objects.filter(id=request.session['userId']).first()
    count = 0
    for commandPerson in commandPersons:
        if request.session['userType'] =='Administrator': # Admin ลบได้ทั้งหมดใน CommandPerson รวมถึงตัวเอง
            commandPerson.delete()
            count+=1
        elif request.session['userType'] =='Staff': # Staff ลบได้ทั้งหมดที่เคยเพิ่มใน CommandPerson รวมถึงตัวเอง
            if commandPerson.recorder == personnel:
                commandPerson.delete()
                count += 1
        else: # กรณีเป็นเจ้าของเอกสาร Personnel
            if commandPerson.recorder == recorder:
                commandPerson.delete()
                count += 1
    if count != 0:
        command.editor = personnel
        command.editDate = datetime.datetime.now()
        command.save()
        messages.add_message(request, messages.SUCCESS, "ลบรายชื่อบุคลากรทั้งหมดที่ผู้ใช้ระบบเคยบันทึกไว้ ออกจากคำสั่งเรียบร้อย ")
    else:
        messages.add_message(request, messages.WARNING, "ไม่มีบุคลากรรายใดที่ผู้ใช้ระบบได้เคยบันทึกไว้ถูกลบออกจากคำสั่งนี้")
    return redirect('commandDetail', id=command.id)


# ***********************************************************
# CRUD. Research
@login_required(login_url='userAuthen')
def researchList(request, pageNo=None):
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    personnel = [recorder]
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        researchs1 = Research.objects.filter(researchperson__personnel=recorder).order_by('-fiscalYear', 'title_th') #งานวิจัยในตารางผู้ทำวิจัย
        researchs2 = Research.objects.filter(recorder_id__in=personnel) #งานวิจัยที่เป็นคนบันทึกไว้เอง
        researchs = researchs1.union(researchs2)
        researchs_page = Paginator(researchs, iterm_per_page)
        count = researchs.count()
        context = {'personnel': recorder,'researchs': researchs_page.page(pageNo), 'count': count}
    elif request.session['userType'] == "Header":
        division = recorder.getHeader().division #หน่วยงานที่เป็นหัวหน้า
        personnels = division.getPersonnels()
        researchs1 = Research.objects.filter(researchperson__personnel__in=personnels).distinct().order_by('-fiscalYear', 'title_th') #งานวิจัยในตารางผู้ทำวิจัย
        researchs2 = Research.objects.filter(recorder_id=recorder) #งานวิจัยที่เป็นคนบันทึกไว้เอง
        researchs =  researchs1.union(researchs2).order_by('-fiscalYear', 'title_th')
        researchs_page = Paginator(researchs, iterm_per_page)
        count = researchs.count()
        context = {'personnel': recorder, 'researchs': researchs_page.page(pageNo), 'count': count}
    else: # request.session['userType'] in ['Administrator', 'Staff', 'Manager'] :
        researchs = Research.objects.all().order_by('-fiscalYear', 'title_th')
        researchs_page = Paginator(researchs, iterm_per_page)
        count = researchs.count()
        context = {'researchs': researchs_page.page(pageNo), 'count': count}
    return render(request, 'work/research/researchList.html', context)

@login_required(login_url='userAuthen')
def researchDetail(request, id):
    research = Research.objects.filter(id=id).first()
    if research is None:
        messages.add_message(request, messages.ERROR,msgErrorId)
        return redirect(request.session['last_url'])
    # getSession(request, dtype='Research', did=research.id)
    # if common.chkPermission(researchDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
    #     messages.add_message(request, messages.ERROR,msgErrorPermission)
    #     return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        fileForm = ResearchFileForm(request.POST, request.FILES)
        urlForm = ResearchURLForm(request.POST)
        if request.POST['action'] == 'uploadfile':
            if fileForm.is_valid():
                files = request.FILES.getlist("file")
                success = True
                fileerror = ""
                for f in files:
                    filepath = common.fileNameCleansing(f.name)
                    point = filepath.rfind('.')
                    ext = filepath[point:]
                    filenames = filepath.split('/')
                    filename = 'documents/research/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหล
                    lf, created = ResearchFile.objects.get_or_create(file=f, research=research, recorder=recorder, filetype=ext[1:])
                    lf.save()
                    researchFile = ResearchFile.objects.last()
                    newfilename = '[' + str(research.id) + '_' + str(researchFile.id) + ']-' + filenames[
                        len(filenames) - 1]  # ชื่อไฟล์ที่ระบบกำหนด
                    researchFile.file.name = newfilename
                    researchFile.recorder = recorder
                    researchFile.save()
                    try:
                        os.rename('static/' + filename, 'static/documents/research/' + researchFile.file.name)
                    except:
                        fileerror = fileerror + researchFile.file.name + ", "
                        researchFile.delete()
                        success = False
                if success == True:
                    messages.add_message(request, messages.SUCCESS, "อัพโหลดไฟล์เอกสารเรียบร้อย")
                else:
                    messages.add_message(request, messages.WARNING,
                                         "ไม่สามารถอัพโหลดไฟล์เอกสารบางไฟล์ได้ [" + fileerror + "]")
                research.editor = recorder
                research.editDate = datetime.datetime.now()
                research.save()
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
        elif request.POST['action']=='uploadLink':  # upload link
            if urlForm.is_valid():
                urlForm.save()
                research.editor = recorder
                research.editDate = datetime.datetime.now()
                research.save()
                messages.add_message(request, messages.SUCCESS, "บันทึกลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
        else: # save uploadPersonnel
            # id = request.POST['research']
            # research = Research.objects.filter(id=id).first()
            status = request.POST['status']
            percent = int(request.POST['percent'])
            status = status.strip()
            personnelIdList = request.POST.getlist('personnel')
            #check percent
            numOfResearch = int(len(personnelIdList))
            if research.getSumPercent() is not None:
                sumPercent = int(research.getSumPercent())
            else:
                sumPercent = 0
            totalPercent = sumPercent +(percent * numOfResearch)
            if totalPercent > 100:
                messages.add_message(request, messages.WARNING, "สัดส่วนการทำงานวิจัยของนักวิจัยรวมแล้วเกิน 100% ไม่สามารถบันทึกได้")
                return redirect(request.session['last_url'])
            if str(status).find('หัวหน้าโครงการ') != -1: # ป้อนตำแหน่งหัวหน้าโครงการ
                if numOfResearch > 1:
                    messages.add_message(request, messages.WARNING, "ตำแหน่ง/ความรับผิดชอบ หัวหน้าโครงการ มีได้เพียงคนเดียวเท่านั้น ไม่สามารถบันทึกได้")
                    return redirect(request.session['last_url'])
                chkStatus = ResearchPerson.objects.filter(status__contains='หัวหน้าโครงการ').first()
                if chkStatus is not None:
                    messages.add_message(request, messages.WARNING, "ตำแหน่ง/ความรับผิดชอบ หัวหน้าโครงการ มีได้เพียงคนเดียวเท่านั้น ไม่สามารถบันทึกได้")
                    return redirect(request.session['last_url'])

            # เช็คคนซ้ำ
            msg = "นักวิจัยที่เลือกมีรายชื่อปรากฎอยู่ในงานวิจัยนี้อยู่แล้ว :"
            error = False
            for pid in personnelIdList:
                person = Personnel.objects.filter(id=pid).first()
                find = ResearchPerson.objects.filter(research=research, personnel=person).first()
                if find is None:
                    researchPerson = ResearchPerson(research=research, personnel=person, status=status,
                                                    percent= percent, recorder=recorder)
                    researchPerson.save()
                else:
                    error = True
                    msg = msg + str(person)
            research.editor = recorder
            research.editDate = datetime.datetime.now()
            research.save()
            if error == True:
                messages.add_message(request, messages.WARNING, msg + " ["+ status + "]")
    fileForm = ResearchFileForm(initial={'research': research, 'filetype': 'Unknow', 'recorder':recorder})
    urlForm = ResearchURLForm(initial={'research': research, 'recorder':recorder})
    if request.session['userType'] == 'Header':
        researchPersonForm = ResearchPersonForm(research=research, division=recorder.division, initial={'research':research, 'recorder':recorder, 'status':'หัวหน้าโครงการวิจัย',  'percent':100 })
    elif request.session['userType'] == 'Staff':
        researchPersonForm = ResearchPersonForm(research=research, division=recorder.division, staff=recorder,
                                              initial={'research': research, 'recorder': recorder, 'status':'หัวหน้าโครงการวิจัย', 'percent':100  })
    else:
        researchPersonForm = ResearchPersonForm(research=research, initial={'research':research, 'recorder':recorder, 'status':'หัวหน้าโครงการวิจัย', 'percent':100 })

    context = {'fileForm': fileForm, 'urlForm': urlForm, 'researchPersonForm':researchPersonForm ,
               'research': research,'personnel':recorder}
    return render(request, 'work/research/researchDetail.html', context)

@login_required(login_url='userAuthen')
def researchNew(request):
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    getSession(request, dtype='Research', did=recorder.id)
    if common.chkPermission(researchNew.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    if request.method == 'POST':
        form = ResearchForm(data=request.POST)
        if form.is_valid():
            form.save()
            research = Research.objects.last()
            # if(request.session["userType"]=="Personnel"):
            #     researchPerson = ResearchPerson(research=research, personnel=recorder, recorder=recorder, percent=research.percent_resp)
            #     researchPerson.save()
            messages.add_message(request, messages.SUCCESS, "บันทึกข้อมูลงานวิจัยเรียบร้อย")
            return redirect('researchDetail', id=research.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form}
            return render(request, 'work/research/researchNew.html', context)
    else:
        university = Faculty.objects.all().first().university
        fiscalYear = common.getCurrentFiscalYear()
        form = ResearchForm(
            initial={'fiscalYear': fiscalYear, 'percent_resp':100,'percent_success':100, 'source':university, 'recorder': recorder, 'editor' :recorder })
        context = {'form': form, 'personnel':recorder}
        return render(request, 'work/research/researchNew.html', context)

@login_required(login_url='userAuthen')
def researchUpdate(request, id):
    research = Research.objects.filter(id=id).first()
    if research is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='Research', did=research.id)
    if common.chkPermission(researchUpdate.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    form = ResearchForm(data=request.POST or None, instance=research)
    if request.method == 'POST':
        if form.is_valid():
            updateForm = form.save(commit=False)
            updateForm.recorder = recorder
            updateForm.save()
            research.editor = recorder
            research.editDate = datetime.datetime.now()
            research.save()
            messages.add_message(request, messages.SUCCESS, "แก้ไขข้อมูลงานวิจัยเรียบร้อย")
            return redirect('researchDetail', id=research.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': recorder, 'research':research}
            return render(request, 'work/research/researchUpdate.html', context)
    else:
        context = {'form': form, 'personnel': recorder,'research':research}
        return render(request, 'work/research/researchUpdate.html', context)

@login_required(login_url='userAuthen')
def researchDelete(request, id):
    research = Research.objects.filter(id=id).first()
    if research is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    # getSession(request, dtype='Research', did=research.id)
    # if common.chkPermission(researchDelete.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
    #     messages.add_message(request, messages.ERROR,msgErrorPermission)
    #     return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    form = ResearchForm(data=request.POST or None, instance=research)
    if request.method == 'POST':
        researchPersonnels = research.getResearchPerson()
        complete = False
        if len(researchPersonnels) == 0:
            complete = True
        elif len(researchPersonnels) == 1:
            researchPerson = researchPersonnels.first()
            if researchPerson.recorder == recorder:
                complete = True
            else:
                messages.add_message(request, messages.ERROR, "งานวิจัยที่เลือกมีรายชื่อนักวิจัยอยู่ ไม่สามารถลบได้")
        else:
            messages.add_message(request, messages.ERROR, "งานวิจัยที่เลือกมีรายชื่อนักวิจัยอยู่ ไม่สามารถลบได้")
        if complete == False:
            return redirect(request.session['last_url'])
        else:
            #ลบคน กรณีเป็นเจ้าของงานวิจัย
            for researchPerson in researchPersonnels:
                researchPerson.delete()
            # ลบไฟล์
            fileList = ResearchFile.objects.filter(research=research)
            for f in fileList:
                fname = f.file.name
                if os.path.exists('static/documents/research/' + fname):
                    try:
                        os.remove('static/documents/research/' +fname)  # file exits, delete it
                    except:
                        messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
                    finally:
                        f.delete()
            urlList =ResearchURL.objects.filter(research=research)
            for u in urlList:
                u.delete()
            research.delete()
            messages.add_message(request, messages.SUCCESS, "ลบข้อมูลงานวิจัยเรียบร้อย")
            return redirect('researchList')
    else:
        form.deleteForm()
        context = {'form': form, 'research':research, 'personnel': research.recorder}
        return render(request, 'work/research/researchDelete.html', context)

@login_required(login_url='userAuthen')
def researchDeleteFile(request, id):
    researchFile = ResearchFile.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    research = researchFile.research
    fname = researchFile.file.name
    if os.path.exists('static/documents/research/' + fname):
        try:
            os.remove('static/documents/research/' + fname)  # file exits, delete it
            messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารที่เลือกเรียบร้อย")
        except:
            messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
    researchFile.delete()
    research.editor = recorder
    research.editDate = datetime.datetime.now()
    research.save()
    return redirect('researchDetail', id=research.id)

@login_required(login_url='userAuthen')
def researchDeleteFileAll(request, id):
    research = Research.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    researchFiles = research.getResearchFiles()
    success = True
    fileerror = ""
    for researchFile in researchFiles:
        fname = researchFile.file.name
        if os.path.exists('static/documents/research/' + fname):
            try:
                os.remove('static/documents/research/' + fname)  # file exits, delete it
            except:
                success = False
                fileerror = fileerror + fname + ", "
            finally:
                researchFile.delete()
    if success == True:
        messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารทั้งหมดเรียบร้อย")
    else:
        messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารบางไฟล์ได้ [" + fileerror + "]")
    research.editor = recorder
    research.editDate = datetime.datetime.now()
    research.save()
    return redirect('researchDetail', id=research.id)

@login_required(login_url='userAuthen')
def researchDeleteURL(request, id):
    researchURL = ResearchURL.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    research = researchURL.research
    researchURL.delete()
    research.editor = recorder
    research.editDate = datetime.datetime.now()
    research.save()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารที่เลือกเรียบร้อย")
    return redirect('researchDetail', id=research.id)

@login_required(login_url='userAuthen')
def researchDeleteURLAll(request, id):
    research = Research.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    researchURLs = research.getResearchURLs()
    for researchURL in researchURLs:
        researchURL.delete()
    research.editor = recorder
    research.editDate = datetime.datetime.now()
    research.save()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('researchDetail', id=research.id)

@login_required(login_url='userAuthen')
def researchDeleteResearchPerson(request, id):
    researchPerson = ResearchPerson.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    research = researchPerson.research
    researchPerson.delete()
    research.editor = recorder
    research.editDate = datetime.datetime.now()
    research.save()
    messages.add_message(request, messages.SUCCESS, "ลบบุคลากรที่เลือกออกจากงานวิจัยเรียบร้อย")
    return redirect('researchDetail', id=research.id)

@login_required(login_url='userAuthen')
def researchDeleteResearchPersonAll(request, id):
    research = Research.objects.filter(id=id).first()
    researchPersons = research.getResearchPerson()
    recorder = research.recorder
    personnel = Personnel.objects.filter(id=request.session['userId']).first()
    count = 0
    for researchPerson in researchPersons:
        if request.session['userType'] =='Administrator': # Admin ลบได้ทั้งหมดใน ResearchPerson รวมถึงตัวเอง
            researchPerson.delete()
            count+=1
        elif request.session['userType'] =='Staff': # Staff ลบได้ทั้งหมดที่เคยเพิ่มใน ResearchPerson รวมถึงตัวเอง
            if researchPerson.recorder == personnel:
                researchPerson.delete()
                count += 1
        else: # กรณีเป็นเจ้าของเอกสาร Personnel
            if researchPerson.recorder == recorder :
                researchPerson.delete()
                count += 1
    if count != 0:
        research.editor = personnel
        research.editDate = datetime.datetime.now()
        research.save()
        messages.add_message(request, messages.SUCCESS, "ลบรายชื่อบุคลากรทั้งหมดที่ผู้ใช้ระบบเคยบันทึกไว้ ออกจากงานวิจัยเรียบร้อย ")
    else:
        messages.add_message(request, messages.WARNING, "ไม่มีบุคลากรรายใดที่ผู้ใช้ระบบได้เคยบันทึกไว้ถูกลบออกจากงานวิจัยนี้")
    return redirect('researchDetail', id=research.id)

# ***********************************************************
# CRUD. SocialService
@login_required(login_url='userAuthen')
def socialserviceList(request, pageNo=None):
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    personnel = [recorder]
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        socialservices1 = SocialService.objects.filter(socialserviceperson__personnel=recorder).order_by('-fiscalYear', 'title_th') #งานวิจัยในตารางผู้ทำวิจัย
        socialservices2 = SocialService.objects.filter(recorder_id__in=personnel) #งานวิจัยที่เป็นคนบันทึกไว้เอง
        socialservices = socialservices1.union(socialservices2)
        socialservices_page = Paginator(socialservices, iterm_per_page)
        count = socialservices.count()
        context = {'personnel': recorder,'socialservices': socialservices_page.page(pageNo), 'count': count}
    elif request.session['userType'] == "Header":
        division = recorder.getHeader().division #หน่วยงานที่เป็นหัวหน้า
        personnels = division.getPersonnels()
        socialservices1 = SocialService.objects.filter(socialserviceperson__personnel__in=personnels).distinct().order_by('-eduYear', '-eduSemeter') #โครงการในตารางผู้ร่วมโครงการ
        socialservices2 = SocialService.objects.filter(recorder_id=recorder) #โครงการที่เป็นคนบันทึกไว้เอง
        socialservices =  socialservices1.union(socialservices2).order_by('-eduYear', '-eduSemeter')
        socialservices_page = Paginator(socialservices, iterm_per_page)
        count = socialservices.count()
        context = {'personnel': recorder, 'socialservices': socialservices_page.page(pageNo), 'count': count}
    else: # request.session['userType'] in ['Administrator', 'Staff', 'Manager'] :
        socialservices = SocialService.objects.all().order_by('-eduYear', '-eduSemeter')
        socialservices_page = Paginator(socialservices, iterm_per_page)
        count = socialservices.count()
        context = {'socialservices': socialservices_page.page(pageNo), 'count': count}
    return render(request, 'work/socialservice/socialserviceList.html', context)

@login_required(login_url='userAuthen')
def socialserviceDetail(request, id):
    socialservice = SocialService.objects.filter(id=id).first()
    if socialservice is None:
        messages.add_message(request, messages.ERROR,msgErrorId)
        return redirect(request.session['last_url'])
    # getSession(request, dtype='SocialService', did=socialservice.id)
    # if common.chkPermission(socialserviceDetail.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
    #     messages.add_message(request, messages.ERROR,msgErrorPermission)
    #     return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    if request.method == 'POST':
        fileForm = SocialServiceFileForm(request.POST, request.FILES)
        urlForm = SocialServiceURLForm(request.POST)
        if request.POST['action'] == 'uploadfile':
            if fileForm.is_valid():
                files = request.FILES.getlist("file")
                success = True
                fileerror = ""
                for f in files:
                    filepath = common.fileNameCleansing(f.name)
                    point = filepath.rfind('.')
                    ext = filepath[point:]
                    filenames = filepath.split('/')
                    filename = 'documents/socialservice/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหล
                    lf, created = SocialServiceFile.objects.get_or_create(file=f, socialservice=socialservice, recorder=recorder, filetype=ext[1:])
                    lf.save()
                    socialserviceFile = SocialServiceFile.objects.last()
                    newfilename = '[' + str(socialservice.id) + '_' + str(socialserviceFile.id) + ']-' + filenames[
                        len(filenames) - 1]  # ชื่อไฟล์ที่ระบบกำหนด
                    socialserviceFile.file.name = newfilename
                    socialserviceFile.recorder = recorder
                    socialserviceFile.save()
                    try:
                        os.rename('static/' + filename, 'static/documents/socialservice/' + socialserviceFile.file.name)
                    except:
                        fileerror = fileerror + socialserviceFile.file.name + ", "
                        socialserviceFile.delete()
                        success = False
                if success == True:
                    messages.add_message(request, messages.SUCCESS, "อัพโหลดไฟล์เอกสารเรียบร้อย")
                else:
                    messages.add_message(request, messages.WARNING,
                                         "ไม่สามารถอัพโหลดไฟล์เอกสารบางไฟล์ได้ [" + fileerror + "]")
                socialservice.editor = recorder
                socialservice.editDate = datetime.datetime.now()
                socialservice.save()
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
        elif request.POST['action']=='uploadLink':  # upload link
            if urlForm.is_valid():
                urlForm.save()
                socialservice.editor = recorder
                socialservice.editDate = datetime.datetime.now()
                socialservice.save()
                messages.add_message(request, messages.SUCCESS, "บันทึกลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
        else: # save uploadPersonnel
            # id = request.POST['socialservice']
            # socialservice = SocialService.objects.filter(id=id).first()
            status = request.POST['status']
            status = status.strip()
            personnelIdList = request.POST.getlist('personnel')
            #check percent
            numOfSocialService = int(len(personnelIdList))

            if str(status).find('หัวหน้าโครงการ') != -1: # ป้อนตำแหน่งหัวหน้าโครงการ
                if numOfSocialService > 1:
                    messages.add_message(request, messages.WARNING, "ตำแหน่ง/ความรับผิดชอบ หัวหน้าโครงการ มีได้เพียงคนเดียวเท่านั้น ไม่สามารถบันทึกได้")
                    return redirect(request.session['last_url'])
                chkStatus = SocialServicePerson.objects.filter(status__contains='หัวหน้าโครงการ').first() #??????????????
                if chkStatus is not None:
                    messages.add_message(request, messages.WARNING, "ตำแหน่ง/ความรับผิดชอบ หัวหน้าโครงการ มีได้เพียงคนเดียวเท่านั้น ไม่สามารถบันทึกได้")
                    return redirect(request.session['last_url'])

            # เช็คคนซ้ำ
            msg = "นักวิจัยที่เลือกมีรายชื่อปรากฎอยู่ในงานวิจัยนี้อยู่แล้ว :"
            error = False
            for pid in personnelIdList:
                person = Personnel.objects.filter(id=pid).first()
                find = SocialServicePerson.objects.filter(socialservice=socialservice, personnel=person).first()
                if find is None:
                    socialservicePerson = SocialServicePerson(socialservice=socialservice, personnel=person, status=status,
                                                    percent= percent, recorder=recorder)
                    socialservicePerson.save()
                else:
                    error = True
                    msg = msg + str(person)
            socialservice.editor = recorder
            socialservice.editDate = datetime.datetime.now()
            socialservice.save()
            if error == True:
                messages.add_message(request, messages.WARNING, msg + " ["+ status + "]")
    fileForm = SocialServiceFileForm(initial={'socialservice': socialservice, 'filetype': 'Unknow', 'recorder':recorder})
    urlForm = SocialServiceURLForm(initial={'socialservice': socialservice, 'recorder':recorder})
    if request.session['userType'] == 'Header':
        socialservicePersonForm = SocialServicePersonForm(socialservice=socialservice, division=recorder.division, initial={'socialservice':socialservice, 'recorder':recorder, 'status':'หัวหน้าโครงการวิจัย',  'percent':100 })
    elif request.session['userType'] == 'Staff':
        socialservicePersonForm = SocialServicePersonForm(socialservice=socialservice, division=recorder.division, staff=recorder,
                                              initial={'socialservice': socialservice, 'recorder': recorder, 'status':'หัวหน้าโครงการวิจัย', 'percent':100  })
    else:
        socialservicePersonForm = SocialServicePersonForm(socialservice=socialservice, initial={'socialservice':socialservice, 'recorder':recorder, 'status':'หัวหน้าโครงการวิจัย', 'percent':100 })

    context = {'fileForm': fileForm, 'urlForm': urlForm, 'socialservicePersonForm':socialservicePersonForm ,
               'socialservice': socialservice,'personnel':recorder}
    return render(request, 'work/socialservice/socialserviceDetail.html', context)

@login_required(login_url='userAuthen')
def socialserviceNew(request):
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    getSession(request, dtype='SocialService', did=recorder.id)
    if common.chkPermission(socialserviceNew.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info

    if request.method == 'POST':
        form = SocialServiceForm(data=request.POST)
        if form.is_valid():
            form.save()
            socialservice = SocialService.objects.last()
            # if(request.session["userType"]=="Personnel"):
            #     socialservicePerson = SocialServicePerson(socialservice=socialservice, personnel=recorder, recorder=recorder, percent=socialservice.percent_resp)
            #     socialservicePerson.save()
            messages.add_message(request, messages.SUCCESS, "บันทึกข้อมูลงานวิจัยเรียบร้อย")
            return redirect('socialserviceDetail', id=socialservice.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form}
            return render(request, 'work/socialservice/socialserviceNew.html', context)
    else:
        university = Faculty.objects.all().first().university
        fiscalYear = common.getCurrentFiscalYear()
        eduYear = common.getCurrentEduYear()
        eduSemeter = common.getCurrentEduSemeter()
        currentDate = common.getCurrentDate()
        form = SocialServiceForm(
            initial={'fiscalYear': fiscalYear,'eduYear':eduYear, 'eduSemeter':eduSemeter, 'startDate':currentDate, 'endDate':currentDate, 'source':university, 'recorder': recorder, 'editor' :recorder })
        context = {'form': form, 'personnel':recorder}
        return render(request, 'work/socialservice/socialserviceNew.html', context)

@login_required(login_url='userAuthen')
def socialserviceUpdate(request, id):
    socialservice = SocialService.objects.filter(id=id).first()
    if socialservice is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    getSession(request, dtype='SocialService', did=socialservice.id)
    if common.chkPermission(socialserviceUpdate.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
        messages.add_message(request, messages.ERROR,msgErrorPermission)
        return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    form = SocialServiceForm(data=request.POST or None, instance=socialservice)
    if request.method == 'POST':
        if form.is_valid():
            updateForm = form.save(commit=False)
            updateForm.recorder = recorder
            updateForm.save()
            socialservice.editor = recorder
            socialservice.editDate = datetime.datetime.now()
            socialservice.save()
            messages.add_message(request, messages.SUCCESS, "แก้ไขข้อมูลงานวิจัยเรียบร้อย")
            return redirect('socialserviceDetail', id=socialservice.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': recorder, 'socialservice':socialservice}
            return render(request, 'work/socialservice/socialserviceUpdate.html', context)
    else:
        context = {'form': form, 'personnel': recorder,'socialservice':socialservice}
        return render(request, 'work/socialservice/socialserviceUpdate.html', context)

@login_required(login_url='userAuthen')
def socialserviceDelete(request, id):
    socialservice = SocialService.objects.filter(id=id).first()
    if socialservice is None:
        messages.add_message(request, messages.ERROR, msgErrorId)
        return redirect(request.session['last_url'])
    # getSession(request, dtype='SocialService', did=socialservice.id)
    # if common.chkPermission(socialserviceDelete.__name__,uType=uType, uId=uId, docType=docType, docId=docId)==False:
    #     messages.add_message(request, messages.ERROR,msgErrorPermission)
    #     return redirect(request.session['last_url'])
    request.session['last_url'] = request.path_info
    recorder = Personnel.objects.filter(id=request.session['userId']).first()

    form = SocialServiceForm(data=request.POST or None, instance=socialservice)
    if request.method == 'POST':
        socialservicePersonnels = socialservice.getSocialServicePerson()
        complete = False
        if len(socialservicePersonnels) == 0:
            complete = True
        elif len(socialservicePersonnels) == 1:
            socialservicePerson = socialservicePersonnels.first()
            if socialservicePerson.recorder == recorder:
                complete = True
            else:
                messages.add_message(request, messages.ERROR, "งานวิจัยที่เลือกมีรายชื่อนักวิจัยอยู่ ไม่สามารถลบได้")
        else:
            messages.add_message(request, messages.ERROR, "งานวิจัยที่เลือกมีรายชื่อนักวิจัยอยู่ ไม่สามารถลบได้")
        if complete == False:
            return redirect(request.session['last_url'])
        else:
            #ลบคน กรณีเป็นเจ้าของงานวิจัย
            for socialservicePerson in socialservicePersonnels:
                socialservicePerson.delete()
            # ลบไฟล์
            fileList = SocialServiceFile.objects.filter(socialservice=socialservice)
            for f in fileList:
                fname = f.file.name
                if os.path.exists('static/documents/socialservice/' + fname):
                    try:
                        os.remove('static/documents/socialservice/' +fname)  # file exits, delete it
                    except:
                        messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
                    finally:
                        f.delete()
            urlList =SocialServiceURL.objects.filter(socialservice=socialservice)
            for u in urlList:
                u.delete()
            socialservice.delete()
            messages.add_message(request, messages.SUCCESS, "ลบข้อมูลงานวิจัยเรียบร้อย")
            return redirect('socialserviceList')
    else:
        form.deleteForm()
        context = {'form': form, 'socialservice':socialservice, 'personnel': socialservice.recorder}
        return render(request, 'work/socialservice/socialserviceDelete.html', context)

@login_required(login_url='userAuthen')
def socialserviceDeleteFile(request, id):
    socialserviceFile = SocialServiceFile.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    socialservice = socialserviceFile.socialservice
    fname = socialserviceFile.file.name
    if os.path.exists('static/documents/socialservice/' + fname):
        try:
            os.remove('static/documents/socialservice/' + fname)  # file exits, delete it
            messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารที่เลือกเรียบร้อย")
        except:
            messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
    socialserviceFile.delete()
    socialservice.editor = recorder
    socialservice.editDate = datetime.datetime.now()
    socialservice.save()
    return redirect('socialserviceDetail', id=socialservice.id)

@login_required(login_url='userAuthen')
def socialserviceDeleteFileAll(request, id):
    socialservice = SocialService.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    socialserviceFiles = socialservice.getSocialServiceFiles()
    success = True
    fileerror = ""
    for socialserviceFile in socialserviceFiles:
        fname = socialserviceFile.file.name
        if os.path.exists('static/documents/socialservice/' + fname):
            try:
                os.remove('static/documents/socialservice/' + fname)  # file exits, delete it
            except:
                success = False
                fileerror = fileerror + fname + ", "
            finally:
                socialserviceFile.delete()
    if success == True:
        messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารทั้งหมดเรียบร้อย")
    else:
        messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารบางไฟล์ได้ [" + fileerror + "]")
    socialservice.editor = recorder
    socialservice.editDate = datetime.datetime.now()
    socialservice.save()
    return redirect('socialserviceDetail', id=socialservice.id)

@login_required(login_url='userAuthen')
def socialserviceDeleteURL(request, id):
    socialserviceURL = SocialServiceURL.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    socialservice = socialserviceURL.socialservice
    socialserviceURL.delete()
    socialservice.editor = recorder
    socialservice.editDate = datetime.datetime.now()
    socialservice.save()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารที่เลือกเรียบร้อย")
    return redirect('socialserviceDetail', id=socialservice.id)

@login_required(login_url='userAuthen')
def socialserviceDeleteURLAll(request, id):
    socialservice = SocialService.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    socialserviceURLs = socialservice.getSocialServiceURLs()
    for socialserviceURL in socialserviceURLs:
        socialserviceURL.delete()
    socialservice.editor = recorder
    socialservice.editDate = datetime.datetime.now()
    socialservice.save()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('socialserviceDetail', id=socialservice.id)

@login_required(login_url='userAuthen')
def socialserviceDeleteSocialServicePerson(request, id):
    socialservicePerson = SocialServicePerson.objects.filter(id=id).first()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    socialservice = socialservicePerson.socialservice
    socialservicePerson.delete()
    socialservice.editor = recorder
    socialservice.editDate = datetime.datetime.now()
    socialservice.save()
    messages.add_message(request, messages.SUCCESS, "ลบบุคลากรที่เลือกออกจากงานวิจัยเรียบร้อย")
    return redirect('socialserviceDetail', id=socialservice.id)

@login_required(login_url='userAuthen')
def socialserviceDeleteSocialServicePersonAll(request, id):
    socialservice = SocialService.objects.filter(id=id).first()
    socialservicePersons = socialservice.getSocialServicePerson()
    recorder = socialservice.recorder
    personnel = Personnel.objects.filter(id=request.session['userId']).first()
    count = 0
    for socialservicePerson in socialservicePersons:
        if request.session['userType'] =='Administrator': # Admin ลบได้ทั้งหมดใน SocialServicePerson รวมถึงตัวเอง
            socialservicePerson.delete()
            count+=1
        elif request.session['userType'] =='Staff': # Staff ลบได้ทั้งหมดที่เคยเพิ่มใน SocialServicePerson รวมถึงตัวเอง
            if socialservicePerson.recorder == personnel:
                socialservicePerson.delete()
                count += 1
        else: # กรณีเป็นเจ้าของเอกสาร Personnel
            if socialservicePerson.recorder == recorder :
                socialservicePerson.delete()
                count += 1
    if count != 0:
        socialservice.editor = personnel
        socialservice.editDate = datetime.datetime.now()
        socialservice.save()
        messages.add_message(request, messages.SUCCESS, "ลบรายชื่อบุคลากรทั้งหมดที่ผู้ใช้ระบบเคยบันทึกไว้ ออกจากงานวิจัยเรียบร้อย ")
    else:
        messages.add_message(request, messages.WARNING, "ไม่มีบุคลากรรายใดที่ผู้ใช้ระบบได้เคยบันทึกไว้ถูกลบออกจากงานวิจัยนี้")
    return redirect('socialserviceDetail', id=socialservice.id)

