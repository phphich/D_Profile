from django import forms
from .models import *

class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ('name_th', 'name_en', 'name_sh')
        widgets = {
            'name_th': forms.TextInput(attrs={'class': 'form-control',  'size': 55, 'maxlength': 50}),
            'name_en': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'name_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 15, 'maxlength': 10}),
        }
        labels = {
            'name_th': 'ชื่อสาขา (ไทย)',
            'name_en': 'ชื่อสาขา (อังกฤษ)',
            'name_sh': 'ชื่อย่อ',
        }
    def deleteForm(self):
        self.fields['name_th'].widget.attrs['readonly'] = True
        self.fields['name_en'].widget.attrs['readonly'] = True
        self.fields['name_sh'].widget.attrs['readonly'] = True

class CurriculumForm(forms.ModelForm):
    class Meta:
        LEVEL_CHOICES = (
            ("ปวช.", "ปวช."),
            ("ปวส.", "ปวส."),
            ("ปริญญาตรี", "ปริญญาตรี"),
            ("ปริญญาโท", "ปริญญาโท"),
            ("ปริญญาเอก", "ปริญญาเอก"),
        )
        model = Curriculumn
        fields = ('name_th', 'name_en', 'name_th_sh', 'name_en_sh', 'level', 'studyTime', 'division')
        widgets = {
            'name_th': forms.TextInput(attrs={'class': 'form-control',  'size': 55, 'maxlength': 50}),
            'name_en': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'name_th_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 35}),
            'name_en_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 35}),
            'level': forms.Select(choices=LEVEL_CHOICES, attrs={'class': 'form-control'}),
            'studyTime': forms.IntegerField(attrs={'class': 'form-control', 'Min': 2}),
            'division':forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name_th': 'ชื่อปริญญา (ไทย)',
            'name_en': 'ชื่อปริญญา (อังกฤษ)',
            'name_th_sh': 'ชื่อย่อปริญญา (ไทย)',
            'name_en_sh': 'ชื่อย่อปริญญา (อังกฤษ)',
            'level': 'ระดับการศึกษา',
            'studyTime': 'ระยะเวลาของหลักสูตร',
            'division': 'สาขา',
        }


    def deleteForm(self):
        self.fields['name_th'].widget.attrs['readonly'] = True
        self.fields['name_en'].widget.attrs['readonly'] = True
        self.fields['name_th_sh'].widget.attrs['readonly'] = True
        self.fields['name_en_sh'].widget.attrs['readonly'] = True
        self.fields['level'].widget.attrs['readonly'] = True
        self.fields['studyTime'].widget.attrs['readonly'] = True
        self.fields['division'].widget.attrs['readonly'] = True


