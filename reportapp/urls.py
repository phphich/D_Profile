from django.urls import path
from reportapp import views

urlpatterns = [
    path('personnelReport', views.personnelReport, name='personnelReport'),
    path('<divId>/<reportType>/personnelReport', views.personnelReport, name='personnelReport'),
    path('<subNo>/<divId>/<paraValue>/personnelSubReport', views.reportSubPersonnel, name='personnelSubReport'),
    path('<personnelId>/personnelDetailReport', views.personnelDetailReport, name='personnelDetailReport'),
    # -------------------------------- #
    path('researchReport', views.researchReport, name='researchReport'),
    path('<budgetType>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/researchReport', views.researchReport, name='researchReport'),
    path('<subNo>/<budgetType>/<paraValue>/researchSubReport', views.researchSubReport, name='researchSubReport'),
    path('<researchId>/researchDetailReport', views.researchDetailReport, name='researchDetailReport'),
    # -------------------------------- #
    path('socialserviceReport', views.socialserviceReport, name='socialserviceReport'),
    path('<budgetType>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/socialserviceReport', views.socialserviceReport,
         name='socialserviceReport'),
    path('<socialserviceId>/soreserviceDetailReport', views.socialserviceDetailReport, name='socialserviceDetailReport'),
    # -------------------------------- #
    path('trainingReport', views.trainingReport, name='trainingReport'),
    path('<divId>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/trainingReport', views.trainingReport,
         name='trainingReport'),
    path('leaveReport', views.leaveReport, name='leaveReport'),
    path('<divId>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/leaveReport', views.leaveReport,
         name='leaveReport'),

    path('commandReport', views.commandReport, name='commandReport'),
    path('<mission>/<eduYearStart>/<eduYearEnd>/<reportType>/commandReport', views.commandReport,
         name='commandReport'),

]
