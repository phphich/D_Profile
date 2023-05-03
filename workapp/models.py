from django.db import models
from baseapp.models import *

class Command(models.Model):
    comId = models.CharField(max_length=30, default="")
    comDate = models.DateField(default=None)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.CharField(max_length=10, default="")
    mission = models.CharField(max_length=50, default="การจัดการเรียนการสอน")
    topic = models.TextField(default=None)
    detail = models.TextField(default=None)
    personnel = models.ForeignKey(Personnel, related_name='PersonnelCom', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderCom', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName + " " + self.personnel.lastName +\
               "  " + self.commandId + " " + self.topic + " (" + str(self.commandDate)+ ")"

class Leave(models.Model):
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    days = models.IntegerField(default=1)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    leaveType = models.CharField(max_length=50, default=None)
    reason = models.CharField(max_length=255, default=None)
    personnel = models.ForeignKey(Personnel, related_name='PersonnelLeave', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderLeave', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName + " " + self.personnel.lastName + \
                "  " + self.leaveType + " : " + str(self.startDate) + " - " + str(self.endDate) + \
                "  " + self.leaveType + " (" + str(self.days) + ")"

class Training(models.Model):
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    days = models.IntegerField(default=1)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.IntegerField(default=0)
    topic = models.CharField(max_length=255, default=None)
    place = models.CharField(max_length=255, default=None)
    budget = models.FloatField(default=0.00)
    budgetType = models.CharField(max_length=30, default="งบประมาณรายได้")
    personnel = models.ForeignKey(Personnel, related_name='PersonnelTraining', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderTraining', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName + " " + self.personnel.lastName + \
               "  " + self.topic + " : " + str(self.startDate) + " - " + str(self.endDate) + \
               " (" + str(self.days) + ")"

class Research(models.Model):
    fiscalYear = models.IntegerField(default=0)
    title_th = models.TextField(default="")
    title_en = models.TextField(default="")
    objective = models.TextField(default="")
    percent_resp = models.IntegerField(default=100)
    budget = models.FloatField(default=0.00)
    budgetType = models.CharField(max_length=30, default="งบประมาณรายได้")
    source = models.CharField(max_length=255, default="")
    keyword = models.TextField(default="")
    percent_success = models.IntegerField(default=0)
    publish_method = models.TextField(default="")
    personnel = models.ForeignKey(Personnel, related_name='PersonnelResearch', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderResearch', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName + " " + self.personnel.lastName + \
               "  " + self.title_th + " - " + str(self.fiscalYear) + " : " + str(self.budget)

class SocialService(models.Model):
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    days = models.IntegerField(default=1)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.IntegerField(default=0)
    topic = models.FloatField(default=0.00)
    objective = models.TextField(default="")
    place = models.CharField(max_length=255, default="")
    budget = models.FloatField(default=0.00)
    budgetType = models.CharField(max_length=30, default="งบประมาณรายได้")
    source = models.CharField(max_length=255, default="")
    receiver = models.CharField(max_length=255, default="")
    num_receiver = models.IntegerField(default = 0)
    personnel = models.ForeignKey(Personnel, related_name='PersonnelSocialService', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderSocialService', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName + " " + self.personnel.lastName + \
               "  " + self.topic + " : " + self.place + " : " + str(self.startDate) + "-" + str(self.endDate)

class Performance(models.Model):
    getDate = models.DateField(default=None)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.IntegerField(default=0)
    topic = models.CharField(max_length=255, default=None)
    detail = models.TextField(default=None)
    budget = models.FloatField(default=0.00)
    budgetType = models.CharField(max_length=30, default="งบประมาณรายได้")
    source = models.CharField(max_length=255, default="")
    personnel = models.ForeignKey(Personnel, related_name='PersonnelPerformance', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderPerformance', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName + " " + self.personnel.lastName + \
               "  " + self.topic + " : " + str(self.getDate)
