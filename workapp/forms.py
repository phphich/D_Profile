from django import forms
from .models import *


class CommandForm(forms.ModelForm):
    class Meta:
        MISSION_CHOICES = (
            ("การจัดการเรียนการสอน", "การจัดการเรียนการสอน"),
            ("การวิจัย", "การวิจัย"),
            ("บริการทางวิชาการแก่สังคม", "บริการทางวิชาการแก่สังคม"),
            ("ทำนุบำรุงศิลปวัฒนธรรม", "การทำนุบำรุงศิลปวัฒนธรรม"),
            ("สนองโครงการอันเนื่องมาจากพระราชดำริ", "สนองโครงการอันเนื่องมาจากพระราชดำริ"),
        )
        SEMETER_CHOICES = (('1', '1'), ('2', '2'), ('ฤดูร้อน', 'ฤดูร้อน'))
        model = Command
        fields = ('comId', 'comDate', 'fiscalYear', 'eduYear', 'eduSemeter', 'mission', 'topic', 'detail', 'personnel')
        widgets = {
            'comId': forms.TextInput(attrs={'class': 'form-control', 'size': 20, 'maxlength': 15}),
            'comDate': forms.TextInput(attrs={'class': 'form-control'}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduSemeter': forms.RadioSelect(choices=SEMETER_CHOICES, attrs={'class': ''}),
            'mission': forms.Select(choices=MISSION_CHOICES, attrs={'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 255}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'personnel': forms.HiddenInput(),
        }

        labels = {
            'comId': 'เลขที่คำสั่ง',
            'comDate': 'วันที่ออกคำสั่ง',
            'fiscalYear': 'ปีงบประมาณ',
            'eduYear': 'ปีการศึกษา',
            'eduSemeter': 'ภาคเรียนที่',
            'mission': 'พันธะกิจ',
            'topic': 'เรื่อง',
            'detail': 'รายละเอียด',
            'personnel': 'บุคลากร'
        }

        def deleteForm(self):
            self.fields['commandId'].widget.attrs['readonly'] = True
            self.fields['commandDate'].widget.attrs['readonly'] = True
            self.fields['fiscalYear'].widget.attrs['readonly'] = True
            self.fields['eduYear'].widget.attrs['readonly'] = True
            self.fields['eduSemeter'].widget.attrs['readonly'] = True
            self.fields['mission'].widget.attrs['readonly'] = True
            self.fields['topic'].widget.attrs['readonly'] = True
            self.fields['detail'].widget.attrs['readonly'] = True
            self.fields['personnel'].widget.attrs['readonly'] = True


class LeaveForm(forms.ModelForm):
    class Meta:
        TYPE_CHOICES = (
            ("ลาป่วย", "ลาป่วย"),
            ("ลากิจส่วนตัว", "ลากิจส่วนตัว"),
            ("ลาพักผ่อนประจำปี", "ลาพักผ่อนประจำปี"),
            ("ลาคลอดบุตร", "ลาคลอดบุตร"),
            ("ไปช่วยเหลือภริยาที่คลอดบุตร", "ไปช่วยเหลือภริยาที่คลอดบุตร"),
            ("ลาอุปสมบทหรือการลาไปประกอบพิธีฮัจย์", "ลาอุปสมบทหรือการลาไปประกอบพิธีฮัจย์"),
            ("ลาเข้ารับการตรวจเลือกหรือเข้ารับการเตรียมพล", "ลาเข้ารับการตรวจเลือกหรือเข้ารับการเตรียมพล"),
            ("การลาไปศึกษา/ฝึกอบรม/ปฏิบัติการวิจัย/ดูงาน", "การลาไปศึกษา/ฝึกอบรม/ปฏิบัติการวิจัย/ดูงาน"),
            ("ลาไปปฏิบัติงานในองค์กรระหว่างประเทศ", "ลาไปปฏิบัติงานในองค์กรระหว่างประเทศ")
        )
        model = Leave
        fields = (
            'fiscalYear', 'eduYear', 'leaveType', 'startDate', 'endDate', 'days', 'reason', 'personnel',
            'recorder')
        widgets = {
            'startDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1, 'max': 20}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'leaveType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'personnel': forms.HiddenInput(),
            'recorder': forms.HiddenInput(),
        }
        labels = {
            'fiscalYear': 'ปีงบประมาณ',
            'eduYear': 'ปีการศึกษา',
            'leaveType': 'ประเภทการลา',
            'startDate': 'วันที่เริ่มต้น',
            'endDate': 'วันที่สิ้นสุด',
            'days': 'จำนวนวันที่ลา',
            'reason': 'เหตุผลประกอบการลา',
            'personnel': 'บุคลากร',
            'recorder': 'ผู้บันทึก'
        }

    def deleteForm(self):
        self.fields['startDate'].widget.attrs['readonly'] = True
        self.fields['endDate'].widget.attrs['readonly'] = True
        self.fields['days'].widget.attrs['readonly'] = True
        self.fields['fiscalYear'].widget.attrs['readonly'] = True
        self.fields['eduYear'].widget.attrs['readonly'] = True
        self.fields['leaveType'].widget.attrs['readonly'] = True
        self.fields['reason'].widget.attrs['readonly'] = True
        self.fields['personnel'].widget.attrs['readonly'] = True


class LeaveFileForm(forms.ModelForm):
    class Meta:
        model = LeaveFile
        fields = ('file', 'filetype', 'leave')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'multiple': True,
                                           'accept': 'application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/pdf',
                                           'onchange': 'javascript:updateList();'}),
            'filetype': forms.HiddenInput(),
            'leave': forms.HiddenInput(),
        }
        labels = {
            'file': 'เลือกไฟล์เอกสารแนบ',
            'filetype': 'ชนิดไฟล์',
            'leave': 'ใบลา',
        }
