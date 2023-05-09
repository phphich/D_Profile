from django.db.models import Max
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from baseapp.models import *
from baseapp.forms import *
import os
from django.contrib import messages
from django.core.paginator import (Paginator, EmptyPage,PageNotAnInteger,)

# import plotly.graph_objs as go
# import pandas as pd
# import plotly.express as px

def home(request):
    return render(request, 'home.html')


# Division CRUD.
def divisionList(request):
    divisions = Division.objects.all().order_by('name_th')
    context = {'divisions': divisions}
    return render(request, 'base/division/divisionList.html', context)


def divisionNew(request):
    if request.method == 'POST':
        form = DivisionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('divisionList')
        else:
            context = {'form': form}
            return render(request, 'base/division/divisionNew.html', context)
    else:
        form = DivisionForm()
        context = {'form': form}
        return render(request, 'base/division/divisionNew.html', context)


def divisionUpdate(request, id):
    division = get_object_or_404(Division, id=id)
    form = DivisionForm(data=request.POST or None, instance=division)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('divisionList')
        else:
            context = {'form': form}
            return render(request, 'base/division/divisionUpdate.html')
    else:
        context = {'form': form}
        return render(request, 'base/division/divisionUpdate.html', context)


def divisionDelete(request, id):
    division = get_object_or_404(Division, id=id)
    form = DivisionForm(data=request.POST or None, instance=division)
    if request.method == 'POST':
        division.delete()
        return redirect('divisionList')
    else:
        form.deleteForm()
        context = {'form': form, 'division': division}
        return render(request, 'base/division/divisionDelete.html', context)


# Curriculum CRUD.
def curriculumList(request):
    curriculums = Curriculum.objects.all().order_by('name_th')
    context = {'curriculums': curriculums}
    return render(request, 'base/curriculum/curriculumList.html', context)


def curriculumNew(request):
    if request.method == 'POST':
        form = CurriculumForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('curriculumList')
        else:
            context = {'form': form}
            return render(request, 'base/curriculum/curriculumNew.html', context)
    else:
        form = CurriculumForm()
        context = {'form': form}
        return render(request, 'base/curriculum/curriculumNew.html', context)


def curriculumUpdate(request, id):
    curriculum = get_object_or_404(Curriculum, id=id)
    form = CurriculumForm(data=request.POST or None, instance=curriculum)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('curriculumList')
        else:
            context = {'form': form}
            return render(request, 'base/curriculum/curriculumUpdate.html')
    else:
        context = {'form': form}
        return render(request, 'base/curriculum/curriculumUpdate.html', context)


def curriculumDelete(request, id):
    curriculum = get_object_or_404(Curriculum, id=id)
    form = CurriculumForm(data=request.POST or None, instance=curriculum)
    if request.method == 'POST':
        curriculum.delete()
        return redirect('curriculumList')
    else:
        form.deleteForm()
        context = {'form': form, 'curriculum': curriculum}
        return render(request, 'base/curriculum/curriculumDelete.html', context)


# Personnel CRUD.
def personnelList(request):
    personnels = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th')
    context = {'personnels': personnels}
    return render(request, 'base/personnel/personnelList.html', context)

def personnelListPage(request, pageNo=None):
    iterm_per_page =5
    if pageNo == None:
        pageNo = 1
    division = Division.objects.all().order_by('name_th')
    listDivPersonCount = {}
    for div in division:
        count = div.getCountPersonnel()
        listDivPersonCount[div.name_th] = count
    # ทำ Plotly Graph
    productsAll = Products.objects.all()
    products = []
    amounts = []
    for item in productsAll:
        products.append(item.name)
        amounts.append(item.getSaleAmount())
    # กรณีอ่านค่าจากบางฟิลด์ใน model มาใช้งาน
    # products = Products.objects.values_list('name', 'samplesale__amount')
    # df = pd.DataFrame(products,  columns=['Product', 'Amount'])
    # ..................
    # df = pd.DataFrame({"Product":products, "Amount":amounts}, columns=['Product', 'Amount'])
    # fig = px.bar(df, x='Product', y='Amount', title="แผนภูมิแท่งแสดงยอดขายแยกตามรายชื่อสินค้า")
    # fig.update_layout(autosize = False, width = 600,  height = 400,
    #                   margin = dict(l=10, r=10, b=100, t=100, pad=5 ),
    #                   paper_bgcolor = "aliceblue",)
    # chart = fig.to_html()
    # context = {'chart':chart}

    personnels = Personnel.objects.all().order_by('division__name_th', 'firstname_th', 'lastname_th')
    personnels_page = Paginator(personnels, iterm_per_page)
    context = {'personnels': personnels_page.page(pageNo)}
    return render(request, 'base/personnel/personnelListPage.html', context)

