from django.db import models
from baseapp.models import *

class Command(models.Model):
    commandId = models.CharField(max_length=15, default="")
    commandDate = models.DateField(default=None)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.CharField(max_length=10, default="")
    topic = models.CharField(max_length=255, default=None)
    mission = models.CharField(max_length=50, default="การจัดการเรียนการสอน")
    detail = models.TextField(default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.commandId + " " + self.topic + " (" + str(self.commandDate)+ ")"

class Leave(models.Model):
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    days = models.IntegerField(default=1)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.IntegerField(default=0)
    leaveType = models.CharField(max_length=50, default=None)
    reason = models.CharField(max_length=255, default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.leaveType + " : " + str(self.startDate) + " - " + str(self.endDate) + self.leaveType + " (" + str(self.days) + ")"

class Trainning(models.Model):
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
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.topic + " : " + str(self.startDate) + " - " + str(self.endDate) + self.leaveType + " (" + str(
            self.days) + ")"

class Performance(models.Model):
    getDate = models.DateField(default=None)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.IntegerField(default=0)
    topic = models.CharField(max_length=255, default=None)
    detail = models.TextField(default=None)
    budget = models.FloatField(default=0.00)
    budgetType = models.CharField(max_length=30, default="งบประมาณรายได้")
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.topic + " : " + str(self.getDate)



