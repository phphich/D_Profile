from django.db import models
from django.utils import timezone

class Faculty(models.Model):
    name_th = models.CharField(max_length=100, default="")
    name_en = models.CharField(max_length=100, default="")
    university = models.CharField(max_length=100, default="")
    address = models.TextField(default="")
    telephone = models.CharField(max_length=20, default="")
    website = models.CharField(max_length=50, default="")
    vision = models.TextField(default="")
    slogan = models.CharField(max_length=128, default="")
    def __str__(self):
        return self.name_th + " " + self.university

class Division(models.Model):
    name_th = models.CharField(max_length=50, default="")
    name_en = models.CharField(max_length=50, default="")
    name_sh = models.CharField(max_length=10, default="")
    def __str__(self):
        return str(self.name_th) + " (" + self.name_sh + ")"

class Curriculumn(models.Model):
    name_th= models.CharField(max_length=100, default="")
    name_en = models.CharField(max_length=100, default="")
    name_th_sh = models.CharField(max_length=50, default="")
    name_en_sh = models.CharField(max_length=50, default="")
    level = models.CharField(max_length=30, default="")
    studyTime = models.IntegerField(default=4)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.name_th

class Personnel(models.Model):
    email = models.CharField(max_length=30, unique=True, default="")
    s_id = models.CharField(max_length=15, default="")
    firstName = models.CharField(max_length=50, default="")
    lastName = models.CharField(max_length=50, default="")
    status  = models.CharField(max_length=30, default="อาจารย์")
    gender = models.CharField(max_length=15, default="ชาย")
    address = models.TextField(default="")
    birthDate = models.DateField(default=None)
    hiringDate = models.DateField(default=None)
    picture = models.ImageField(upload_to ='static/images/personnels/', default=None)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.status + self.firstName +  " " + self.lastName

class Education(models.Model):
    level = models.CharField(max_length=30, default="")
    degree_th = models.CharField(max_length=100, default="")
    degree_en = models.CharField(max_length=100, default="")
    degree_th_sh = models.CharField(max_length=50, default="")
    degree_en_sh = models.CharField(max_length=50, default="")
    yearGraduate = models.IntegerField(default=0)
    institute = models.CharField(max_length=100, default="")
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName + " " + self.personnel.lastName +\
               " " + self.degree_th + " " + str(self.yearGraduate)

class Expertise(models.Model):
    topic = models.CharField(max_length=100, default=None)
    detail = models.TextField(default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.personnel.status + self.personnel.firstName + " " + self.personnel.lastName + \
               " - " + self.topic

class PersonCurriculum(models.Model):
    status = models.CharField(max_length=30, default="อาจารย์ประจำหลักสูตร")
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    curriculum = models.ForeignKey(Curriculumn, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.curriculum.name_th + "  (" + self.status + ")"

class Documents(models.Model):
    docType=models.CharField(max_length=15, default=None)
    refId=models.IntegerField(default=0)
    fileName = models.CharField(max_length=100, default=None)
    fileType = models.CharField(max_length=30, default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to='static/documents/', default=None)
