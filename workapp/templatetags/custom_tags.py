from django import template
from workapp.models import *
from workapp import common

register = template.Library()
@register.simple_tag
def groupValue(val=None):
  return val

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
