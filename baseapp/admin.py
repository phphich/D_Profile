from django.contrib import admin
from baseapp.models import *

class CurrAffiliationAdmin(admin.ModelAdmin):
    ordering = ['personnel']
admin.site.register(Faculty)
admin.site.register(Division)
admin.site.register(Curriculum)
class PersonnelAdmin(admin.ModelAdmin):
    ordering = ['firstname_th', 'lastname_th']
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Education)
admin.site.register(Expertise)
admin.site.register(CurrAffiliation, CurrAffiliationAdmin)


