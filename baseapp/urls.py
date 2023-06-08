from django.urls import path
from baseapp import views

urlpatterns = [
    path('facultyDetail', views.facultyDetail, name='facultyDetail'),
    path('facultyUpdate', views.facultyUpdate, name='facultyUpdate'),

    path('divisionList', views.divisionList, name='divisionList'),
    path('divisionNew', views.divisionNew, name='divisionNew'),
    path('<id>/divisionUpdate', views.divisionUpdate, name='divisionUpdate'),
    path('<id>/divisionDelete', views.divisionDelete, name='divisionDelete'),

    path('curriculumList', views.curriculumList, name='curriculumList'),
    path('curriculumNew', views.curriculumNew, name='curriculumNew'),
    path('<id>/curriculumUpdate', views.curriculumUpdate, name='curriculumUpdate'),
    path('<id>/curriculumDelete', views.curriculumDelete, name='curriculumDelete'),

    # path('personnelList', views.personnelList, name='personnelList' ),
    path('personnelList', views.personnelList, name='personnelList' ),
    path('<pageNo>/personnelList', views.personnelList, name='personnelList' ),
    path('personnelNew', views.personnelNew, name='personnelNew' ),
    path('<id>/personnelDetail', views.personnelDetail, name='personnelDetail'),
    path('<id>/personnelUpdate', views.personnelUpdate, name='personnelUpdate'),
    path('<id>/personnelDelete', views.personnelDelete, name='personnelDelete'),

    path('educatonList', views.educationList, name='educationList'),
    path('<divisionId>/<personnelId>/educatonList', views.educationList, name='educationList'),
    path('<id>/educationNew', views.educationNew, name='educationNew'),
    path('<id>/educationDetail', views.educationDetail, name='educationDetail'),
    path('<id>/educationUpdate', views.educationUpdate, name='educationUpdate'),
    path('<id>/educationDelete', views.educationDelete, name='educationDelete'),

    path('expertiseList', views.expertiseList, name='expertiseList'),
    path('<divisionId>/<personnelId>/expertiseList', views.expertiseList, name='expertiseList'),
    path('<id>/expertiseNew', views.expertiseNew, name='expertiseNew'),
    path('<id>/expertiseDetail', views.expertiseDetail, name='expertiseDetail'),
    path('<id>/expertiseUpdate', views.expertiseUpdate, name='expertiseUpdate'),
    path('<id>/expertiseDelete', views.expertiseDelete, name='expertiseDelete'),

    path('currAffiliationList', views.currAffiliationList, name='currAffiliationList'),
    path('<curriculumId>/currAffiliationList', views.currAffiliationList, name='currAffiliationList'),
    path('<id>/currAffiliationDelete', views.currAffiliationDelete, name='currAffiliationDelete'),

    path('responsibleList', views.responsibleList, name='responsibleList'),
    path('<pageNo>/responsibleList', views.responsibleList, name='responsibleList'),
    path('<id>/responsibleDelete', views.responsibleDelete, name='responsibleDelete'),

    path('headerList', views.headerList, name='headerList'),
    path('<pageNo>/headerList', views.headerList, name='headerList'),
    path('<id>/headerDelete', views.headerDelete, name='headerDelete'),

    path('managerList', views.managerList, name='managerList'),
    path('<id>/managerDelete', views.managerDelete, name='managerDelete'),

    # report **************
    path('personnelReport', views.personnelReport, name='personnelReport'),
    

]
