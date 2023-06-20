from django import template
from workapp.models import *
from workapp import common

register = template.Library()
@register.simple_tag
def groupValue(val=None):
    return val

@register.filter(name='aimphich')
def iamphich(name=None):
    a = "***-" + name + "-***"

@register.filter(name='strFormatValue')
def strFormatValue(strValue=None):
    return strValue

@register.filter(name='getTimeUpdate')
def getTimeUpdate(docDate):
    return common.chkUpdateTime(docDate)

@register.filter(name='is_in_list')
def is_in_list(value, given_list):
    return True if value in given_list else False

@register.filter(name='getCountCommandPersonnelDivision')
def getCountCommandPersonnelDivision(divId, comId):
    command = Command.objects.filter(id=comId).first()
    division = Division.objects.filter(id=divId).first()
    personnels= Personnel.objects.filter(division=division)
    # count = commPerson.count()
    # print('personnels')
    # print(personnels)
    count = CommandPerson.objects.filter(command=command).filter(personnel__in=personnels).aggregate(count=Count('id'))
    return count['count']

@register.filter(name='getCountResearchPersonnelDivision')
def getCountResearchPersonnelDivision(divId, comId):
    research = Research.objects.filter(id=comId).first()
    division = Division.objects.filter(id=divId).first()
    personnels= Personnel.objects.filter(division=division)
    count = ResearchPerson.objects.filter(research=research).filter(personnel__in=personnels).aggregate(count=Count('id'))
    return count['count']

@register.filter(name='getCountsocialservicePersonnelDivision')
def getCountsocialservicePersonnelDivision(divId, socialserviceId):
    socialservice = SocialService.objects.filter(id=socialserviceId).first()
    division = Division.objects.filter(id=divId).first()
    personnels= Personnel.objects.filter(division=division)
    count = SocialServicePerson.objects.filter(socialservice=socialservice).filter(personnel__in=personnels).aggregate(count=Count('id'))
    return count['count']

from django.utils.safestring import mark_safe
import re
@register.filter(name='setHilight')
def setHilight(text, keyword):
    rekeyword =  re.compile(re.escape(keyword), re.IGNORECASE)
    text = rekeyword.sub(keyword, text)
    hilightText = text.replace(keyword, '<span style = "font-weight: bold; background-color:yellow;color:green">{}</span>'.format(keyword))
    return mark_safe(hilightText)

@register.filter(name='chkPermissReport')
def chkPermissReport(group, userId, userType, reportId):
    permission = False
    if userType == 'Header':
        header = Header.objects.filter(personnel_id=userId).first()
        personnelSet = Division.getPersonnels(division=header.division)
    elif userType == 'Staff':
        staff = Responsible.objects.filter(personnel_id=userId).first()
        personnelSet = Responsible.getPersonnelResponsibles()

    if group == 'personnel':
        reportSet = Personnel.objects.filter(id=reportId).first()
        if userId == reportSet.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == reportSet.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission == True
                    break
    elif group == 'education':
        reportSet = Education.objects.filter(id=reportId).first()
        if userId == reportSet.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == reportSet.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission == True
                    break
    elif group == 'expertise':
        reportSet = Expertise.objects.filter(id=reportId).first()
        if userId == reportSet.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == reportSet.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission == True
                    break
    elif group == 'training':
        reportSet = Training.objects.filter(id=reportId).first()
        if userId == reportSet.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == reportSet.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission == True
                    break
    elif group == 'performance':
        reportSet = Performance.objects.filter(id=reportId).first()
        if userId == reportSet.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == reportSet.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission == True
                    break
    elif group == 'leave':
        reportSet = Leave.objects.filter(id=reportId).first()
        if userId == reportSet.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == reportSet.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission == True
                    break
    elif group == 'resarch':
        reportSet = Research.objects.filter(id=reportId).first()
        # reportSet = ResearchPerson.objects.filter(id=reportId).first() 
        researcherSet = reportSet.getResearchPerson()
        if userId == reportSet.personnel.id:
            permission = True
    elif group == 'socialservice':
        pass
