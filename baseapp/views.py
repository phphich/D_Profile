from django.conf import settings
from django.db.models import Max
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from baseapp.models import *
from baseapp.forms import *
import os
import D_Profile.settings

def home(request):
    return render(request, 'home.html')

def personnelList(request):
    personnels = Personnel.objects.all()
    context = {'personnels':personnels}
    return render(request, 'base/personnelList.html', context)

def personnelNew(request):
    if request.method == 'POST':
        form = PersonnelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            id_max = Personnel.objects.all().aggregate(Max('id'))['id__max']
            id = id_max + 1 if id_max else 1
            newForm = form.save(commit=False)
            # id = newForm.id
            # print("id: "+ str(id_next) )
            # filename = newForm.picture.name
            filepath = newForm.picture.name
            filepath = filepath.replace(' ', '_')
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = filenames[len(filenames) - 1]
            # filename = filename
            newfilename = str(id) + ext
            newForm.save()  # product_tmp/xxx.xxx
            personnel = get_object_or_404(Personnel, id=id)
            personnel.picture.name = 'images/personnels/' + newfilename  # pxxx.xxx
            personnel.save()
            if os.path.exists('static/images/personnels/' + newfilename):
                os.remove('static/images/personnesl/' + newfilename)  # file exits, delete it
            os.rename('static/images/personnels/'+filename, 'static/images/personnels/' + newfilename)
            return redirect('personnelList')
        else:
            context = {'form': form}
            return render(request, 'base/personnelNew.html', context)
    else:
        form = PersonnelForm()
        context = {'form': form}
        return render(request, 'base/personnelNew.html', context)

def personnelDetail(request, id):
    personnel = Personnel.objects.filter(id=id).first()
    context = {'personnel':personnel}
    return render(request, 'base/personnelDetail.html', context)

def personnelUpdate(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    form = PersonnelForm(data=request.POST or None, instance=personnel)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('personnelList')
        else:
            context = {'form': form}
            return render(request, 'base/personnelUpdate.html', context)
    else:
        context = {'form': form}
        return render(request, 'base/personnelUpdate.html', context)

def categoryDelete(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    form = PersonnelForm(data=request.POST or None, instance=personnel)
    if request.method == 'POST':
        personnel.delete()
        return redirect('personnelList')
    else:
        form.deleteForm()
        context = {'form': form, 'personnel': personnel}
        return render(request, 'base/personelDelete.html', context)
