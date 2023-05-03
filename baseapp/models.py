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
    philosophy = models.CharField(max_length=128, default="")
    def __str__(self):
        return self.name_th + " " + self.university

class Division(models.Model):
    name_th = models.CharField(max_length=50, default="")
    name_en = models.CharField(max_length=50, default="")
    name_sh = models.CharField(max_length=10, default="")
    def __str__(self):
        return str(self.name_th) + " (" + self.name_sh + ")"

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

class Personnel(models.Model):
    email = models.CharField(max_length=30, unique=True, default="")
    sId = models.CharField(max_length=15, default="")
    firstname_th = models.CharField(max_length=50, default="")
    lastname_th = models.CharField(max_length=50, default="")
    firstname_en = models.CharField(max_length=50, default="")
    lastname_en = models.CharField(max_length=50, default="")
    status  = models.CharField(max_length=30, default="อาจารย์")
    type = models.CharField(max_length=10, default="")
    gender = models.CharField(max_length=15, default="ชาย")
    address = models.TextField(default="")
    birthDate = models.DateField(default=None)
    hiringDate = models.DateField(default=None)
    picture = models.ImageField(upload_to ='static/images/personnels/', default=None)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.status + self.firstname_th +  " " + self.lastname_th

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
        return self.personnel.status + self.personnel.firstname_th + " " + self.personnel.lastname_th +\
               " " + self.degree_th + " " + str(self.yearGraduate)

class Expertise(models.Model):
    topic = models.CharField(max_length=100, default=None)
    detail = models.TextField(default=None)
    experience = models.TextField(default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.personnel.status + self.personnel.firstname_th + " " + self.personnel.lastname_th + \
               " - " + self.topic

class CurrAffiliation(models.Model):
    status = models.CharField(max_length=30, default="อาจารย์ประจำหลักสูตร")
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.curriculum.name_th + "  (" + self.status + ")"

class Documents(models.Model):
    doctype=models.CharField(max_length=15, default=None)
    refId=models.IntegerField(default=0)
    filename = models.CharField(max_length=100, default=None)
    filetype = models.CharField(max_length=30, default=None)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to='static/documents/', default=None)
