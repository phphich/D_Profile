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

# @register.filter(name='getPracticeResult')
# def getPracticeResult(stdid, pid):
#     score = Score.objects.filter(student_id=stdid).filter(problem_id=pid).first()
#     if score is None:
#         return 0
#     else:
#         return score.result
