from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from baseapp.models import *
from baseapp.forms import *

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
            form.save()
            return redirect('personnelList')
        else:
            context = {'form': form}
            return render(request, 'base/personnelNew.html', context)
    else:
        form = PersonnelForm()
        context = {'form': form}
        return render(request, 'base/personnelNew.html', context)


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
