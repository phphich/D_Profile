from django import forms
from .models import *


# ฟอร์มการลา
class LeaveForm(forms.ModelForm):
    class Meta:
        TYPE_CHOICES = (
            ("ลาป่วย", "ลาป่วย"),
            ("ลากิจส่วนตัว", "ลากิจส่วนตัว"),
            ("ลาพักผ่อนประจำปี", "ลาพักผ่อนประจำปี"),
            ("ลาคลอดบุตร", "ลาคลอดบุตร"),
            ("ลาไปช่วยเหลือภริยาที่คลอดบุตร", "ลาไปช่วยเหลือภริยาที่คลอดบุตร"),
            ("ลาอุปสมบทหรือการลาไปประกอบพิธีฮัจย์", "ลาอุปสมบทหรือการลาไปประกอบพิธีฮัจย์"),
            ("ลาเข้ารับการตรวจเลือกหรือเข้ารับการเตรียมพล", "ลาเข้ารับการตรวจเลือกหรือเข้ารับการเตรียมพล"),
            ("ลาไปศึกษา/ฝึกอบรม/ปฏิบัติการวิจัย/ดูงาน", "ลาไปศึกษา/ฝึกอบรม/ปฏิบัติการวิจัย/ดูงาน"),
            ("ลาไปปฏิบัติงานในองค์กรระหว่างประเทศ", "ลาไปปฏิบัติงานในองค์กรระหว่างประเทศ")
        )
        EDITABLE_CHOICES = (
            (True, 'อนุญาตให้แก้ไขได้'),
            (False, 'ป้องกันการแก้ไข'),
        )
        model = Leave
        fields = (
            'fiscalYear', 'leaveType', 'startDate', 'endDate', 'days', 'reason', 'personnel',
            'editable', 'recorder', 'editor')
        widgets = {
            'startDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date',
                                                  'onchange': 'javascript:chkDateDiff();'}),
            'endDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date',
                                                'onchange': 'javascript:chkDateDiff();'}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1, 'max': 20,
                                             'onfocusout': 'javascript:chkDays();'}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'leaveType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'editable': forms.RadioSelect(choices=EDITABLE_CHOICES, attrs={'class': ''}),
            'personnel': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
            'editor': forms.HiddenInput(),
        }
        labels = {
            'fiscalYear': 'ปีงบประมาณ',
            'leaveType': 'ประเภทการลา',
            'startDate': 'วันที่เริ่มต้น',
            'endDate': 'วันที่สิ้นสุด',
            'days': 'จำนวนวันที่ลา',
            'reason': 'เหตุผลประกอบการลา',
            'personnel': 'บุคลากร',
            'editable': 'การแก้ไขโดยบุคลากร',
            'recorder': 'ผู้บันทึก',
            'editor': 'ผู้แก้ไข'
        }

    def updateForm(self):
        del self.fields['editable']

    def deleteForm(self):
        self.fields['startDate'].widget.attrs['readonly'] = True
        self.fields['endDate'].widget.attrs['readonly'] = True
        self.fields['days'].widget.attrs['readonly'] = True
        self.fields['fiscalYear'].widget.attrs['readonly'] = True
        self.fields['leaveType'].widget.attrs['readonly'] = True
        self.fields['reason'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True
        self.fields['recorder'].widget.attrs['readonly'] = True
        self.fields['editor'].widget.attrs['readonly'] = True


class LeaveFileForm(forms.ModelForm):
    class Meta:
        model = LeaveFile
        fields = ('file', 'filetype', 'leave','recorder')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'multiple': True,
                                           'accept': 'application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/pdf',
                                           'onchange': 'javascript:updateList();'}),
            'filetype': forms.HiddenInput(),
            'leave': forms.HiddenInput(),
            'recorder':forms.HiddenInput(),
        }
        labels = {
            'file': 'เลือกไฟล์เอกสารแนบ',
            'filetype': 'ชนิดไฟล์',
            'leave': 'ใบลา',
            'recorder': 'ผู้บันทึก',
        }

class LeaveURLForm(forms.ModelForm):
    class Meta:
        model = LeaveURL
        fields = ('url','description', 'leave', 'recorder')
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', }),
            'description': forms.TextInput(attrs={'class': 'form-control', }),
            'leave': forms.HiddenInput(),
            'recorder':forms.HiddenInput(),
        }
        labels = {
            'url': 'ลิงก์ตำแหน่งไฟล์เอกสาร',
            'description': 'คำอธิบายลิงก์ ',
            'leave': 'ใบลา',
            'recorder': 'ผู้บันทึก',
        }

