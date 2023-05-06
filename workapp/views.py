import datetime

from django.db.models import Max
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from workapp.models import *
from workapp.forms import *
import os
from django.contrib import messages

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
    return render(request, 'work/leaveList.html', context)

def leaveNew(request, id):
    personnel = get_object_or_404(Personnel, id=id)
    if request.method == 'POST':
        form = LeaveForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('leaveList', divisionId=personnel.division.id, personnelId=personnel.id)
        else:
            context = {'form': form, 'personnel': personnel}
            return render(request, 'work/leaveNew.html', context)
    else:
        today = datetime.date.today()
        currentYear = today.year

        form = LeaveForm(initial={'personnel': personnel, 'recorder': personnel, 'fiscalYear':currentYear, 'eduYear':currentYear})
        context = {'form': form, 'personnel': personnel}
        return render(request, 'work/leaveNew.html', context)

def leaveDetail(request, id):
    pass

def leaveUpdate(request, id):
    pass

def leaveDelete(request, id):
    pass





