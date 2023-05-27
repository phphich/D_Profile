from django.db import models
from django.utils import timezone
from django.db.models import F, Sum, Count

class Faculty(models.Model):
    name_th = models.CharField(max_length=100, default="")
    name_en = models.CharField(max_length=100, default="")
    university = models.CharField(max_length=100, default="")
    address = models.TextField(default="")
    telephone = models.CharField(max_length=20, default="")
    website = models.CharField(max_length=50, default="")
    vision = models.TextField(default="")
    philosophy = models.CharField(max_length=128, default="")
    def __str__(self):
        return self.name_th + " " + self.university

class Division(models.Model):
    name_th = models.CharField(max_length=50, default="")
    name_en = models.CharField(max_length=50, default="")
    name_sh = models.CharField(max_length=10, default="")
    def __str__(self):
        if self.name_sh  ==  "":
            return str(self.name_th)
        else:
            return str(self.name_th) + " (" + self.name_sh + ")"

    def getCurriculum(self):
        curriculums = Curriculum.objects.filter(division=self)
        return curriculums
    def getPersonnels(self):
        personnels = Personnel.objects.filter(division=self).order_by('firstname_th', 'lastname_th')
        return personnels
    def getCountPersonnel(self):
        count = Personnel.objects.filter(division=self).aggregate(count=Count('id'))
        return count['count']

class Curriculum(models.Model):
    name_th= models.CharField(max_length=100, default="")
    name_en = models.CharField(max_length=100, default="")
    name_th_sh = models.CharField(max_length=50, default="")
    name_en_sh = models.CharField(max_length=50, default="")
    level = models.CharField(max_length=30, default="")
    studyTime = models.IntegerField(default=4)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.name_th
    def getCurrAffiliation(self):
        currAffilaitions = CurrAffiliation.objects.filter(curriculum=self).order_by('status')
        return currAffilaitions

class Personnel(models.Model):
    email = models.CharField(max_length=30, unique=True, default="")
    sId = models.CharField(max_length=15, default="")
    firstname_th = models.CharField(max_length=50, default="")
    lastname_th = models.CharField(max_length=50, default="")
    firstname_en = models.CharField(max_length=50, default="")
    lastname_en = models.CharField(max_length=50, default="")
    status  = models.CharField(max_length=30, default="อาจารย์")
    type = models.CharField(max_length=30, default="สายวิชาการ")
    gender = models.CharField(max_length=15, default="ชาย")
    address = models.TextField(default="")
    birthDate = models.DateField(default=None)
    hiringDate = models.DateField(default=None)
    picture = models.ImageField(upload_to ='static/images/personnels/', default=None)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, default=None)
    class Meta:
        ordering = ['firstname_th', 'lastname_th', 'status',]
    def __str__(self):
        return self.status + self.firstname_th +  " " + self.lastname_th
    def getEducations(self):
        educations = Education.objects.filter(personnel=self).order_by('-yearGraduate')
        return educations
    def getExpertise(self):
        expertises = Expertise.objects.filter(personnel=self).order_by('id')
        return expertises
    def getCurrAffiliation(self):
        curraffiliations = CurrAffiliation.objects.filter(personnel=self).order_by('id')
        return curraffiliations

class Education(models.Model):
    level = models.CharField(max_length=30, default="")
    degree_th = models.CharField(max_length=100, default="")
    degree_en = models.CharField(max_length=100, default="")
    degree_th_sh = models.CharField(max_length=50, default="")
    degree_en_sh = models.CharField(max_length=50, default="")
    yearGraduate = models.IntegerField(default=0)
    institute = models.CharField(max_length=100, default="")
    personnel = models.ForeignKey(Personnel, related_name='PersonnelEducation', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderEducation', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstname_th + " " + self.personnel.lastname_th +\
               " " + self.degree_th + " " + str(self.yearGraduate)

class Expertise(models.Model):
    topic = models.CharField(max_length=100, default=None)
    detail = models.TextField(default=None)
    experience = models.TextField(default=None)
    personnel = models.ForeignKey(Personnel, related_name='PersonnelExpertise', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderExpertise', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.personnel.status + self.personnel.firstname_th + " " + self.personnel.lastname_th + \
               " - " + self.topic

class CurrAffiliation(models.Model):
    status = models.CharField(max_length=30, default="อาจารย์ประจำหลักสูตร")
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, default=None)
    personnel = models.ForeignKey(Personnel, related_name='PersonnelCurrAffiliation', on_delete=models.CASCADE, default=None)
    recorder = models.ForeignKey(Personnel, related_name='RecorderCurrAffiliation', on_delete=models.CASCADE, default=None)
    recordDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.curriculum.name_th + "  (" + self.status + ")"

class Documents(models.Model):
    doctype=models.CharField(max_length=15, default=None)
    refId=models.IntegerField(default=0)
    filename = models.CharField(max_length=100, default=None)
    filetype = models.CharField(max_length=30, default=None)
    uploadDate = models.DateTimeField(auto_now_add=True)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to='static/documents/', default=None)

class Permission(models.Model): # เจ้าหน้าที่รับผิดชอบจัดการข้อมูลสาขา
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.personnel.firstname_th + ' ' + self.personnel.lastname_th + ' => ' + self.division.name_th
