from django import template
from workapp.models import *

register = template.Library()
@register.simple_tag
def fiscalYearValue(val=None):
  return val

@register.simple_tag
def eduYearValue(val=None):
  return val

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