# ฟอร์มการฝึกอบรม
class TrainignForm(forms.ModelForm):
    class Meta:
        SEMETER_CHOICES = (('1', '1'), ('2', '2'), ('3', 'ฤดูร้อน'))
        TYPE_CHOICES = (
            ('งบประมาณแผ่นดิน', 'งบประมาณแผ่นดิน'),
            ('งบประมาณรายได้', 'งบประมาณรายได้'),
            ('งบประมาณภายนอก', 'งบประมาณภายนอก'),
            ('งบประมาณส่วนตัว', 'งบประมาณส่วนตัว'),
            ('ไม่ใช้งบประมาณ', 'ไม่ใช้งบประมาณ')
        )
        model = Training
        fields = ('fiscalYear','topic', 'place',  'startDate', 'endDate', 'days', 'eduYear', 'eduSemeter', 'budget',
            'budgetType', 'personnel', 'recorder', 'editor')
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'startDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date',
                                                  'onchange': 'javascript:chkDateDiff();'}),
            'endDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date',
                                                'onchange': 'javascript:chkDateDiff();'}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1,
                                             'onfocusout': 'javascript:chkDays();'}),
            'eduYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduSemeter': forms.Select(choices=SEMETER_CHOICES, attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 0 }),
            'budgetType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control',
                                                                    'onchange': 'javascript:chkBudgetType();'}),
            'personnel': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
            'editor': forms.HiddenInput(),
        }
        labels = {
            'startDate': 'วันที่เริ่มต้น',
            'endDate': 'วันที่สิ้นสุด',
            'days': 'จำนวนวัน',
            'fiscalYear': 'ปีงบประมาณ',
            'eduYear': 'ปีการศึกษา',
            'eduSemeter': 'ภาคเรียนที่',
            'topic': 'หัวข้ออบรม/สัมมนา',
            'place': 'สถานที่/ผู้จัดโครงการ',
            'budget': 'งบประมาณที่ใช้',
            'budgetType': 'ประเภทงบประมาณ',
            'personnel': 'บุคลากร',
            'recorder': 'ผู้บันทึก',
            'editor': 'ผู้แก้ไข',
        }

    def deleteForm(self):
        self.fields['topic'].widget.attrs['readonly'] = True
        self.fields['place'].widget.attrs['readonly'] = True
        self.fields['fiscalYear'].widget.attrs['readonly'] = True
        self.fields['startDate'].widget.attrs['readonly'] = True
        self.fields['endDate'].widget.attrs['readonly'] = True
        self.fields['days'].widget.attrs['readonly'] = True
        self.fields['eduYear'].widget.attrs['readonly'] = True
        self.fields['eduSemeter'].widget.attrs['readonly'] = True
        self.fields['budget'].widget.attrs['readonly'] = True
        self.fields['budgetType'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True
        self.fields['recorder'].widget.attrs['readonly'] = True
        self.fields['editor'].widget.attrs['readonly'] = True


class TrainingFileForm(forms.ModelForm):
    class Meta:
        model = TrainingFile
        fields = ('file', 'filetype', 'training', 'recorder')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'multiple': True,
                                           'accept': 'application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/pdf',
                                           'onchange': 'javascript:updateList();'}),
            'filetype': forms.HiddenInput(),
            'training': forms.HiddenInput(),
            'recorder':forms.HiddenInput(),
        }
        labels = {
            'file': 'เลือกไฟล์เอกสารแนบ',
            'filetype': 'ชนิดไฟล์',
            'training': 'การฝึกอบรม/สัมมนา',
            'recorder': 'ผู้บันทึก',
        }


class TrainingURLForm(forms.ModelForm):
    class Meta:
        model = TrainingURL
        fields = ('url','description', 'training', 'recorder')
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', }),
            'description': forms.TextInput(attrs={'class': 'form-control', }),
            'training': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'url': 'ลิงก์ตำแหน่งไฟล์เอกสาร',
            'description': 'คำอธิบายลิงก์ ',
            'training': 'การฝึกอบรม/สัมมนา',
            'recorder': 'ผู้บันทึก',
        }

