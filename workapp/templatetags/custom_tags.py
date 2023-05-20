from django import template
from workapp.models import *

register = template.Library()
@register.simple_tag
def fiscalValue(val=None):
  return val

# @register.filter(name='getPracticeResult')
# def getPracticeResult(stdid, pid):
#     score = Score.objects.filter(student_id=stdid).filter(problem_id=pid).first()
#     if score is None:
#         return 0
#     else:
#         return score.result
