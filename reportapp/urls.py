from django.urls import path
from reportapp import views

urlpatterns = [
    path('personnelReport', views.personnelReport, name='personnelReport'),
    path('<divId>/<reportType>/personnelReport', views.personnelReport, name='personnelReport'),
    path('researchReport', views.researchReport, name='researchReport'),
    path('<budgetType>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/researchReport', views.researchReport, name='researchReport'),
    path('socialserviceReport', views.socialserviceReport, name='socialserviceReport'),
    path('<budgetType>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/socialserviceReport', views.socialserviceReport,
         name='socialserviceReport'),
    path('trainingReport', views.trainingReport, name='trainingReport'),
    path('<divId>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/trainingReport', views.trainingReport,
         name='trainingReport'),
]