# ฟอร์มการผลงานรางวัล
class PerformanceForm(forms.ModelForm):
    class Meta:
        SEMETER_CHOICES = (('1', '1'), ('2', '2'), ('3', 'ฤดูร้อน'))
        TYPE_CHOICES = (
            ('งบประมาณแผ่นดิน', 'งบประมาณแผ่นดิน'),
            ('งบประมาณรายได้', 'งบประมาณรายได้'),
            ('งบประมาณภายนอก', 'งบประมาณภายนอก'),
            ('งบประมาณส่วนตัว', 'งบประมาณส่วนตัว'),
            ('ไม่ใช้งบประมาณ', 'ไม่ใช้งบประมาณ')
        )
        model = Performance
        fields = ('fiscalYear','topic', 'detail', 'source','getDate',  'eduYear', 'eduSemeter',  'budget', 'budgetType',
                  'personnel', 'recorder', 'editor')
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'getDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduSemeter': forms.Select(choices=SEMETER_CHOICES, attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 0}),
            'budgetType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control',
                                                                    'onchange': 'javascript:chkBudgetType();'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'personnel': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
            'editor': forms.HiddenInput(),
        }
        labels = {
            'getDate': 'วันที่ได้รางวัล/ผลงาน',
            'fiscalYear': 'ปีงบประมาณ',
            'eduYear': 'ปีการศึกษา',
            'eduSemeter': 'ภาคเรียนที่',
            'topic': 'ชื่อผลงาน/รางวัล',
            'detail': 'รายละเอียด',
            'budget': 'งบประมาณ',
            'budgetType': 'ประเภทงบประมาณ',
            'source': 'ได้รับจาก/ผู้มอบ',
            'personnel': 'บุคลากร',
            'recorder': 'ผู้บันทึก',
            'editor': 'ผู้แก้ไข',
        }

    def deleteForm(self):
        self.fields['getDate'].widget.attrs['readonly'] = True
        self.fields['fiscalYear'].widget.attrs['readonly'] = True
        self.fields['eduYear'].widget.attrs['readonly'] = True
        self.fields['eduSemeter'].widget.attrs['readonly'] = True
        self.fields['topic'].widget.attrs['readonly'] = True
        self.fields['detail'].widget.attrs['readonly'] = True
        self.fields['budget'].widget.attrs['readonly'] = True
        self.fields['budgetType'].widget.attrs['readonly'] = True
        self.fields['source'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True
        self.fields['recorder'].widget.attrs['readonly'] = True
        self.fields['editor'].widget.attrs['readonly'] = True

class PerformanceFileForm(forms.ModelForm):
    class Meta:
        model = PerformanceFile
        fields = ('file', 'filetype', 'performance','recorder')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'multiple': True,
                                           'accept': 'application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/pdf',
                                           'onchange': 'javascript:updateList();'}),
            'filetype': forms.HiddenInput(),
            'performance': forms.HiddenInput(),
            'recorder':forms.HiddenInput(),

        }
        labels = {
            'file': 'เลือกไฟล์เอกสารแนบ',
            'filetype': 'ชนิดไฟล์',
            'performance': 'การฝึกอบรม/สัมมนา',
            'recorder': 'ผู้บันทึก',
        }


class PerformanceURLForm(forms.ModelForm):
    class Meta:
        model = PerformanceURL
        fields = ('url','description', 'performance','recorder')
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', }),
            'description': forms.TextInput(attrs={'class': 'form-control', }),
            'performance': forms.HiddenInput(),
            'recorder':forms.HiddenInput(),
        }
        labels = {
            'url': 'ลิงก์ตำแหน่งไฟล์เอกสาร',
            'description': 'คำอธิบายลิงก์ ',
            'performance': 'การฝึกอบรม/สัมมนา',
            'recorder':'ผู้บันทึก',
        }

# +++++++++++++++
# ฟอร์มคำสั่ง
class CommandForm(forms.ModelForm):
    class Meta:
        MISSION_CHOICES = (
            ("การจัดการเรียนการสอน", "การจัดการเรียนการสอน"),
            ("การวิจัย", "การวิจัย"),
            ("การบริการทางวิชาการแก่สังคม", "การบริการทางวิชาการแก่สังคม"),
            ("การทำนุบำรุงศิลปวัฒนธรรม", "การทำนุบำรุงศิลปวัฒนธรรม"),
            ("สนองโครงการอันเนื่องมาจากพระราชดำริ", "สนองโครงการอันเนื่องมาจากพระราชดำริ"),
            ("งานอื่น ๆ ที่ได้รับมอบหมาย", "งานอื่น ๆ ที่ได้รับมอบหมาย"),
        )
        SEMETER_CHOICES = (('1', '1'), ('2', '2'), ('3', 'ฤดูร้อน'))
        model = Command
        fields = ( 'eduYear', 'eduSemeter','mission', 'comId', 'topic', 'detail','comDate',  'fiscalYear','recorder','editor')
        widgets = {
            'comId': forms.TextInput(attrs={'class': 'form-control', 'size': 20, 'maxlength': 15}),
            'comDate': forms.NumberInput(attrs={'class': 'form-control', 'type':'date'}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduSemeter': forms.Select(choices=SEMETER_CHOICES, attrs={'class': 'form-control'}),
            'mission': forms.Select(choices=MISSION_CHOICES, attrs={'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 255}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'recorder': forms.HiddenInput(),
            'editor': forms.HiddenInput(),
        }

        labels = {
            'eduYear': 'ปีการศึกษา',
            'eduSemeter': 'ภาคเรียนที่',
            'comId': 'เลขที่คำสั่ง',
            'comDate': 'วันที่ออกคำสั่่ง',
            'fiscalYear': 'ปีงบประมาณ',
            'mission': 'พันธกิจ',
            'topic': 'เรื่อง',
            'detail': 'รายละเอียด',
            'recorder': 'ผู้บันทึก',
            'editor' : 'ผู้แก้ไข',
        }

    def deleteForm(self):
        self.fields['comId'].widget.attrs['readonly'] = True
        self.fields['comDate'].widget.attrs['readonly'] = True
        self.fields['fiscalYear'].widget.attrs['readonly'] = True
        self.fields['eduYear'].widget.attrs['readonly'] = True
        self.fields['eduSemeter'].widget.attrs['readonly'] = True
        self.fields['mission'].widget.attrs['readonly'] = True
        self.fields['topic'].widget.attrs['readonly'] = True
        self.fields['detail'].widget.attrs['readonly'] = True
        self.fields['recorder'].widget.attrs['readonly'] = True
        self.fields['editor'].widget.attrs['readonly'] = True

class CommandFileForm(forms.ModelForm):
    class Meta:
        model = CommandFile
        fields = ('file', 'filetype', 'command','recorder')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'multiple': True,
                                           'accept': 'application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/pdf',
                                           'onchange': 'javascript:updateList();'}),
            'filetype': forms.HiddenInput(),
            'command': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'file': 'เลือกไฟล์เอกสารแนบ',
            'filetype': 'ชนิดไฟล์',
            'command': 'คำสั่ง',
            'recorder': 'ผู้บันทึก',
        }

