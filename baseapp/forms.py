from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ('name_th', 'name_en', 'university', 'address', 'telephone', 'website', 'vision', 'philosophy')
        widgets = {
            'name_th': forms.TextInput(attrs={'class': 'form-control',  'size': 110, 'maxlength': 100}),
            'name_en': forms.TextInput(attrs={'class': 'form-control', 'size': 110, 'maxlength': 100}),
            'university': forms.TextInput(attrs={'class': 'form-control', 'size': 110, 'maxlength': 100}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'size': 25, 'maxlength': 20}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'size': 110, 'maxlength': 100}),
            'vision': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'philosophy': forms.TextInput(attrs={'class': 'form-control', 'size': 110, 'maxlength': 100}),
        }
        labels = {
            'name_th': 'ชื่อคณะ (ไทย)',
            'name_en': 'ชื่อคณะ (อังกฤษ)',
            'university' : 'ชื่อมหาวิทยาลัย',
            'address': 'ที่อยู่',
            'telephone': 'เบอร์โทรศัพท์',
            'website': 'เว็บไซต์คณะ',
            'vision': 'วิสัยทัศน์',
            'philosophy': 'ปรัชญา',

        }
    def deleteForm(self):
        self.fields['name_th'].widget.attrs['readonly'] = True
        self.fields['name_en'].widget.attrs['readonly'] = True
        self.fields['name_sh'].widget.attrs['readonly'] = True
        self.fields['university'].widget.attrs['readonly'] = True
        self.fields['address'].widget.attrs['readonly'] = True
        self.fields['telephone'].widget.attrs['readonly'] = True
        self.fields['website'].widget.attrs['readonly'] = True
        self.fields['vision'].widget.attrs['readonly'] = True
        self.fields['philosophy'].widget.attrs['readonly'] = True

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
            'name_th': 'ชื่อสาขา/หน่วยงานย่อย (ไทย)',
            'name_en': 'ชื่อสาขา/หน่วยงานย่อย (อังกฤษ)',
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
        model = Curriculum
        fields = ('name_th', 'name_en', 'curriculumYear','name_th_sh', 'name_en_sh', 'level', 'studyTime', 'division')
        widgets = {
            'name_th': forms.TextInput(attrs={'class': 'form-control',  'size': 110, 'maxlength': 100}),
            'name_en': forms.TextInput(attrs={'class': 'form-control', 'size': 110, 'maxlength': 100}),
            'curriculumYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 55}),
            'name_th_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'name_en_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'level': forms.Select(choices=LEVEL_CHOICES, attrs={'class': 'form-control'}),
            'studyTime': forms.NumberInput(attrs={'class': 'form-control', 'Min': 1}),
            'division':forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name_th': 'ชื่อปริญญา (ไทย)',
            'name_en': 'ชื่อปริญญา (อังกฤษ)',
            'curriculumYear': 'ปี พ.ศ.',
            'name_th_sh': 'ชื่อย่อปริญญา (ไทย)',
            'name_en_sh': 'ชื่อย่อปริญญา (อังกฤษ)',
            'level': 'ระดับการศึกษา',
            'studyTime': 'ระยะเวลาของหลักสูตร',
            'division': 'หน่วยงานที่รับผิดชอบ',
        }


    def deleteForm(self):
        self.fields['name_th'].widget.attrs['readonly'] = True
        self.fields['name_en'].widget.attrs['readonly'] = True
        self.fields['curriculumYear'].widget.attrs['readonly'] = True
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
        STATUS_CHOICES = (
            ("อาจารย์", "อาจารย์"),
            ("ผู้ช่วยศาสตราจารย์", "ผู้ช่วยศาสตราจารย์"),
            ("รองศาสตราจารย์", "รองศาสตราจารย์"),
            ("ศาสตราจารย์", "ศาสตราจารย์"),
            ("นาย", "นาย"),
            ("นาง", "นาง"),
            ("นางสาว", "นางสาว"),

        )
        TYPE_CHOICES = (
            ('สายวิชาการ', 'สายวิชาการ'),
            ('สายสนับสนุน', 'สายสนับสนุน'),
        )

        model = Personnel
        fields = ('id', 'sId', 'firstname_th', 'lastname_th', 'firstname_en', 'lastname_en', 'status', 'type', 'gender', 'address',
                  'birthDate', 'hiringDate', 'division', 'picture', 'email')
        widgets = {
            'id': forms.HiddenInput(),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 30}),
            'sId': forms.TextInput(attrs={'class': 'form-control', 'size': 20, 'maxlength': 15}),
            'firstname_th': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'lastname_th': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'firstname_en': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'lastname_en': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'status': forms.Select(choices=STATUS_CHOICES, attrs={'class': 'form-control'}),
            'type': forms.RadioSelect(choices=TYPE_CHOICES, attrs={'class': ''}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'gender': forms.RadioSelect(choices=GENDER_CHOICES, attrs={'class': ''}),
            'birthDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hiringDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'email': 'อีเมล์',
            'sId': 'เลขที่ตำแหน่ง',
            'firstname_th': 'ชื่อ (ไทย)',
            'lastname_th': 'สกุล (ไทย)',
            'firstname_en': 'ชื่อ (อังกฤษ)',
            'lastname_en': 'สกุล (อังกฤษ)',
            'status': 'ตำแหน่ง',
            'type': 'ประเภท',
            'gender': 'เพศ',
            'address': 'ที่อยู่',
            'birthDate': 'วันเดือนปีเกิด',
            'hiringDate': 'วันที่เริ่มบรรจุเข้าทำงาน',
            'picture': 'รูปภาพ',
            'division':'สังกัดสาขา',
        }

    def updateForm(self):
        self.fields['email'].widget.attrs['readonly'] = False

    def deleteForm(self):
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['sId'].widget.attrs['readonly'] = True
        self.fields['firstname_th'].widget.attrs['readonly'] = True
        self.fields['lastname_th'].widget.attrs['readonly'] = True
        self.fields['firstname_en'].widget.attrs['readonly'] = True
        self.fields['lastname_en'].widget.attrs['readonly'] = True
        self.fields['status'].widget.attrs['readonly'] = True
        self.fields['type'].widget.attrs['readonly'] = True
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
        fields = ('level', 'degree_th', 'degree_en','degree_th_sh','degree_en_sh','institute','yearGraduate', 'personnel', 'recorder')
        widgets = {
            'level': forms.Select(choices=LEVEL_CHOICES, attrs={'class': 'form-control'}),
            'degree_th': forms.TextInput(attrs={'class': 'form-control', 'size': 110, 'maxlength': 100}),
            'degree_en': forms.TextInput(attrs={'class': 'form-control', 'size': 110, 'maxlength': 100}),
            'degree_th_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'degree_en_sh': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'institute': forms.TextInput(attrs={'class': 'form-control', 'size': 110, 'maxlength': 100}),
            'yearGraduate': forms.NumberInput(attrs={'class': 'form-control', 'size': 20}),
            'personnel':forms.HiddenInput(),
            'recorder':forms.HiddenInput(),
        }
        labels = {
            'level': 'ระดับการศึกษา',
            'degree_th': 'ชื่อวุฒิการศึกษา (ไทย)',
            'degree_en': 'ชื่อวุฒิการศึกษา (อังกฤษ)',
            'degree_th_sh': 'ชื่อย่อวุฒิการศึกษา (ไทย)',
            'degree_en_sh': 'ชื่อย่อวุฒิการศึกษา (อังกฤษ)',
            'institute': 'ชื่อสถาบันการศึกษา',
            'yearGraduate': 'ปีที่สำเร็จการศึกษา',
            'personnel': 'บุคลากร',
            'recorder': 'ผู้บันทึก',

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
        fields = ('topic', 'detail','experience', 'personnel', 'recorder')
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 120, 'maxlength': 100}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows':5}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'personnel': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'topic': 'เรื่อง/ประเด็นที่เชี่ยวชาญ',
            'detail': 'รายละเอียด',
            'experience': 'ประสบการณ์/ผลงาน',
            'personnel': 'บุคลากร',
            'recorder': 'ผู้บันทึก',
        }

    def deleteForm(self):
        self.fields['topic'].widget.attrs['readonly'] = True
        self.fields['detail'].widget.attrs['readonly'] = True
        self.fields['experience'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True

class CurrAffiliationForm(forms.ModelForm):
    class Meta:
        STATUS_CHOICES = (
            ("ผู้รับผิดชอบหลักสูตร", "ผู้รับผิดชอบหลักสูตร"),
            ("กรรมการประจำหลักสูตร", "กรรมการประจำหลักสูตร"),
            ("อาจารย์ประจำหลักสูตร", "อาจารย์ประจำหลักสูตร"),
        )
        model = CurrAffiliation
        fields = (
            'curriculum', 'personnel', 'status', 'recorder')
        widgets = {
            'curriculum': forms.HiddenInput(attrs={'class': 'form-control text-primary', 'readonly':'readonly'}),
            'personnel': forms.Select(attrs={'class': 'form-control text-primary'}),
            'status': forms.Select(choices=STATUS_CHOICES, attrs={'class': 'form-control text-primary'}),
            'recorder': forms.HiddenInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
        }
        labels = {
            'curriculum': 'หลักสูตร',
            'personnel': 'บุคลากร',
            'status': 'ตำแหน่งในหลักสูตร',
            'recorder': 'ผู้บันทึก',
        }

    def deleteForm(self):
        self.fields['curriculum'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True
        self.fields['status'].widget.attrs['readonly'] = True

class AuthenForm(forms.Form):
    userName = forms.CharField(label='ชื่อบัญชีผู้ใช้ระบบ (User Name) ', max_length=50,
                             widget=forms.TextInput(attrs={'class':'form-control'}))
    userPass = forms.CharField(label='รหัสผ่าน (Password) ', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))

class ChgPasswordForm(forms.Form):
    email = forms.CharField(label='ชื่อบัญชีผู้ใช้ระบบ (User Name)', max_length=50,
                             widget=forms.TextInput(attrs={'class':'form-control', 'readonly':True}))
    currentPassword = forms.CharField(label='รหัสผ่านเดิม', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    newPassword = forms.CharField(label='รหัสผ่านใหม่', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(label='ยืนยันรหัสผ่านใหม่',  max_length=100,
                                      widget=forms.PasswordInput(attrs={'class':'form-control'}))

class ResetPasswordForm(forms.Form):
    userId = forms.CharField(label='ชื่อบัญชีผู้ใช้ระบบ (User Name)', max_length=50,
                             widget=forms.TextInput(attrs={'class':'form-control', 'readonly':True}))
    newPassword = forms.CharField(label='รหัสผ่านใหม่', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(label='ยืนยันรหัสผ่านใหม่',  max_length=100,
                                      widget=forms.PasswordInput(attrs={'class':'form-control'}))