class PersonnelForm(forms.ModelForm):
    class Meta:
        GENDER_CHOICES = (
            ("ชาย", "ชาย"),
            ("หญิง", "หญิง"),
        )
        model = Personnel
        fields = ('email', 's_id', 'firstName', 'lastName', 'status', 'gender', 'address',
                  'birthDate', 'hiringDate', 'picture', 'division')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 30}),
            's_id': forms.TextInput(attrs={'class': 'form-control', 'size': 20, 'maxlength': 15}),
            'firstName': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'lastName': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'size': 20, 'maxlength': 15}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'gender': forms.Select(choices=GENDER_CHOICES, attrs={'class': 'form-control'}),
            'birthDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hiringDate': forms.NumberInput(attrs={'class': 'form-control', type: 'date'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'email': 'อีเมล์',
            's_id': 'เลขที่ตำแหน่ง',
            'firstName': 'ชื่อ',
            'lastName': 'สกุล',
            'status': 'ตำแหน่ง',
            'gender': 'เพศ',
            'address': 'ที่อยู่',
            'birthDate': 'วันเดือนปีเกิด',
            'hiringDate': 'วันเริ่มทำงาน',
            'picture': 'รูปภาพ',
            'division':'สาขา',
        }

    def deleteForm(self):
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['s_id'].widget.attrs['readonly'] = True
        self.fields['firstName'].widget.attrs['readonly'] = True
        self.fields['lastName'].widget.attrs['readonly'] = True
        self.fields['status'].widget.attrs['readonly'] = True
        self.fields['gender'].widget.attrs['readonly'] = True
        self.fields['address'].widget.attrs['readonly'] = True
        self.fields['birthDate'].widget.attrs['readonly'] = True
        self.fields['hiringDate'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True
        self.fields['division'].widget.attrs['readonly'] = True

class EducationForm(forms.ModelForm):
    class Meta:
        LEVEL_CHOICES = (
            ("ปวช.", "ปวช."),
            ("ปวส.", "ปวส."),
            ("ปริญญาตรี", "ปริญญาตรี"),
            ("ปริญญาโท", "ปริญญาโท"),
            ("ปริญญาเอก", "ปริญญาเอก"),
            ("ประกาศนียบัตร", "ประกาศนียบัตร"),
        )
        model = Education
        fields = ('level', 'degree_th', 'degree_en','degree_th_sh','degree_en_sh','yearGraduate','institute','personnel')
        widgets = {
            'level': forms.Select(choices=LEVEL_CHOICES, attrs={'class': 'form-control',  'size': 35}),
            'degree_th': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'degree_en': forms.TextInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 35}),
            'name_th_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 35}),
            'name_en_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 35}),
            'yearGraduate': forms.IntegerField(attrs={'class': 'form-control', 'size': 10, 'maxlength': 4}),
            'institute': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'personnel':forms.HiddenInput(),
        }
        labels = {
            'level': 'ระดับการศึกษา',
            'degree_th': 'ชื่อปริญญา (ไทย)',
            'degree_en': 'ชื่อปริญญา (อังกฤษ)',
            'degree_th_sh': 'ชื่อย่อปริญญา (ไทย)',
            'degree_en_sh': 'ชื่อย่อปริญญา (อังกฤษ)',
            'yearGraduate': 'ปีที่สำเร็จการศึกษา',
            'institute': 'จากสถาบันการศึกษา',
            'personnel': 'บุคลากร',
        }

    def deleteForm(self):
        self.fields['level'].widget.attrs['readonly'] = True
        self.fields['degree_th'].widget.attrs['readonly'] = True
        self.fields['degree_en'].widget.attrs['readonly'] = True
        self.fields['degree_th_sh'].widget.attrs['readonly'] = True
        self.fields['degree_en_sh'].widget.attrs['readonly'] = True
        self.fields['yearGraduate'].widget.attrs['readonly'] = True
        self.fields['institute'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True

class ExpertiseForm(forms.ModelForm):
    class Meta:
        model = Expertise
        fields = ('topic', 'detail', 'personnel')
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 120, 'maxlength': 100}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows':5}),
            'personnel':forms.HiddenInput(),
        }
        labels = {
            'topic': 'เรื่อง/ประเด็นที่เชี่ยวชาญ',
            'detail': 'รายละเอียด',
            'personnel': 'บุคลากร',
        }

    def deleteForm(self):
        self.fields['topic'].widget.attrs['readonly'] = True
        self.fields['detail'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True

class PersonCurriculumForm(forms.ModelForm):
    class Meta:
        STATUS_CHOICES = (
            ("ผู้รับผิดชอบหลักสูตร", "ผู้รับผิดชอบหลักสูตร"),
            ("กรรมการประจำหลักสูตร", "กรรมการประจำหลักสูตร"),
            ("อาจารย์ประจำหลักสูตร", "อาจารย์ประจำหลักสูตร"),
        )
        model = PersonCurriculum
        fields = (
            'status', 'personnel', 'curriculum')
        widgets = {
            'status': forms.Select(choices=LEVEL_CHOICES, attrs={'class': 'form-control', 'size': 55}),
            'personnel': forms.Select(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'curriculum': forms.HiddenInput(),
        }
        labels = {
            'status': 'ตำแหน่งในหลักสูตร',
            'personnel': 'บุคลากร',
            'curriculum': 'หลักสูตร',
        }

    def deleteForm(self):
        self.fields['status'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True
        self.fields['curriculum'].widget.attrs['readonly'] = True