class CommandURLForm(forms.ModelForm):
    class Meta:
        model = CommandURL
        fields = ('url','description', 'command', 'recorder')
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', }),
            'description': forms.TextInput(attrs={'class': 'form-control', }),
            'command': forms.HiddenInput(),
            'recorder':forms.HiddenInput(),
        }
        labels = {
            'url': 'ลิงก์ตำแหน่งไฟล์เอกสาร',
            'description': 'คำอธิบายลิงก์ ',
            'command': 'คำสั่ง',
            'recorder': 'ผู้บันทึก',
        }

class CommandPersonForm(forms.ModelForm):
    def __init__(self, command, division=None, staff=None,  *args, **kwargs):
        super(CommandPersonForm, self).__init__(*args, **kwargs)
        if staff==None:
            if(division != None): # หัวหน้าสาขา
                indivision = Personnel.objects.filter(division_id=division)
                personInDivisionInComm = CommandPerson.objects.filter(command=command, personnel__in=indivision)
                #ลูกน้องที่อยู่ในคำสั่งแล้ว
                personnels = []
                for person in indivision:
                    found=False
                    for incomm in personInDivisionInComm:
                        if person == incomm.personnel:
                            found=True
                            break
                    if found == False:
                        personnels.append(person.id)
                # self.fields['personnel'].queryset = Personnel.objects.filter(id__in=personnels)
            else: #Admin หรือ Personnel
                personnelsId = []
                compersonnels = CommandPerson.objects.filter(command=command).order_by('personnel__firstname_th',
                                                                                       'personnel__lastname_th')
                for commpersonnel in compersonnels:
                    personnelsId.append(commpersonnel.personnel.id)
                personnels = Personnel.objects.filter().exclude(id__in=personnelsId)
                # self.fields['personnel'].queryset = Personnel.objects.filter().exclude(id__in=personnelsId)
                # self.fields['personnel'].queryset = Personnel.objects.filter(id__in=personnels)
        else: # Staff
            personResponsibleAll = staff.getPersonnelResponsible()
            personResponsibles=[]
            foundStaff = False
            for person in personResponsibleAll:
                personResponsibles.append(person)
                if person==staff:
                    foundStaff = True
            if foundStaff == False:   # ถ้า Staff ไม่ได้อยู่ในกลุ่มที่รับผิดชอบ
                personResponsibles.append(staff)
            personInDivisionInComm = CommandPerson.objects.filter(command=command, personnel__in=personResponsibles)
            #คนที่รับผิดชอบและอยู่ในคำสั่งแล้ว
            personnels = []
            for person in personResponsibles:
                found = False
                for incomm in personInDivisionInComm:
                    if person == incomm.personnel:
                        found = True
                        break
                if found == False:
                    personnels.append(person.id)

        self.fields['personnel'].queryset = Personnel.objects.filter(id__in=personnels)
    class Meta:
        model = CommandPerson
        fields = ('status','command', 'personnel',  'recorder')
        widgets = {
            'command': forms.HiddenInput(),
            'personnel': forms.CheckboxSelectMultiple(attrs={'class': ''}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 30}),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'command': 'คำสั่ง',
            'personnel': 'บุคลากร',
            'status': 'หน้าที่ที่มอบหมาย',
            'recorder': 'ผู้บันทึก',
        }