class LeaveURLForm(forms.ModelForm):
    class Meta:
        model = LeaveURL
        fields = ('url', 'leave')
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control',}),
            'leave': forms.HiddenInput(),
        }
        labels = {
            'url': 'ลิงก์ตำแหน่งไฟล์เอกสาร',
            'leave': 'ใบลา',
        }

class TrainignForm(forms.ModelForm):
    class Meta:
        SEMETER_CHOICES = (('1', '1'), ('2', '2'), ('ฤดูร้อน', 'ฤดูร้อน'))
        TYPE_CHOICES = (
            ('งบประมาณแผ่นดิน', 'งบประมาณแผ่นดิน'),
            ('งบประมาณรายได้', 'งบประมาณรายได้'),
            ('งบประมาณส่วนตัว', 'งบประมาณส่วนตัว'),
            ('ไม่ใช้งบประมาณ', 'ไม่ใช้งบประมาณ')
        )
        model = Training
        fields = (
            'startDate', 'endDate', 'days', 'fiscalYear', 'eduYear', 'eduSemeter', 'topic', 'place', 'budget',
            'budgetType',
            'personnel')
        widgets = {
            'startDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduSemeter': forms.Select(choices=SEMETER_CHOICES, attrs={'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1}),
            'budgetType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}),
            'personnel': forms.HiddenInput(),
        }
        labels = {
            'startDate': 'วันที่เริ่มต้น',
            'endDate': 'วันที่สิ้นสุด',
            'days': 'จำนวนวันที่ลา',
            'fiscalYear': 'ปีงบประมาณ',
            'eduYear': 'ปีการศึกษา',
            'eduSemeter': 'ภาคเรียนที่',
            'topic': 'หัวข้ออบรม/ดูงาน',
            'place': 'สถานที่ฝึกอบรม/ดูงาน',
            'budget': 'งบประมาณ',
            'budgetType': 'ประเภทงบประมาณ',
            'personnel': 'บุคลากร'
        }

        def deleteForm(self):
            self.fields['startDate'].widget.attrs['readonly'] = True
            self.fields['endDate'].widget.attrs['readonly'] = True
            self.fields['days'].widget.attrs['readonly'] = True
            self.fields['fiscalYear'].widget.attrs['readonly'] = True
            self.fields['eduYear'].widget.attrs['readonly'] = True
            self.fields['eduSemeter'].widget.attrs['readonly'] = True
            self.fields['topic'].widget.attrs['readonly'] = True
            self.fields['place'].widget.attrs['readonly'] = True
            self.fields['budget'].widget.attrs['readonly'] = True
            self.fields['budgetType'].widget.attrs['readonly'] = True
            self.fields['personnel'].widget.attrs['readonly'] = True


class ResearchForm(forms.ModelForm):
    class Meta:
        TYPE_CHOICES = (
            ('งบประมาณแผ่นดิน', 'งบประมาณแผ่นดิน'),
            ('งบประมาณรายได้', 'งบประมาณรายได้'),
            ('งบประมาณส่วนตัว', 'งบประมาณส่วนตัว'),
            ('ไม่ใช้งบประมาณ', 'ไม่ใช้งบประมาณ')
        )
        model = Research
        fields = (
            'fiscalYear', 'title_th', 'title_en', 'objective', 'percent_resp', 'budget', 'budgetType', 'source',
            'keyword',
            'percent_success', 'publish_method', 'personnel')
        widgets = {
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'title_th': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'title_en': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 3}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'percent_resp': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1, 'max': 100}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1}),
            'budgetType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'keyword': forms.TextInput(attrs={'class': 'form-control', 'size': 255}),
            'percent_success': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1, 'max': 100}),
            'keyword': forms.TextInput(attrs={'class': 'form-control', 'size': 255}),
            'personnel': forms.HiddenInput(),
        }
        labels = {
            'fiscalYear': 'ปีงบประมาณ',
            'title_th': 'หัวข้อวิจัย (ไทย)',
            'title_en': 'หัวข้อวิจัย (อังกฤษ)',
            'objective': 'วัตถุประสงค์',
            'percent_resp': 'สัดส่วนความรับผิดชอบ (%)',
            'budget': 'งบประมาณ',
            'budgetType': 'ประเภทงบประมาณ',
            'source': 'หน่วยงานเจ้าของงบประมาณ',
            'keyword': 'คำสำคัญ',
            'percent_success': 'สัดส่วนความก้าวหน้า (%)',
            'publish_method': 'วิธีการเผยแพร่ผลงาน',
            'personnel': 'บุคลากร'
        }

        def deleteForm(self):
            self.fields['fiscalYear'].widget.attrs['readonly'] = True
            self.fields['topic_th'].widget.attrs['readonly'] = True
            self.fields['topic_en'].widget.attrs['readonly'] = True
            self.fields['objective'].widget.attrs['readonly'] = True
            self.fields['percen_resp'].widget.attrs['readonly'] = True
            self.fields['budget'].widget.attrs['readonly'] = True
            self.fields['budgetType'].widget.attrs['readonly'] = True
            self.fields['source'].widget.attrs['readonly'] = True
            self.fields['keyword'].widget.attrs['readonly'] = True
            self.fields['percent_success'].widget.attrs['readonly'] = True
            self.fields['publish_method'].widget.attrs['readonly'] = True
            self.fields['personnel'].widget.attrs['readonly'] = True


