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

iterm_per_page = 5
#Leave CRUD
@login_required(login_url='userAuthen')
def leaveList(request, divisionId=None, personnelId=None, pageNo=None):
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        personnel = Personnel.objects.filter(id=request.session['userId']).first()
        leaves = Leave.objects.filter(personnel=personnel).order_by('-startDate')
        leaves_page = Paginator(leaves, iterm_per_page)
        count = leaves.count()
        context = {'personnel': personnel,'leaves': leaves_page.page(pageNo), 'count': count}
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
            division = Division.objects.all().order_by('name_th').first() #ถ้ายังไม่เคยเลือกสาขา ให้ระบบเลือกสาขาแรก
            personnel = division.getPersonnels().first() #ถ้ายังไม่เคยเลือกบุคลากร ให้ระบบเลือกบุคลากรคนแรกในสาขา

        leaves = Leave.objects.filter(personnel=personnel).order_by('-startDate')
        count = leaves.count()
        leaves_page = Paginator(leaves, iterm_per_page)
        context = {'divisions': divisions, 'division': division, 'personnel': personnel,
                   'leaves': leaves_page.page(pageNo), 'count':count}
    return render(request, 'work/leave/leaveList.html', context)

@login_required(login_url='userAuthen')
def leaveDetail(request, id):
    leave = Leave.objects.filter(id=id).first()
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
                messages.add_message(request, messages.SUCCESS, "บันทึกตำแหน่งลิงก์ของเอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'leave': leave}
                return render(request, 'work/leave/leaveDetail.html', context)
    # else:
    timeUpdate = leave.getTimeUpdate()
    fileForm = LeaveFileForm(initial={'leave':leave, 'filetype':'Unknow', 'recorder':recorder})
    urlForm = LeaveURLForm(initial={'leave':leave, 'recorder':recorder})
    context={'fileForm': fileForm, 'urlForm':urlForm, 'leave': leave, 'timeUpdate':timeUpdate}
    return render(request, 'work/leave/leaveDetail.html', context)

@login_required(login_url='userAuthen')
def leaveNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
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
    leave = get_object_or_404(Leave, id=id)
    personnel = leave.personnel
    form = LeaveForm(data=request.POST or None, instance=leave)
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
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
    leave = get_object_or_404(Leave, id=id)
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
    leaveFile = get_object_or_404(LeaveFile, id=id)
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
    leave = get_object_or_404(Leave, id=id)
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
    leaveURL = get_object_or_404(LeaveURL, id=id)
    leave = leaveURL.leave
    leaveURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
    return redirect('leaveDetail', id=leave.id)

@login_required(login_url='userAuthen')
def leaveDeleteURLAll(request, id):
    leave = get_object_or_404(Leave, id=id)
    leaveURLs = leave.getLeaveURLs()
    for leaveURL in leaveURLs:
        leaveURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('leaveDetail', id=leave.id)

#Training CRUD
@login_required(login_url='userAuthen')
def trainingList(request, divisionId=None, personnelId=None, pageNo=None):
    if 'userType' not in request.session:
        return redirect('userAuthen')
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        personnel = Personnel.objects.filter(id=request.session['userId']).first()
        trainings = Training.objects.filter(personnel=personnel).order_by('-startDate')
        leaves_page = Paginator(trainings, iterm_per_page)
        count = trainings.count()
        context = {'personnel': personnel, 'trainings': leaves_page.page(pageNo), 'count': count}
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

        trainings = Training.objects.filter(personnel=personnel).order_by('-fiscalYear', '-startDate')
        count = trainings.count()
        trainings_page = Paginator(trainings, iterm_per_page)
        context = {'divisions': divisions, 'division': division, 'personnel': personnel,
                   'trainings':trainings_page.page(pageNo),  'count':count}
    return render(request, 'work/training/trainingList.html', context)

@login_required(login_url='userAuthen')
def trainingDetail(request, id):
    training = Training.objects.filter(id=id).first()
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
                messages.add_message(request, messages.SUCCESS, "บันทึกตำแหน่งลิงก์ของเอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'training': training}
                return render(request, 'work/training/trainingDetail.html', context)
    # else:
    timeUpdate = training.getTimeUpdate()
    fileForm = TrainingFileForm(initial={'training':training, 'filetype':'Unknow', 'recorder':recorder})
    urlForm = TrainingURLForm(initial={'training':training, 'recorder':recorder})
    context={'fileForm': fileForm, 'urlForm':urlForm, 'training': training, 'timeUpdate':timeUpdate}
    return render(request, 'work/training/trainingDetail.html', context)

@login_required(login_url='userAuthen')
def trainingNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
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
    training = get_object_or_404(Training, id=id)
    personnel = training.personnel
    form = TrainignForm(data=request.POST or None, instance=training)
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
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
    training = get_object_or_404(Training, id=id)
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
    trainingFile = get_object_or_404(TrainingFile, id=id)
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
    training = get_object_or_404(Training, id=id)
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
    trainingURL = get_object_or_404(TrainingURL, id=id)
    training = trainingURL.training
    trainingURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารที่เลือกเรียบร้อย")
    return redirect('trainingDetail', id=training.id)

@login_required(login_url='userAuthen')
def trainingDeleteURLAll(request, id):
    training = get_object_or_404(Training, id=id)
    trainingURLs = training.getTrainingURLs()
    for trainingURL in trainingURLs:
        trainingURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('trainingDetail', id=training.id)

# Performance CRUD
@login_required(login_url='userAuthen')
def performanceList(request, divisionId=None, personnelId=None, pageNo=None):
    if 'userType' not in request.session:
        return redirect('userAuthen')
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        personnel = Personnel.objects.filter(id=request.session['userId']).first()
        performances = Performance.objects.filter(personnel=personnel).order_by('-getDate')
        leaves_page = Paginator(performances, iterm_per_page)
        count = performances.count()
        context = {'personnel': personnel, 'performances': leaves_page.page(pageNo), 'count': count}
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

        performances = Performance.objects.filter(personnel=personnel).order_by('-fiscalYear', '-getDate')
        count = performances.count()
        performances_page = Paginator(performances, iterm_per_page)
        context = {'divisions': divisions, 'division': division, 'personnel': personnel,
                   'performances': performances_page.page(pageNo), 'count':count}
    return render(request, 'work/performance/performanceList.html', context)

@login_required(login_url='userAuthen')
def performanceDetail(request, id):
    performance = Performance.objects.filter(id=id).first()
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
                messages.add_message(request, messages.SUCCESS, "บันทึกตำแหน่งลิงก์ของเอกสารเรียบร้อย")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'performance': performance}
                return render(request, 'work/performance/performanceDetail.html', context)
    # else:
    timeUpdate = performance.getTimeUpdate()
    fileForm = PerformanceFileForm(initial={'performance': performance, 'filetype': 'Unknow','recorder':recorder})
    urlForm = PerformanceURLForm(initial={'performance': performance, 'recorder':recorder})
    context = {'fileForm': fileForm, 'urlForm': urlForm, 'performance': performance, 'timeUpdate':timeUpdate}
    return render(request, 'work/performance/performanceDetail.html', context)

@login_required(login_url='userAuthen')
def performanceNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
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
    performance = get_object_or_404(Performance, id=id)
    personnel = performance.personnel
    form = PerformanceForm(data=request.POST or None, instance=performance)
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
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
    performance = get_object_or_404(Performance, id=id)
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
    performanceFile = get_object_or_404(PerformanceFile, id=id)
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
    performance = get_object_or_404(Performance, id=id)
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
    performanceURL = get_object_or_404(PerformanceURL, id=id)
    performance = performanceURL.performance
    performanceURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารเรียบร้อย")
    return redirect('performanceDetail', id=performance.id)

@login_required(login_url='userAuthen')
def performanceDeleteURLAll(request, id):
    performance = get_object_or_404(Performance, id=id)
    performanceURLs = performance.getPerformanceURLs()
    for performanceURL in performanceURLs:
        performanceURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('performanceDetail', id=performance.id)

# CRUD. command
@login_required(login_url='userAuthen')
def commandList(request, pageNo=None):
    if 'userType' not in request.session:
        return redirect('userAuthen')
    if pageNo == None:
        pageNo = 1
    if request.session['userType'] == "Personnel":
        personnel = Personnel.objects.filter(id=request.session['userId']).first()
        # commands = CommandPerson.objects.filter(personnel = personnel)
        commands = Command.objects.filter(commandperson__personnel=personnel).order_by('-eduYear', '-eduSemeter', '-comDate')
        commands_page = Paginator(commands, iterm_per_page)
        count = len(commands)
        context = {'personnel': personnel,'commands': commands_page.page(pageNo), 'count': count}
    else:
        commands = Command.objects.all().order_by('-eduYear', '-eduSemeter', '-comDate')
        commands_page = Paginator(commands, iterm_per_page)
        count = commands.count()
        context = {'commands': commands_page.page(pageNo), 'count': count}
    return render(request, 'work/command/commandList.html', context)

@login_required(login_url='userAuthen')
def commandNew(request):
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
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
def commandDetail(request, id):
    if 'userType' not in request.session:
        return redirect('userAuthen')
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    if (request.session['userType'] == "Personnel"):
        personnel = Personnel.objects.filter(id=request.session['userId']).first()
    command = Command.objects.filter(id=id).first()
    if request.session['userType'] == 'Administrator':
        right = 'Write'
    elif request.session['userType'] == 'Manager':
        if command.recorder == recorder:
            right = 'Write'
        else:
            right = 'Read'
    elif request.session['userType'] == 'Personnel':
        if command.recorder == recorder:
            right = 'Write'
        else:
            right = 'Deny'
    elif request.session['userType'] == 'Staff':
        right = 'Write'
    # ดึงรายชื่อสาขาที่ได้รับมอบหมายให้ดูแลข้อมูลให้ มา

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
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")                
        elif request.POST['action']=='uploadLink':  # upload link
            if urlForm.is_valid():
                urlForm.save()
                messages.add_message(request, messages.SUCCESS, "บันทึกตำแหน่งลิงก์ของเอกสารเรียบร้อย")
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
            if error == True:
                messages.add_message(request, messages.WARNING, msg + " ["+ status + "]")
    fileForm = CommandFileForm(initial={'command': command, 'filetype': 'Unknow', 'recorder':recorder})
    urlForm = CommandURLForm(initial={'command': command, 'recorder':recorder})
    commandPersonForm = CommandPersonForm(command=command, initial={'command':command, 'recorder':recorder, })
    context = {'fileForm': fileForm, 'urlForm': urlForm, 'commandPersonForm':commandPersonForm ,
               'command': command,'personnel':recorder, 'right':right}
    return render(request, 'work/command/commandDetail.html', context)

@login_required(login_url='userAuthen')
def commandUpdate(request, id):
    command = get_object_or_404(Command, id=id)
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
    command = get_object_or_404(Command, id=id)
    form = TrainignForm(data=request.POST or None, instance=command)
    if request.method == 'POST':
        #ลบไฟล์
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
        messages.add_message(request, messages.SUCCESS, "ลบข้อมูลการฝึกอบรม/สัมมนาที่เลือกเรียบร้อย")
        return redirect('commandList', divisionId=command.personnel.division.id, personnelId=command.personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'command':command, 'personnel': command.personnel}
        return render(request, 'work/command/commandDelete.html', context)

@login_required(login_url='userAuthen')
def commandDeleteFile(request, id):
    commandFile = get_object_or_404(CommandFile, id=id)
    command = commandFile.command
    fname = commandFile.file.name
    if os.path.exists('static/documents/command/' + fname):
        try:
            os.remove('static/documents/command/' + fname)  # file exits, delete it
            messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารที่เลือกเรียบร้อย")
        except:
            messages.add_message(request, messages.ERROR, "ไม่สามารถลบไฟล์เอกสารได้")
    commandFile.delete()
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteFileAll(request, id):
    command = get_object_or_404(Command, id=id)
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
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteURL(request, id):
    commandURL = get_object_or_404(CommandURL, id=id)
    command = commandURL.command
    commandURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารที่เลือกเรียบร้อย")
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteURLAll(request, id):
    command = get_object_or_404(Command, id=id)
    commandURLs = command.getCommandURLs()
    for commandURL in commandURLs:
        commandURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดเรียบร้อย")
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteCommandPerson(request, id):
    commandPerson = get_object_or_404(CommandPerson, id=id)
    command = commandPerson.command
    commandPerson.delete()
    messages.add_message(request, messages.SUCCESS, "ลบบุคลากรที่เลือกออกจากคำสั่งเรียบร้อย")
    return redirect('commandDetail', id=command.id)

@login_required(login_url='userAuthen')
def commandDeleteCommandPersonAll(request, id):
    command = get_object_or_404(Command, id=id)
    commandPersons = command.getCommandPerson()
    recorder = Personnel.objects.filter(id=request.session['userId']).first()
    for commandPerson in commandPersons:
        if commandPerson.personnel != recorder:
            commandPerson.delete()
    messages.add_message(request, messages.SUCCESS, "ลบรายชื่อบุคลากรทั้งหมดออกจากคำสั่งเรียบร้อย")
    return redirect('commandDetail', id=command.id)