# +++++++++++++++
# ฟอร์มการวิจัย
class ResearchForm(forms.ModelForm):
    class Meta:
        TYPE_CHOICES = (
            ('งบประมาณแผ่นดิน', 'งบประมาณแผ่นดิน'),
            ('งบประมาณรายได้', 'งบประมาณรายได้'),
            ('งบประมาณภายนอก', 'งบประมาณภายนอก'),
            ('งบประมาณส่วนตัว', 'งบประมาณส่วนตัว'),
            ('ไม่ใช้งบประมาณ', 'ไม่ใช้งบประมาณ')
        )
        DB_CHOICES = (
            ('บทความวิจัยหรือบทความวิชาการฯ สืบเนื่องจากการประชุมวิชาการระดับชาติ (0.2)',
             'บทความวิจัยหรือบทความวิชาการฯ สืบเนื่องจากการประชุมวิชาการระดับชาติ (0.2)'),
            ('บทความวิจัยหรือบทความวิชาการฯ สืบเนื่องจากการประชุมวิชาการระดับนานาชาติ หรือในวารสารทางวิชาการระดับชาติที่ไม่อยู่ในฐานข้อมูลตามประกาศ ก.พ.อ. (0.4)',
             'บทความวิจัยหรือบทความวิชาการฯ สืบเนื่องจากการประชุมวิชาการระดับนานาชาติ หรือในวารสารทางวิชาการระดับชาติที่ไม่อยู่ในฐานข้อมูลตามประกาศ ก.พ.อ. (0.4)'),
            ('ผลงานที่ได้รับการจดอนุสิทธิบัตร (0.4)',
             'ผลงานที่ได้รับการจดอนุสิทธิบัตร (0.4)'),
            ('บทความวิจัยหรือบทความวิชาการที่ตีพิมพ์ในวารสารวิชาการที่ปรากฏในฐานข้อมูล TCI-2 (0.6)',
             'บทความวิจัยหรือบทความวิชาการที่ตีพิมพ์ในวารสารวิชาการที่ปรากฏในฐานข้อมูล TCI-2 (0.6)'),
            ('บทความวิจัยหรือบทความวิชาการที่ตีพิมพ์ในวารสารวิชาการที่ปรากฏในฐานข้อมูล TCI-1 (0.8)',
             'บทความวิจัยหรือบทความวิชาการที่ตีพิมพ์ในวารสารวิชาการที่ปรากฏในฐานข้อมูล TCI-1 (0.8)'),
            ('บทความวิจัยหรือบทความวิชาการที่ตีพิมพ์ในวารสารวิชาการระดับนานาชาติ ที่ปรากฏในฐานข้อมูลระดับนานาชาติ (1.0)',
             'บทความวิจัยหรือบทความวิชาการที่ตีพิมพ์ในวารสารวิชาการระดับนานาชาติ ที่ปรากฏในฐานข้อมูลระดับนานาชาติ (1.0)'),
            ('ผลงานได้รับการจดสิทธิบัตร (1.0)',
             'ผลงานได้รับการจดสิทธิบัตร (1.0)'),
            ('ผลงานวิชาการรับใช้สังคมที่ได้รับการประเมินผ่านเกณฑ์การขอตําแหน่งทางวิชาการแล้ว (1.0)',
             'ผลงานวิชาการรับใช้สังคมที่ได้รับการประเมินผ่านเกณฑ์การขอตําแหน่งทางวิชาการแล้ว (1.0)'),
            ('ผลงานวิจัยที่หน่วยงานหรือองค์กรระดับชาติว่าจ้างให้ดําเนินการ (1.0)',
             'ผลงานวิจัยที่หน่วยงานหรือองค์กรระดับชาติว่าจ้างให้ดําเนินการ (1.0)'),
            ('ผลงานค้นพบพันธุ์พืช พันธุ์สัตว์ ที่ค้นพบใหม่และได้รับการจดทะเบียน (1.0)',
             'ผลงานค้นพบพันธุ์พืช พันธุ์สัตว์ ที่ค้นพบใหม่และได้รับการจดทะเบียน (1.0)'),
            ('ตําราหรือหนังสือที่ได้รับการประเมินผ่านเกณฑ์การขอตําแหน่งทางวิชาการแล้ว (1.0)',
             'ตําราหรือหนังสือที่ได้รับการประเมินผ่านเกณฑ์การขอตําแหน่งทางวิชาการแล้ว (1.0)'),
            ('ตําราหรือหนังสือที่ผ่านการพิจารณาตามหลักเกณฑ์การประเมินตําแหน่งทางวิชาการ (1.0)',
             'ตําราหรือหนังสือที่ผ่านการพิจารณาตามหลักเกณฑ์การประเมินตําแหน่งทางวิชาการ (1.0)'),
            ('งานสร้างสรรค์ที่มีการเผยแพร่สู่สาธารณะในลักษณะใดลักษณะหนึ่ง หรือผ่านสื่ออิเล็กทรอนิกส์ Online (0.2)',
             'งานสร้างสรรค์ที่มีการเผยแพร่สู่สาธารณะในลักษณะใดลักษณะหนึ่ง หรือผ่านสื่ออิเล็กทรอนิกส์ Online (0.2)'),
            ('งานสร้างสรรค์ที่ได้รับการเผยแพร่ในระดับสถาบัน (0.4)',
             'งานสร้างสรรค์ที่ได้รับการเผยแพร่ในระดับสถาบัน (0.4)'),
            ('งานสร้างสรรค์ที่ได้รับการเผยแพร่ในระดับชาติ (0.6)',
             'งานสร้างสรรค์ที่ได้รับการเผยแพร่ในระดับชาติ (0.6)'),
            ('งานสร้างสรรค์ที่ได้รับการเผยแพร่ในระดับความร่วมมือระหว่างประเทศ (0.8)',
             'งานสร้างสรรค์ที่ได้รับการเผยแพร่ในระดับความร่วมมือระหว่างประเทศ (0.8)'),
            ('งานสร้างสรรค์ที่ได้รับการเผยแพร่ในระดับภูมิภาคอาเซียน/นานาชาติ (1.0)',
             'งานสร้างสรรค์ที่ได้รับการเผยแพร่ในระดับภูมิภาคอาเซียน/นานาชาติ (1.0)'),
            ('N/A', 'N/A'),
            ('-', '-'),
        )
        model = Research
        fields = (
            'fiscalYear', 'title_th', 'title_en', 'objective', 'budget', 'budgetType', 'source',
             'percentSuccess', 'publishMethod', 'publishDate', 'publishDb', 'reference','recorder', 'editor', )
        widgets = {
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'title_th': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'title_en': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 0}),
            'budgetType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control',
                                                                    'onchange': 'javascript:chkBudgetType();'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'reference': forms.Textarea(attrs={'class': 'form-control', 'cols':55, 'rows':2}),
            'percentSuccess': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1, 'max': 100}),
            'publishMethod': forms.TextInput(attrs={'class': 'form-control', 'size': 255}),
            'publishDate': forms.NumberInput(attrs={'class': 'form-control', 'type':'date'}),
            'publishDb': forms.Select(choices=DB_CHOICES, attrs={'class': 'form-control'}),
            'recorder': forms.HiddenInput(),
            'editor': forms.HiddenInput(),
        }
        labels = {
            'fiscalYear': 'ปีงบประมาณ',
            'title_th': 'ชื่องานวิจัย (ไทย)',
            'title_en': 'ชื่องานวิจัย (อังกฤษ)',
            'objective': 'วัตถุประสงค์การวิจัย',
            'budget': 'ทุนวิจัย',
            'budgetType': 'ประเภทงบประมาณ',
            'source': 'หน่วยงานเจ้าของทุนวิจัย',
            'reference': 'อ้างอิง (Reference)',
            'percentSuccess': 'ร้อยละความก้าวหน้า (%)',
            'publishMethod': 'การเผยแพร่ผลการวิจัย',
            'publishDate': 'วันที่ตีพิมพ์เผยแพร่',
            'publishDb': 'ประเภทบทความวิจัยฯ',
            'recorder': 'ผู้บันทึก',
            'editor': 'ผู้แก้ไข'
        }

    def deleteForm(self):
        self.fields['fiscalYear'].widget.attrs['readonly'] = True
        self.fields['title_th'].widget.attrs['readonly'] = True
        self.fields['title_en'].widget.attrs['readonly'] = True
        self.fields['objective'].widget.attrs['readonly'] = True
        self.fields['budget'].widget.attrs['readonly'] = True
        self.fields['budgetType'].widget.attrs['readonly'] = True
        self.fields['source'].widget.attrs['readonly'] = True
        self.fields['reference'].widget.attrs['readonly'] = True
        self.fields['percentSuccess'].widget.attrs['readonly'] = True
        self.fields['publishMethod'].widget.attrs['readonly'] = True
        self.fields['publishDate'].widget.attrs['readonly'] = True
        self.fields['publishDb'].widget.attrs['readonly'] = True
        self.fields['recorder'].widget.attrs['readonly'] = True
        # self.fields[all].widget.attrs['class'] = 'form-control text-danger'