class SocialServiceForm(forms.ModelForm):
    class Meta:
        SEMETER_CHOICES = (('1', '1'), ('2', '2'), ('ฤดูร้อน', 'ฤดูร้อน'))
        TYPE_CHOICES = (
            ('งบประมาณแผ่นดิน', 'งบประมาณแผ่นดิน'),
            ('งบประมาณรายได้', 'งบประมาณรายได้'),
            ('งบประมาณส่วนตัว', 'งบประมาณส่วนตัว'),
            ('ไม่ใช้งบประมาณ', 'ไม่ใช้งบประมาณ')
        )
        model = SocialService
        fields = (
            'startDate', 'endDate', 'days', 'fiscalYear', 'eduYear', 'eduSemeter', 'topic', 'place', 'budget',
            'budgetType',
            'source', 'receiver', 'num_receiver', 'personnel')
        widgets = {
            'startDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'edulYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduSemeter': forms.RadioSelect(choices=SEMETER_CHOICES, attrs={'class': ''}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1}),
            'budgetType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'receiver': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'num_receiver': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1}),
            'personnel': forms.HiddenInput(),
        }
        labels = {
            'startDate': 'วันที่เริ่มต้น',
            'endDate': 'วันที่สิ้นสุด',
            'days': 'จำนวนวันที่ลา',
            'fiscalYear': 'ปีงบประมาณ',
            'eduYear': 'ปีการศึกษา',
            'eduSemeter': 'ภาคเรียนที่',
            'topic': 'เรื่อง',
            'objective': 'วัตถุประสงค์',
            'place': 'สถานที่ให้บริการ',
            'budget': 'งบประมาณ',
            'budgetType': 'ประเภทงบประมาณ',
            'source': 'หน่วยงานเจ้าของงบประมาณ',
            'receiver': 'กลุ่มเป้าหมาย',
            'num_receiver': 'จำนวนผู้เข้าร่วมโครงการ',
            'personnel': 'บุคลากร'
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
            self.fields['personnel'].widget.attrs['readonly'] = True


class Performance(forms.ModelForm):
    class Meta:
        SEMETER_CHOICES = (('1', '1'), ('2', '2'), ('ฤดูร้อน', 'ฤดูร้อน'))
        TYPE_CHOICES = (
            ('งบประมาณแผ่นดิน', 'งบประมาณแผ่นดิน'),
            ('งบประมาณรายได้', 'งบประมาณรายได้'),
            ('งบประมาณส่วนตัว', 'งบประมาณส่วนตัว'),
            ('ไม่ใช้งบประมาณ', 'ไม่ใช้งบประมาณ')
        )
        model = Performance
        fields = ('getDate', 'fiscalYear', 'eduYear', 'eduSemeter', 'topic', 'detail', 'budget', 'budgetType', 'source',
                  'personnel')
        widgets = {
            'getDate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fiscalYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduYear': forms.NumberInput(attrs={'class': 'form-control', 'size': 10}),
            'eduSemeter': forms.RadioSelect(choices=SEMETER_CHOICES, attrs={'class': ''}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'cols': 55, 'rows': 5}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'size': 10, 'min': 1}),
            'budgetType': forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'size': 255, 'maxlength': 255}),
            'personnel': forms.HiddenInput(),
        }
        labels = {
            'getDate': 'วันที่ได้รางวัล/ผลงาน',
            'fiscalYear': 'ปีงบประมาณ',
            'eduYear': 'ปีการศึกษา',
            'eduSemeter': 'ภาคเรียนที่',
            'topic': 'เรื่อง/รางวัล/ผลงาน',
            'detail': 'รายละเอียด',
            'budget': 'งบประมาณ',
            'budgetType': 'ประเภทงบประมาณ',
            'source': 'หน่วยงานเจ้าของงบประมาณ',
            'personnel': 'บุคลากร'
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
