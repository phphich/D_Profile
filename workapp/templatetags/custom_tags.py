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

# @register.filter(name='chkPermissionReport')
@register.simple_tag(name='chkPermissionReport')
def chkPermissionReport(group, userId, userType, reportId):
    permission = False
    if userType in ['Administrator', 'Manager']:
        return True
    elif userType == 'Header':
        header = Header.objects.filter(personnel_id=userId).first()
        division = header.division
        personnelSet = division.getPersonnels()
    elif userType == 'Staff':
        staff = Responsible.objects.filter(personnel_id=userId).first()
        personnelSet = Responsible.getPersonnelResponsibles(userId)
    else: #personnel
        personnelSet = [Personnel.objects.filter(id=userId).first()]

    if group == 'personnel':
        report = Personnel.objects.filter(id=reportId).first()
        if userId == report.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == report.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission = True
    elif group == 'education':
        report = Education.objects.filter(id=reportId).first()
        if userId == report.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == report.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission = True
    elif group == 'expertise':
        report = Expertise.objects.filter(id=reportId).first()
        if userId == report.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == report.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission = True
    elif group == 'training':
        report = Training.objects.filter(id=reportId).first()
        if userId == report.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == report.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission = True
    elif group == 'performance':
        report = Performance.objects.filter(id=reportId).first()
        if userId == report.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == report.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission = True
    elif group == 'leave':
        report = Leave.objects.filter(id=reportId).first()
        if userId == report.personnel.id:
            permission = True
        else:
            for personnel in personnelSet:
                if personnel.id == report.personnel.id: #ถ้ารหัสบุคลากรที่รายงานตรงกับรหัสบุคลากรที่ผู้ล็อกอินบริหารหรือดูแลข้อมูลให้อยู่
                    permission = True
    elif group == 'research':
        report = Research.objects.filter(id=reportId).first()
        if report.recorder_id == userId:
            permission=True
        else:
            researchers = ResearchPerson.objects.filter(research=report)
            for researcher in researchers:
                for personnel in personnelSet:
                    if personnel.id == researcher.personnel.id:
                        permission=True
    elif group == 'socialservice':
        report = SocialService.objects.filter(id=reportId).first()
        if report.recorder_id == userId:
            permission=True
        else:
            operators = SocialServicePerson.objects.filter(socialservice=report)
            for operator in operators:
                for personnel in personnelSet:
                    if personnel.id == operator.personnel.id:
                        permission=True
    elif group == 'command':
        report = Command.objects.filter(id=reportId).first()
        if report.recorder_id == userId:
            permission=True
        else:
            operators = CommandPerson.objects.filter(command=report)
            for operator in operators:
                for personnel in personnelSet:
                    if personnel.id == operator.personnel.id:
                        permission=True
    return permission