class ResearchFileForm(forms.ModelForm):
    class Meta:
        model = ResearchFile
        fields = ('file', 'filetype', 'research', 'recorder')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'multiple': True,
                                           'accept': 'application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/pdf',
                                           'onchange': 'javascript:updateList();'}),
            'filetype': forms.HiddenInput(),
            'research': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'file': 'เลือกไฟล์เอกสารแนบ',
            'filetype': 'ชนิดไฟล์',
            'research': 'งานวิจัย',
            'recorder': 'ผู้บันทึก',
        }


class ResearchURLForm(forms.ModelForm):
    class Meta:
        model = ResearchURL
        fields = ('url', 'description', 'research', 'recorder')
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', }),
            'description': forms.TextInput(attrs={'class': 'form-control', }),
            'research': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'url': 'ลิงก์ตำแหน่งไฟล์เอกสาร',
            'description': 'คำอธิบายลิงก์ ',
            'research': 'งานวิจัย',
            'recorder': 'ผู้บันทึก',
        }


class ResearchPersonForm(forms.ModelForm):
    def __init__(self, research, division=None, staff=None,  *args, **kwargs):
        super(ResearchPersonForm, self).__init__(*args, **kwargs)
        if staff==None:
            if(division != None): # หัวหน้าสาขา
                indivision = Personnel.objects.filter(division_id=division)
                personInDivisionInRes = ResearchPerson.objects.filter(research=research, personnel__in=indivision)
                #ลูกน้องที่ร่วมวิจัยอยู่แล้ว
                personnels = []
                for person in indivision:
                    found=False
                    for incomm in personInDivisionInRes:
                        if person == incomm.personnel:
                            found=True
                            break
                    if found == False:
                        personnels.append(person.id)
            else: #Admin หรือ Personnel
                personnelsId = []
                respersonnels = ResearchPerson.objects.filter(research=research).order_by('personnel__firstname_th',
                                                                                       'personnel__lastname_th')
                for respersonnel in respersonnels:
                    personnelsId.append(respersonnel.personnel.id)
                personnels = Personnel.objects.filter().exclude(id__in=personnelsId)
        else: # Staff
            personResponsibleAll = staff.getPersonnelResponsible()
            personResponsibles=[]
            foundStaff = False
            for person in personResponsibleAll:
                personResponsibles.append(person)
                if person==staff:
                    foundStaff = True
            if foundStaff == False:   # ถ้า Staff ไม่ได้อยู่ในกลุ่มที่รับผิดชอบ
                personResponsibles.append(staff)


            personInDivisionInRes = ResearchPerson.objects.filter(research=research, personnel__in=personResponsibles)
            #คนที่รับผิดชอบและอยู่ในวิจัยแล้ว
            personnels = []
            for person in personResponsibles:
                found = False
                for incomm in personInDivisionInRes:
                    if person == incomm.personnel:
                        found = True
                        break
                if found == False:
                    personnels.append(person.id)

        self.fields['personnel'].queryset = Personnel.objects.filter(id__in=personnels)
        
    class Meta:
        model = ResearchPerson
        fields = ('status', 'percent', 'research', 'personnel', 'recorder')
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 30}),
            'percent': forms.NumberInput(attrs={'class': 'form-control', 'size': 35}),
            'research': forms.HiddenInput(),
            'personnel': forms.CheckboxSelectMultiple(attrs={'class': ''}),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'status': 'หน้าที่/ตำแหน่งในงานวิจัย',
            'percent': 'สัดส่วนการดำเนินการวิจัย (%)',
            'personnel': 'บุคลากร',
            'research': 'งานวิจัย',
            'recorder': 'ผู้บันทึก',
        }


