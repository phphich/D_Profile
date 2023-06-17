from django.urls import path
from reportapp import views

urlpatterns = [
    path('personnelReport', views.personnelReport, name='personnelReport'),
    path('<divId>/<reportType>/personnelReport', views.personnelReport, name='personnelReport'),
    path('<subNo>/<divId>/<paraValue>/personnelSubReport', views.reportSubPersonnel, name='personnelSubReport'),
    path('<personnelId>/personnelDetailReport', views.personnelDetailReport, name='personnelDetailReport'),
    # -------------------------------- #
    path('leaveReport', views.leaveReport, name='leaveReport'),
    path('<divId>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/leaveReport', views.leaveReport,
         name='leaveReport'),
    path('<subNo>/<name>/<paraValue>/leaveSubReport', views.leaveSubReport, name='leaveSubReport'),
    path('<leaveId>/leaveDetailReport', views.leaveDetailReport, name='leaveDetailReport'),
    # -------------------------------- #
    path('trainingReport', views.trainingReport, name='trainingReport'),
    path('<divId>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/trainingReport', views.trainingReport,
         name='trainingReport'),
    path('<subNo>/<divName>/<paraValue>/trainingSubReport', views.trainingSubReport, name='trainingSubReport'),
    path('<trainingId>/trainingDetailReport', views.trainingDetailReport, name='trainingDetailReport'),
    # -------------------------------- #
    path('performanceReport', views.performanceReport, name='performanceReport'),
    path('<divId>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/performanceReport', views.performanceReport,
         name='performanceReport'),
    path('<subNo>/<divName>/<paraValue>/performanceSubReport', views.performanceSubReport, name='performanceSubReport'),
    path('<performanceId>/performanceDetailReport', views.performanceDetailReport, name='performanceDetailReport'),
    # -------------------------------- #
    path('researchReport', views.researchReport, name='researchReport'),
    path('<budgetType>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/researchReport', views.researchReport, name='researchReport'),
    path('<subNo>/<budgetType>/<paraValue>/researchSubReport', views.researchSubReport, name='researchSubReport'),
    path('<researchId>/researchDetailReport', views.researchDetailReport, name='researchDetailReport'),
    # -------------------------------- #
    path('socialserviceReport', views.socialserviceReport, name='socialserviceReport'),
    path('<budgetType>/<fiscalYearStart>/<fiscalYearEnd>/<reportType>/socialserviceReport', views.socialserviceReport,
         name='socialserviceReport'),
    path('<subNo>/<budgetType>/<paraValue>/socialserviceSubReport', views.socialserviceSubReport, name='socialserviceSubReport'),
    path('<socialserviceId>/soreserviceDetailReport', views.socialserviceDetailReport, name='socialserviceDetailReport'),
    # -------------------------------- #

    path('commandReport', views.commandReport, name='commandReport'),
    path('<mission>/<eduYearStart>/<eduYearEnd>/<reportType>/commandReport', views.commandReport,
         name='commandReport'),
    path('<subNo>/<mission>/<paraValue>/commandSubReport', views.commandSubReport, name='commandSubReport'),
    path('<commandId>/commandDetailReport', views.commandDetailReport, name='commandDetailReport'),
]
