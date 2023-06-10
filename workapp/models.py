import fileinput
from django.db import models
from baseapp.models import *

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
    editor = models.ForeignKey(Personnel, related_name='EditorLeave', on_delete=models.CASCADE, default=None)
    editDate = models.DateTimeField(auto_now_add = True)
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
    # def getTimeUpdate(self):
    #     return common.chkUpdateTime(self.recordDate)
    @staticmethod
    def getCountPersonLeave(personnel): #นับจำนวนครั้งที่บุคลากรรายหนึ่งทำเกี่ยวกับการลา
        countLeave = Leave.objects.filter(Q(personnel=personnel) or Q(recorder=personnel) or Q(editor=personnel)).count()
        countLeaveFile = LeaveFile.objects.filter(recorder=personnel).count()
        countLeaveURL = LeaveURL.objects.filter(recorder=personnel).count()        
        countAll = countLeave + countLeaveFile + countLeaveURL
        return countAll
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        editor  = Personnel.objects.filter(id=self.editor.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        editDate = self.editDate.strftime('%d/%m/%Y %H:%M:%S')
        if recorder == editor and recordDate == editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'
        elif recorder == editor and recordDate != editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate + \
                   '), แก้ไขเมื่อ:' + ' ('+ editDate +')'
        else:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + \
                   '), แก้ไขโดย:' + editor.firstname_th + ' ' + editor.lastname_th + ' ('+ editDate +')'

class LeaveFile(models.Model):
    file = models.FileField(upload_to='static/documents/leave', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderLeaveFile', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "(" + str(self.leave.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'

class LeaveURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE, default=None)
    description = models.CharField(max_length=255, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderLeaveURL', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description + ' (' + self.url + ')'
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'

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
    editor = models.ForeignKey(Personnel, related_name='EditorTraining', on_delete=models.CASCADE, default=None)
    editDate = models.DateTimeField(auto_now_add = True)
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
    # def getTimeUpdate(self):
    #     return common.chkUpdateTime(self.recordDate)
    @staticmethod
    def getCountPersonTraining(personnel):  # นับจำนวนครั้งที่บุคลากรรายหนึ่งทำเกี่ยวกับการลา
        countTraining = Training.objects.filter(Q(personnel=personnel) or Q(recorder=personnel) or Q(editor=personnel)).count()
        countTrainingFile = TrainingFile.objects.filter(recorder=personnel).count()
        countTrainingURL = TrainingURL.objects.filter(recorder=personnel).count()
        countAll = countTraining + countTrainingFile + countTrainingURL
        return countAll    
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        editor  = Personnel.objects.filter(id=self.editor.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        editDate = self.editDate.strftime('%d/%m/%Y %H:%M:%S')
        if recorder == editor and recordDate == editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'
        elif recorder == editor and recordDate != editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate + \
                   '), แก้ไขเมื่อ:' + ' ('+ editDate +')'
        else:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + \
                   '), แก้ไขโดย:' + editor.firstname_th + ' ' + editor.lastname_th + ' ('+ editDate +')'

class TrainingFile(models.Model):
    file = models.FileField(upload_to='static/documents/training', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderTrainingFile', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "(" + str(self.training.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'

class TrainingURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderTrainingURL', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description + ' (' + self.url + ')'
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'

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
    editor = models.ForeignKey(Personnel, related_name='EditorPerformance', on_delete=models.CASCADE, default=None)
    editDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " + self.topic + " : " + str(self.getDate)
    def getRecorder(self):
        return self.recorder.status + self.recorder.firstname_th + ' ' + self.recorder.lastname_th
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
    # def getTimeUpdate(self):
    #     return common.chkUpdateTime(self.recordDate)
    @staticmethod
    def getCountPersonPerformance(personnel):  # นับจำนวนครั้งที่บุคลากรรายหนึ่งทำเกี่ยวกับการลา
        countPerformance = Performance.objects.filter(Q(personnel=personnel) or Q(recorder=personnel) or Q(editor=personnel)).count()
        countPerformanceFile = PerformanceFile.objects.filter(recorder=personnel).count()
        countPerformanceURL = PerformanceURL.objects.filter(recorder=personnel).count()
        countAll = countPerformance + countPerformanceFile + countPerformanceURL
        return countAll    
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        editor  = Personnel.objects.filter(id=self.editor.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        editDate = self.editDate.strftime('%d/%m/%Y %H:%M:%S')
        if recorder == editor and recordDate == editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'
        elif recorder == editor and recordDate != editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate + \
                   '), แก้ไขเมื่อ:' + ' ('+ editDate +')'
        else:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + \
                   '), แก้ไขโดย:' + editor.firstname_th + ' ' + editor.lastname_th + ' ('+ editDate +')'

class PerformanceFile(models.Model):
    file = models.FileField(upload_to='static/documents/performance', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderPerformanceFile', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "(" + str(self.performance.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'

class PerformanceURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderPerformanceURL', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description + ' (' + self.url + ')'
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'

class Command(models.Model):
    comId = models.CharField(max_length=30, default="")
    comDate = models.DateField(default=None)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.IntegerField(default=0)
    mission = models.CharField(max_length=50, default="การจัดการเรียนการสอน")
    topic = models.TextField(default=None)
    detail = models.TextField(default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderCommand', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    editor = models.ForeignKey(Personnel, related_name='EditorCommand', on_delete=models.CASCADE, default=None)
    editDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.comId + " " + self.topic + " (" + str(self.comDate)+ ")"
    def getEduYearAndSementer(self):
        return self.eduYear + self.eduSemeter
    def getSemeter(self):
        if self.eduSemeter== 3:
            return "ฤดูร้อน"
        else:
            return self.eduSemeter
    def getCommandPerson(self):
        personnels = CommandPerson.objects.filter(command=self).order_by('personnel__firstname_th', 'personnel__lastname_th')
        return personnels
    def getCountPersonnel(self): #จำนวนคนที่อยู่ในคำสั่ง
        count = CommandPerson.objects.filter(command=self).aggregate(count=Count('id'))
        return count['count']
    def getCommandFiles(self):
        commandFiles = CommandFile.objects.filter(command=self)
        return commandFiles
    def getCommandURLs(self):
        commandURLs = CommandURL.objects.filter(command=self)
        return commandURLs
    @staticmethod
    def getCountPersonCommand(personnel):  # นับจำนวนครั้งที่บุคลากรรายหนึ่งทำเกี่ยวกับการลา
        countCommand = Command.objects.filter(Q(recorder=personnel) or Q(editor=personnel)).count()
        countCommandPerson = CommandPerson.objects.filter(Q(personnel=personnel) or Q(recorder=personnel)).count()
        countCommandFile = CommandFile.objects.filter(recorder=personnel).count()
        countCommandURL = CommandURL.objects.filter(recorder=personnel).count()
        countAll = countCommand + countCommandPerson + countCommandFile + countCommandURL
        return countAll 
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        editor  = Personnel.objects.filter(id=self.editor.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        editDate = self.editDate.strftime('%d/%m/%Y %H:%M:%S')
        if recorder == editor and recordDate == editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'
        elif recorder == editor and recordDate != editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate + \
                   '), แก้ไขเมื่อ:' + ' ('+ editDate +')'
        else:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + \
                   '), แก้ไขโดย:' + editor.firstname_th + ' ' + editor.lastname_th + ' ('+ editDate +')'

class CommandPerson(models.Model):
    status = models.CharField(max_length=30, default="")
    command = models.ForeignKey(Command, on_delete=models.CASCADE, default=None)
    personnel = models.ForeignKey(Personnel, related_name='PersonnelCommandPerson', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderCommandPerson',on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.command.comId + " : " + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " +  " (" + self.status + ")"
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'

class CommandFile(models.Model):
    file = models.FileField(upload_to='static/documents/command', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderCommandFile',on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "(" + str(self.command.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'

class CommandURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderCommandURL', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description + ' (' + self.url + ')'
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'

class Research(models.Model):
    fiscalYear = models.IntegerField(default=0)
    title_th = models.TextField(default="")
    title_en = models.TextField(default="")
    objective = models.TextField(default="")
    budget = models.FloatField(default=0.00)
    budgetType = models.CharField(max_length=30, default="งบประมาณรายได้")
    source = models.CharField(max_length=255, default="")
    keyword = models.TextField(default="")
    percent_success = models.IntegerField(default=0)
    publish_method = models.TextField(default="")
    recorder = models.ForeignKey(Personnel, related_name='RecorderResearch', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add = True)
    editor = models.ForeignKey(Personnel, related_name='EditorResearch', on_delete=models.CASCADE, default=None)
    editDate = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.title_th + ' (' + str(self.fiscalYear) +  ") : " + str(self.budget)
    def getResearchPerson(self):
        personnels = ResearchPerson.objects.filter(research=self).order_by('personnel__firstname_th', 'personnel__lastname_th')
        return personnels
    def getCountPersonnel(self): #จำนวนคนที่อยู่ในงานวิจัย
        count = ResearchPerson.objects.filter(research=self).aggregate(count=Count('id'))
        return count['count']
    def getSumPercent(self):  # สัดส่วนการทำวิจัยรวมทุกคน
        sum = ResearchPerson.objects.filter(research=self).aggregate(sum=Sum('percent'))
        return sum['sum']
    def getResearchFiles(self):
        researchFiles = ResearchFile.objects.filter(research=self)
        return researchFiles
    def getResearchURLs(self):
        researchURLs = ResearchURL.objects.filter(research=self)
        return researchURLs
    @staticmethod
    def getCountPersonResearch(personnel):  # นับจำนวนครั้งที่บุคลากรรายหนึ่งทำเกี่ยวกับการวิจัย
        countResearch = Research.objects.filter(Q(recorder=personnel) or Q(editor=personnel)).count()
        countResearchPerson = ResearchPerson.objects.filter(Q(personnel=personnel) or Q(recorder=personnel)).count()
        countResearchFile = ResearchFile.objects.filter(recorder=personnel).count()
        countResearchURL = ResearchURL.objects.filter(recorder=personnel).count()
        countAll = countResearch + countResearchPerson + countResearchFile + countResearchURL
        return countAll
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        editor  = Personnel.objects.filter(id=self.editor.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        editDate = self.editDate.strftime('%d/%m/%Y %H:%M:%S')
        if recorder == editor and recordDate == editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate +')'
        elif recorder == editor and recordDate != editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' ('+ recordDate + \
                   '), แก้ไขเมื่อ:' + ' ('+ editDate +')'
        else:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + \
                   '), แก้ไขโดย:' + editor.firstname_th + ' ' + editor.lastname_th + ' ('+ editDate +')'

class ResearchPerson(models.Model):
    status = models.CharField(max_length=30, default="หัวหน้าโครงการ")
    percent= models.IntegerField(default=100)
    research = models.ForeignKey(Research, on_delete=models.CASCADE, default=None)
    personnel = models.ForeignKey(Personnel, related_name='PersonnelResearchPerson', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderResearchPerson', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.research.id + " : " + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " +  " (" + self.status + ")"
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'

class ResearchFile(models.Model):
    file = models.FileField(upload_to='static/documents/research', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    research = models.ForeignKey(Research, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderResearchFile', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "(" + str(self.research.id) + "_" + str(self.id) + ") filename: " + self.file.name +  ", filetype: "   + self.filetype
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'

class ResearchURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)
    research = models.ForeignKey(Research, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderResearchURL', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description + ' (' + self.url + ')'
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'


class SocialService(models.Model):
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    days = models.IntegerField(default=1)
    fiscalYear = models.IntegerField(default=0)
    eduYear = models.IntegerField(default=0)
    eduSemeter = models.IntegerField(default=0)
    topic = models.TextField(default="")
    objective = models.TextField(default="")
    place = models.CharField(max_length=255, default="")
    budget = models.FloatField(default=0.00)
    budgetType = models.CharField(max_length=30, default="งบประมาณรายได้")
    source = models.CharField(max_length=255, default="")
    receiver = models.CharField(max_length=255, default="")
    num_receiver = models.IntegerField(default=0)
    recorder = models.ForeignKey(Personnel, related_name='RecorderSocialService', on_delete=models.CASCADE,
                                 default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    editor = models.ForeignKey(Personnel, related_name='EditorSocialService', on_delete=models.CASCADE, default=None)
    editDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.recorder.status + self.recorder.firstName_th + " " + self.recorder.lastName_th + \
               "  " + self.topic + " : " + self.place + " : " + str(self.startDate) + "-" + str(self.endDate)
    def getSocialServicePerson(self):
        personnels = SocialServicePerson.objects.filter(socialservice=self).order_by('personnel__firstname_th', 'personnel__lastname_th')
        return personnels
    def getRecorder(self):
        return self.recorder.status + self.recorder.firstname_th + ' ' + self.recorder.lastname_th
    def getEduYearAndSementer(self):
        return self.eduYear + self.eduSemeter
    def getCountPersonnel(self): #จำนวนคนที่อยู่ในโครงการบริการวิชาการ
        count = SocialServicePerson.objects.filter(socialservice=self).aggregate(count=Count('id'))
        return count['count']
    def getSocialServiceFiles(self):
        socialserviceFiles = SocialServiceFile.objects.filter(socialservice=self)
        return socialserviceFiles
    def getSocialServiceURLs(self):
        socialserviceURLs = SocialServiceURL.objects.filter(socialservice=self)
        return socialserviceURLs
    @staticmethod
    def getCountPersonSocialService(personnel):  # นับจำนวนครั้งที่บุคลากรรายหนึ่งทำเกี่ยวกับการบริการทางวิชาการ
        countSocialService = SocialService.objects.filter(Q(recorder=personnel) or Q(editor=personnel)).count()
        countSocialServicePerson = SocialServicePerson.objects.filter(
            Q(personnel=personnel) or Q(recorder=personnel)).count()
        countSocialServiceFile = SocialServiceFile.objects.filter(recorder=personnel).count()
        countSocialServiceURL = SocialServiceURL.objects.filter(recorder=personnel).count()
        countAll = countSocialService + countSocialServicePerson + countSocialServiceFile + countSocialServiceURL
        return countAll
    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        editor = Personnel.objects.filter(id=self.editor.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        editDate = self.editDate.strftime('%d/%m/%Y %H:%M:%S')
        if recorder == editor and recordDate == editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'
        elif recorder == editor and recordDate != editDate:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + \
                   '), แก้ไขเมื่อ:' + ' (' + editDate + ')'
        else:
            return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + \
                   '), แก้ไขโดย:' + editor.firstname_th + ' ' + editor.lastname_th + ' (' + editDate + ')'


class SocialServicePerson(models.Model):
    status = models.CharField(max_length=30, default="")
    socialservice = models.ForeignKey(SocialService, on_delete=models.CASCADE, default=None)
    personnel = models.ForeignKey(Personnel, related_name='PersonnelSocialServicePerson', on_delete=models.CASCADE,
                                  default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderSocialServicePerson', on_delete=models.CASCADE,
                                 default=None)
    recordDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.socialservice.id + " : " + self.personnel.firstName_th + " " + self.personnel.lastName_th + \
               "  " + " (" + self.status + ")"

    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'


class SocialServiceFile(models.Model):
    file = models.FileField(upload_to='static/documents/socialservice', default=None, null=True, blank=True)
    filetype = models.CharField(max_length=50, default=None)
    socialservice = models.ForeignKey(SocialService, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderSocialServiceFile', on_delete=models.CASCADE,
                                 default=None)
    recordDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "(" + str(self.socialservice.id) + "_" + str(
            self.id) + ") filename: " + self.file.name + ", filetype: " + self.filetype

    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'


class SocialServiceURL(models.Model):
    url = models.URLField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)
    socialservice = models.ForeignKey(SocialService, on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderSocialServiceURL', on_delete=models.CASCADE,
                                 default=None)
    recordDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description + ' (' + self.url + ')'

    def getRecorderAndEditor(self):
        recorder = Personnel.objects.filter(id=self.recorder.id).first()
        recordDate = self.recordDate.strftime('%d/%m/%Y %H:%M:%S')
        return 'บันทึกโดย: ' + recorder.firstname_th + ' ' + recorder.lastname_th + ' (' + recordDate + ')'