# ฟอร์มการบริการวิชาการแก่สังคม
class SocialServiceForm(forms.ModelForm):
    class Meta:
        SEMETER_CHOICES = ((1, '1'), (2, '2'), (3, 'ฤดูร้อน'))
        TYPE_CHOICES = (
            ('งบประมาณแผ่นดิน', 'งบประมาณแผ่นดิน'),
            ('งบประมาณรายได้', 'งบประมาณรายได้'),
            ('งบประมาณภายนอก', 'งบประมาณภายนอก'),
            ('งบประมาณส่วนตัว', 'งบประมาณส่วนตัว'),
            ('ไม่ใช้งบประมาณ', 'ไม่ใช้งบประมาณ')
        )
        model = SocialService
        fields = (
            'fiscalYear', 'eduYear', 'eduSemeter','topic', 'objective', 'place','receiver', 'num_receiver', 'startDate', 'endDate', 'days', 'budget',
            'budgetType', 'source', 'recorder','editor')
        widgets = {
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduSemeter': forms.Select(choices=SEMETER_CHOICES, attrs={'class': 'form-control'}),
            'startDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date',
                                                  'onchange': 'javascript:chkDateDiff();'}),
            'endDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date',
                                                'onchange': 'javascript:chkDateDiff();'}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1,
                                             'onfocusout': 'javascript:chkDays();'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 0}),
            'budgetType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control',
                                                                    'onchange': 'javascript:chkBudgetType();'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'receiver': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'num_receiver': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1}),
            'recorder': forms.HiddenInput(),
            'editor': forms.HiddenInput(),
        }
        labels = {
            'startDate': 'วันที่เริ่มต้น',
            'endDate': 'วันที่สิ้นสุด',
            'days': 'จำนวนวัน',
            'fiscalYear': 'ปีงบประมาณ',
            'eduYear': 'ปีการศึกษา',
            'eduSemeter': 'ภาคเรียนที่',
            'topic': 'เรื่อง',
            'objective': 'วัตถุประสงค์',
            'place': 'สถานที่ให้บริการ',
            'budget': 'งบประมาณ',
            'budgetType': 'ประเภทงบประมาณ',
            'source': 'หน่วยงานเจ้าของงบประมาณ',
            'receiver': 'กลุ่มผู้รับบริการ',
            'num_receiver': 'จำนวนผู้เข้าร่วมโครงการ',
            'recorder': 'ผู้บันทึก',
            'editor': 'ผู้แก้ไข',
        }

    def deleteForm(self):
        self.fields['startDate'].widget.attrs['readonly'] = True
        self.fields['endDate'].widget.attrs['readonly'] = True
        self.fields['days'].widget.attrs['readonly'] = True
        self.fields['fiscalYear'].widget.attrs['readonly'] = True
        self.fields['eduYear'].widget.attrs['readonly'] = True
        self.fields['eduSemeter'].widget.attrs['readonly'] = True
        self.fields['topic'].widget.attrs['readonly'] = True
        self.fields['objective'].widget.attrs['readonly'] = True
        self.fields['place'].widget.attrs['readonly'] = True
        self.fields['budget'].widget.attrs['readonly'] = True
        self.fields['budgetType'].widget.attrs['readonly'] = True
        self.fields['source'].widget.attrs['readonly'] = True
        self.fields['receiver'].widget.attrs['readonly'] = True
        self.fields['num_receiver'].widget.attrs['readonly'] = True
        self.fields['recorder'].widget.attrs['readonly'] = True
        self.fields['editor'].widget.attrs['readonly'] = True


