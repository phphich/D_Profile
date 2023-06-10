from django.urls import path
from reportapp import views

urlpatterns = [
    path('personnelReport', views.personnelReport, name='personnelReport'),
    path('<divId>/<reportType>/personnelReport', views.personnelReport, name='personnelReport'),
    path('researchReport', views.researchReport, name='researchReport'),
    path('<budgetType>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/researchReport', views.researchReport, name='researchReport'),



]
