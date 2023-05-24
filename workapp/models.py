import fileinput

from django.db import models
from baseapp.models import *

# def getCommand(self):
#     commands = Command.objects.filter(personnel=self).order_by('id')
#     return commands
# def getResearch(self):
#     researchs = Research.objects.filter(personnel=self).order_by('id')
#     return researchs
# def getSocialService(self):
#     socialServices = SocialService.objects.filter(personnel=self).order_by('id')
#     return socialServices
# def getTraining(self):
#     trainings = Training.objects.filter(personnel=self).order_by('id')
#     return trainings
# def getLeave(self):
#     leaves = Leave.objects.filter(personnel=self).order_by('id')
#     return leaves
# def getPerformance(self):
#     performances = Performance.objects.filter(personnel=self).order_by('id')
#     return performances

class Command(models.Model):
    comId = models.CharField(max_length=30, default="")
    comDate = models.DateField(default=None)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.CharField(max_length=10, default="")
    mission = models.CharField(max_length=50, default="การจัดการเรียนการสอน")
    topic = models.TextField(default=None)
    detail = models.TextField(default=None)
    personnel = models.ForeignKey(Personnel, related_name='RecorderCommand', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.comId + " " + self.topic + " (" + str(self.comDate)+ ")"
    def getPersonnel(self):
        personnels = CommandPerson.objects.filter(command=self).order_by('personnel__firstname_th', 'personnel__lastname_th')
        return personnels
    def getCountPersonnel(self):
        count = CommandPerson.objects.filter(command=self).aggregate(count=Count('id'))
        return count['count']

class CommandPerson(models.Model):
    status = models.CharField(max_length=30, default="")
    command = models.ForeignKey(Command, on_delete=models.CASCADE, default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.command.comId + " : " + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " +  " (" + self.status + ")"
class CommandFile(models.Model):
    file = models.FileField(upload_to='static/documents/command', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "(" + str(self.command.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype

class CommandURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "[" + str(self.command.id) + "_" + str(self.id) + "]_"+ self.url

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
        return self.personnel.status + self.personnel.firstName_th + " " + self.personnel.lastName_th +\
                "  " + self.leaveType+ " : " + str(self.startDate) + " - " + str(self.endDate) + \
                "  " + self.leaveType + " (" + str(self.days) + ")"
    def getLeaveFiles(self):
        leaveFiles = LeaveFile.objects.filter(leave=self)
        return leaveFiles
    def getLeaveURLs(self):
        leaveURLs = LeaveURL.objects.filter(leave=self)
        return leaveURLs

class LeaveFile(models.Model):
    file = models.FileField(upload_to='static/documents/leave', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "(" + str(self.leave.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype

class LeaveURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "[" + str(self.leave.id) + "_" + str(self.id) + "]_"+ self.url

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
        return self.personnel.status + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " + self.topic + " : " + str(self.startDate) + " - " + str(self.endDate) + \
               " (" + str(self.days) + ")"
    def getTrainingFiles(self):
        trainingFiles = TrainingFile.objects.filter(training=self)
        return trainingFiles
    def getTrainingURLs(self):
        trainingURLs = TrainingURL.objects.filter(training=self)
        return trainingURLs
    def getSemeter(self):
        if self.eduSemeter== 3:
            return "ฤดูร้อน"
        else:
            return self.eduSemeter

class TrainingFile(models.Model):
    file = models.FileField(upload_to='static/documents/training', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "(" + str(self.training.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype

class TrainingURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "[" + str(self.training.id) + "_" + str(self.id) + "]_"+ self.url

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
    personnel = models.ForeignKey(Personnel, related_name='RecorderResearch', on_delete=models.CASCADE, default=None)
    # recorder = models.ForeignKey(Personnel, related_name='RecorderResearch', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " + self.title_th + " - " + str(self.fiscalYear) + " : " + str(self.budget)

class ResearchPerson(models.Model):
    status = models.CharField(max_length=30, default="")
    research = models.ForeignKey(Research, on_delete=models.CASCADE, default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.research.id + " : " + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " +  " (" + self.status + ")"

class ResearchFile(models.Model):
    file = models.FileField(upload_to='static/documents/research', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    research = models.ForeignKey(Research, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "(" + str(self.research.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype

class ResearchURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    research = models.ForeignKey(Research, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "[" + str(self.research.id) + "_" + str(self.id) + "]_"+ self.url

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
    personnel = models.ForeignKey(Personnel, related_name='RecorderSocialService', on_delete=models.CASCADE, default=None)
    # recorder = models.ForeignKey(Personnel, related_name='RecorderSocialService', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " + self.topic + " : " + self.place + " : " + str(self.startDate) + "-" + str(self.endDate)

class SocialServicePerson(models.Model):
    status = models.CharField(max_length=30, default="")
    socialservice = models.ForeignKey(SocialService, on_delete=models.CASCADE, default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.socialservice.id + " : " + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " +  " (" + self.status + ")"

class SocialServiceFile(models.Model):
    file = models.FileField(upload_to='static/documents/socialservice', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    socialservice = models.ForeignKey(SocialService, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "(" + str(self.socialservice.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype

class SocialServiceURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    socialservice = models.ForeignKey(SocialService, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "[" + str(self.socialservice.id) + "_" + str(self.id) + "]_"+ self.url

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
        return self.personnel.status + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " + self.topic + " : " + str(self.getDate)
    def getPerformanceFiles(self):
        performanceFiles = PerformanceFile.objects.filter(performance=self)
        return performanceFiles
    def getPerformanceURLs(self):
        performanceURLs = PerformanceURL.objects.filter(performance=self)
        return performanceURLs
    def getSemeter(self):
        if self.eduSemeter== 3:
            return "ฤดูร้อน"
        else:
            return self.eduSemeter


class PerformanceFile(models.Model):
    file = models.FileField(upload_to='static/documents/performance', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "(" + str(self.performance.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype

class PerformanceURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "[" + str(self.performance.id) + "_" + str(self.id) + "]_"+ self.url