class SocialServiceFileForm(forms.ModelForm):
    class Meta:
        model = SocialServiceFile
        fields = ('file', 'filetype', 'socialservice', 'recorder')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'multiple': True,
                                           'accept': 'application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/pdf',
                                           'onchange': 'javascript:updateList();'}),
            'filetype': forms.HiddenInput(),
            'socialservice': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'file': 'เลือกไฟล์เอกสารแนบ',
            'filetype': 'ชนิดไฟล์',
            'socialservice': 'งานบริการทางวิชาการแก่สังคม',
            'recorder': 'ผู้บันทึก',
        }


class SocialServiceURLForm(forms.ModelForm):
    class Meta:
        model = SocialServiceURL
        fields = ('url', 'description', 'socialservice', 'recorder')
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', }),
            'description': forms.TextInput(attrs={'class': 'form-control', }),
            'socialservice': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'url': 'ลิงก์ตำแหน่งไฟล์เอกสาร',
            'description': 'คำอธิบายลิงก์ ',
            'socialservice': 'งานบริการทางวิชาการแก่สังคม',
            'recorder': 'ผู้บันทึก',
        }


class SocialServicePersonForm(forms.ModelForm):
    def __init__(self, socialservice, division=None, staff=None,  *args, **kwargs):
        super(SocialServicePersonForm, self).__init__(*args, **kwargs)
        if staff==None:
            if(division != None): # หัวหน้าสาขา
                indivision = Personnel.objects.filter(division_id=division)
                personInDivisionInRes = SocialServicePerson.objects.filter(socialservice=socialservice, personnel__in=indivision)
                #ลูกน้องที่ร่วมบริการอยู่แล้ว
                personnels = []
                for person in indivision:
                    found=False
                    for incomm in personInDivisionInRes:
                        if person == incomm.personnel:
                            found=True
                            break
                    if found == False:
                        personnels.append(person.id)
            else: #Admin หรือ Personnel
                personnelsId = []
                respersonnels = SocialServicePerson.objects.filter(socialservice=socialservice).order_by('personnel__firstname_th',
                                                                                       'personnel__lastname_th')
                for respersonnel in respersonnels:
                    personnelsId.append(respersonnel.personnel.id)
                personnels = Personnel.objects.filter().exclude(id__in=personnelsId)
        else: # Staff
            personResponsibleAll = staff.getPersonnelResponsible()
            personResponsibles=[]
            foundStaff = False
            for person in personResponsibleAll:
                personResponsibles.append(person)
                if person==staff:
                    foundStaff = True
            if foundStaff == False:   # ถ้า Staff ไม่ได้อยู่ในกลุ่มที่รับผิดชอบ
                personResponsibles.append(staff)


            personInDivisionInRes = SocialServicePerson.objects.filter(socialservice=socialservice, personnel__in=personResponsibles)
            #คนที่รับผิดชอบและอยู่ในวิจัยแล้ว
            personnels = []
            for person in personResponsibles:
                found = False
                for incomm in personInDivisionInRes:
                    if person == incomm.personnel:
                        found = True
                        break
                if found == False:
                    personnels.append(person.id)
        self.fields['personnel'].queryset = Personnel.objects.filter(id__in=personnels)

    class Meta:
        model = SocialServicePerson
        fields = ('status', 'socialservice', 'personnel', 'recorder')
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-control', 'size': 35, 'maxlength': 30}),
            'socialservice': forms.HiddenInput(),
            'personnel': forms.CheckboxSelectMultiple(attrs={'class': ''}),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'socialservice': 'งานบริการทางวิชาการแก่สังคม',
            'personnel': 'บุคลากร',
            'status': 'หน้าที่ในโครงการ',
            'percent': 'สัดส่วนการดำเนินการวิจัย (%)',
            'recorder': 'ผู้บันทึก',
        }

# +++++++++++++++