def personnelNew(request):
    if request.method == 'POST':
        form = PersonnelForm(data=request.POST or None, files=request.FILES)
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
            personnel = get_object_or_404(Personnel, email=email)
            newfilename = 'images/personnels/' + str(personnel.id) + ext
            personnel.picture.name = newfilename
            personnel.save()
            if os.path.exists('static/' + personnel.picture.name):
                os.remove('static/' + personnel.picture.name)  # file exits, delete it
            os.rename('static/' + filename, 'static/' + personnel.picture.name)
            return redirect('personnelListPage', pageNo=1)
        else:
            context = {'form': form}
            return render(request, 'base/personnel/personnelNew.html', context)
    else:
        form = PersonnelForm()
        context = {'form': form}
        return render(request, 'base/personnel/personnelNew.html', context)

def personnelDetail(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    context = {'personnel': personnel}
    return render(request, 'base/personnel/personnelDetail.html', context)


def personnelUpdate(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    oldpicture = personnel.picture.name  # รูปเดิม
    if request.method == 'POST':
        form = PersonnelForm(data=request.POST, instance=personnel, files=request.FILES)
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
                print("file name2:" + filename)
                print("new file name: " + newfilename)
                personnel.picture.name = newfilename  # ต้องอัพเดท เผื่อกรณีที่เปลี่ยนชนิดไฟล์ภาพ
                personnel.save()
                if os.path.exists('static/' + oldpicture):  # delete older picture profile
                    os.remove('static/' + oldpicture)
                os.rename('static/' + filename, 'static/' + personnel.picture.name)
            else:
                form.save()
            return redirect('personnelListPage', pageNo=1)
        else:
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/personnel/personnelUpdate.html', context)
    else:
        form = PersonnelForm(instance=personnel)
        form.updateForm()
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/personnel/personnelUpdate.html', context)


def personnelDelete(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    picturefile = personnel.picture.name
    form = PersonnelForm(data=request.POST or None, instance=personnel)
    if request.method == 'POST':
        personnel.delete()
        # delete picture file
        if os.path.exists('static/' + picturefile):
            os.remove('static/' + picturefile)  # file exits, delete it
        return redirect('personnelListPage', pageNo=1)
    else:
        form.deleteForm()
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/personnel/personelDelete.html', context)


# Education CRUD.
def educationList(request, divisionId=None, personnelId=None):
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
    context = {'divisions': divisions, 'division': division, 'personnel': personnel}
    return render(request, 'base/education/educationList.html', context)


def educationNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    if request.method == 'POST':
        form = EducationForm(data=request.POST)
        if form.is_valid():
            form.save()
            divisions = Division.objects.all().order_by('name_th')
            return redirect('educationList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/education/educationNew.html', context)
    else:
        form = EducationForm(initial={'personnel': personnel, 'recorder': personnel})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/education/educationNew.html', context)

def educationDetail(request, id):
    education = Education.objects.filter(id=id).first()
    context = {'education': education}
    return render(request, 'base/education/educationDetail.html', context)

def educationUpdate(request, id):
    education = get_object_or_404(Education, id=id)
    personnel = education.personnel
    form = EducationForm(data=request.POST or None, instance=education, initial={'recorder': education.personnel})
    if request.method == 'POST':
        if form.is_valid():
            divisions = Division.objects.all().order_by('name_th')
            form.save()
            return redirect('educationList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/education/educationUpdate.html', context)
    else:
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/education/educationUpdate.html', context)


def educationDelete(request, id):
    education = get_object_or_404(Education, id=id)
    personnel = education.personnel
    form = EducationForm(instance=education)
    if request.method == 'POST':
        divisions = Division.objects.all().order_by('name_th')
        education.delete()
        return redirect('educationList', divisionId=personnel.division.id, personnelId=personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'personnel': education.personnel}
        return render(request, 'base/education/educationDelete.html', context)


# Expertise CRUD.
def expertiseList(request, divisionId=None, personnelId=None):
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
    context = {'divisions': divisions, 'division': division, 'personnel': personnel}
    return render(request, 'base/expertise/expertiseList.html', context)

def expertiseNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    if request.method == 'POST':
        form = ExpertiseForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('expertiseList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/expertise/expertiseNew.html', context)
    else:
        form = ExpertiseForm(initial={'personnel': personnel, 'recorder': personnel})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/expertise/expertiseNew.html', context)


def expertiseDetail(request, id):
    expertise = Expertise.objects.filter(id=id).first()
    context = {'expertise': expertise}
    return render(request, 'base/expertise/expertiseDetail.html', context)


def expertiseUpdate(request, id):
    expertise = get_object_or_404(Expertise, id=id)
    personnel = expertise.personnel
    form = ExpertiseForm(data=request.POST or None, instance=expertise, initial={'recorder': expertise.personnel})
    if request.method == 'POST':
        if form.is_valid():
            divisions = Division.objects.all().order_by('name_th')
            form.save()
            return redirect('expertiseList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            context = {'form': form, 'personnel': personnel}
            return render(request, 'base/expertise/expertiseUpdate.html', context)
    else:
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/expertise/expertiseUpdate.html', context)


def expertiseDelete(request, id):
    expertise = get_object_or_404(Expertise, id=id)
    personnel = expertise.personnel
    form = ExpertiseForm(instance=expertise)
    if request.method == 'POST':
        divisions = Division.objects.all().order_by('name_th')
        expertise.delete()
        return redirect('expertiseList', divisionId=personnel.division.id, personnelId=personnel.id)
    else:
        form.deleteForm()
        context = {'form': form, 'personnel': expertise.personnel}
        return render(request, 'base/expertise/expertiseDelete.html', context)

# CurrAffiliation CRUD.
def currAffiliationList(request, curriculumId = None):
    curriculum = None
    # for next time, recorder must used user login
    recorder = Personnel.objects.all().first()
    if request.method == 'POST':
        if 'action' in request.POST:
            form = CurrAffiliationForm(data=request.POST)
            print("form", form)
            if form.is_valid():
                newForm = form.save(commit=False)
                person = Personnel.objects.filter(id=newForm.personnel.id).first()
                curriculum = Curriculum.objects.filter(id=newForm.curriculum.id).first()
                currAffs  = curriculum.getCurrAffiliation()
                duplicate = False
                for currAff in currAffs:
                    if currAff.personnel == person:
                        messages.add_message(request, messages.WARNING, 'บุคลากรที่เลือกมีรายชื่อในการบริหารหลักสูตรอยู่แล้ว')
                        duplicate = True
                        break
                if duplicate == False:
                    newForm.save()
                    messages.add_message(request, messages.SUCCESS, 'บันทึกข้อมูลผู้บริหารหลักสูตรสำเร็จ')
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

def currAffiliationDelete(request,id):
    currAffiliation = get_object_or_404(CurrAffiliation, id=id)
    # for next time, recorder must used user login
    recorder = Personnel.objects.all().first()

    curriculum = currAffiliation.curriculum
    curriculums = Curriculum.objects.all().order_by('name_th')
    form = CurrAffiliationForm(initial={'curriculum': curriculum, 'recorder': recorder})
    context = {'curriculums': curriculums, 'curriculum': curriculum, 'form': form}
    currAffiliation.delete()
    # return render(request, 'base/currAffiliationList.html', context)
    return redirect('currAffiliationList', curriculumId=curriculum.id)




