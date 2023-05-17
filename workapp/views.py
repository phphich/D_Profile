import datetime

from django.db.models import Max
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from workapp.models import *
from workapp.forms import *
from baseapp.models import *
from baseapp.forms import *
import os
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

#Leave CRUD
def leaveList(request, divisionId=None, personnelId=None):
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
    leaves = Leave.objects.filter(personnel=personnel).order_by('-startDate')
    # leaves = personnel.getLeave()

    context = {'divisions': divisions, 'division': division, 'personnel': personnel, 'leaves':leaves}
    return render(request, 'work/leave/leaveList.html', context)

def leaveNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    if request.method == 'POST':
        form = LeaveForm(data=request.POST)
        if form.is_valid():
            form.save()
            leave = Leave.objects.last()
            messages.add_message(request, messages.SUCCESS, "บันทึกข้อมูลเข้าสู่ระบบเรียบร้อย")
            return redirect('leaveDetail', id=leave.id)
            # return redirect('leaveList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': personnel}
            return render(request, 'work/leave/leaveNew.html', context)
    else:
        today = datetime.date.today()
        currentYear = today.year
        form = LeaveForm(initial={'personnel': personnel, 'recorder': personnel, 'fiscalYear':currentYear, 'eduYear':currentYear})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/leave/leaveNew.html', context)

def fileNameCleansing(filename):
    find = [' ', '+', '%', '#','$','@','!', '^','&','*',',',
            'ั', '่','้','๊','๋','์',
            'ิ','ี','ึ', 'ื','ุ','ู',
            '(',')','[',']','{','}',
            ]
    for f in find:
        if f == ' ':
            filename = filename.replace(f, '_')
        else:
            filename = filename.replace(f, '')
    return filename

def leaveDetail(request, id):
    leave = Leave.objects.filter(id=id).first()
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
                    filepath = fileNameCleansing(f.name)
                    point = filepath.rfind('.')
                    ext = filepath[point:]
                    filenames = filepath.split('/')
                    filename = 'documents/leave/' + filenames[len(filenames) - 1]  # ชื่อไฟล์ที่อัพโหล
                    lf, created = LeaveFile.objects.get_or_create(file=f, leave=leave, filetype=ext[1:])
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
                    messages.add_message(request, messages.SUCCESS, "อัพโหลดไฟล์เอกสารสำเร็จ")
                else:
                    messages.add_message(request, messages.WARNING, "ไม่สามารถอัพโหลดไฟล์เอกสารบางไฟล์ได้ [" + fileerror+"]")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'leave': leave}
                return render(request, 'work/leave/leaveDetail.html', context)
        else: # upload link
            if urlForm.is_valid():
                urlForm.save()
                messages.add_message(request, messages.SUCCESS, "บันทึกตำแหน่งลิงก์ของเอกสารสำเร็จ")
            else:
                messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์ss")
                context = {'fileForm': fileForm, 'urlForm': urlForm, 'leave': leave}
                return render(request, 'work/leave/leaveDetail.html', context)
    # else:
    fileForm = LeaveFileForm(initial={'leave':leave, 'filetype':'Unknow'})
    urlForm = LeaveURLForm(initial={'leave':leave})
    context={'fileForm': fileForm, 'urlForm':urlForm, 'leave': leave}
    return render(request, 'work/leave/leaveDetail.html', context)

def leaveUpdate(request, id):
    leave = get_object_or_404(Leave, id=id)
    personnel = leave.personnel
    form = LeaveForm(data=request.POST or None, instance=leave)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "แก้ไขข้อมูลเรียบร้อย")
            return redirect('leaveDetail', id=leave.id)
        else:
            messages.add_message(request, messages.WARNING, "ข้อมูลไม่สมบูรณ์")
            context = {'form': form, 'personnel': personnel}
            return render(request, 'work/leave/leaveUpdate.html', context)
    else:
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/leave/leaveUpdate.html', context)

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
                    messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารได้")
                finally:
                    f.delete()
        leave.delete()
        messages.add_message(request, messages.SUCCESS, "ลบข้อมูลการลาสำเร็จ")
        return redirect('leaveList', divisionId=leave.personnel.division.id, personnelId=leave.personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'leave':leave, 'personnel': leave.personnel}
        return render(request, 'work/leave/leaveDelete.html', context)

def leaveDeleteFile(request, id):
    leaveFile = get_object_or_404(LeaveFile, id=id)
    leave = leaveFile.leave
    fname = leaveFile.file.name
    if os.path.exists('static/documents/leave/' + fname):
        try:
            os.remove('static/documents/leave/' + fname)  # file exits, delete it
            messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารสำเร็จ")
        except:
            messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารได้")
    leaveFile.delete()
    return redirect('leaveDetail', id=leave.id)

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
        messages.add_message(request, messages.SUCCESS, "ลบไฟล์เอกสารทั้งหมดสำเร็จ")
    else:
        messages.add_message(request, messages.WARNING, "ไม่สามารถลบไฟล์เอกสารบางไฟล์ได้ [" + fileerror+"]")
    return redirect('leaveDetail', id=leave.id)


def leaveDeleteURL(request, id):
    leaveURL = get_object_or_404(LeaveURL, id=id)
    leave = leaveURL.leave
    leaveURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารสำเร็จ")
    return redirect('leaveDetail', id=leave.id)

def leaveDeleteURLAll(request, id):
    leave = get_object_or_404(Leave, id=id)
    leaveURLs = leave.getLeaveURLs()
    for leaveURL in leaveURLs:
        leaveURL.delete()
    messages.add_message(request, messages.SUCCESS, "ลบลิงก์ตำแหน่งไฟล์เอกสารทั้งหมดสำเร็จ")
    return redirect('leaveDetail', id=leave.id)