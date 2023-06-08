from django.urls import path
from workapp import views

urlpatterns = [
    # การลา
    path('leaveList', views.leaveList, name='leaveList'),
    path('<pageNo>/leaveList', views.leaveList, name='leaveList'),
    path('<divisionId>/<personnelId>/leaveList', views.leaveList, name='leaveList'),
    path('<divisionId>/<personnelId>/<pageNo>/leaveList', views.leaveList, name='leaveList'),
    path('<id>/leaveDetail', views.leaveDetail, name='leaveDetail'),
    path('<id>/leaveNew', views.leaveNew, name='leaveNew'),
    path('<id>/leaveUpdate', views.leaveUpdate, name='leaveUpdate'),
    path('<id>/leaveDelete', views.leaveDelete, name='leaveDelete'),
    path('<id>/leaveDeleteFile', views.leaveDeleteFile, name='leaveDeleteFile'),
    path('<id>/leaveDeleteFileAll', views.leaveDeleteFileAll, name='leaveDeleteFileAll'),
    path('<id>/leaveDeleteURL', views.leaveDeleteURL, name='leaveDeleteURL'),
    path('<id>/leaveDeleteURLAll', views.leaveDeleteURLAll, name='leaveDeleteURLAll'),

    # การฝึกอบรม/สัมมนา
    path('trainingList', views.trainingList, name='trainingList'),
    path('<pageNo>/trainingList', views.trainingList, name='trainingList'),
    path('<divisionId>/<personnelId>/trainingList', views.trainingList, name='trainingList'),
    path('<divisionId>/<personnelId>/<pageNo>/trainingList', views.trainingList, name='trainingList'),
    path('<id>/trainingDetail', views.trainingDetail, name='trainingDetail'),
    path('<id>/trainingNew', views.trainingNew, name='trainingNew'),
    path('<id>/trainingUpdate', views.trainingUpdate, name='trainingUpdate'),
    path('<id>/trainingDelete', views.trainingDelete, name='trainingDelete'),
    path('<id>/trainingDeleteFile', views.trainingDeleteFile, name='trainingDeleteFile'),
    path('<id>/trainingDeleteFileAll', views.trainingDeleteFileAll, name='trainingDeleteFileAll'),
    path('<id>/trainingDeleteURL', views.trainingDeleteURL, name='trainingDeleteURL'),
    path('<id>/trainingDeleteURLAll', views.trainingDeleteURLAll, name='trainingDeleteURLAll'),

    # ผลงาน/รางวัล 
    path('performanceList', views.performanceList, name='performanceList'),
    path('<pageNo>/performanceList', views.performanceList, name='performanceList'),
    path('<divisionId>/<personnelId>/performanceList', views.performanceList, name='performanceList'),
    path('<divisionId>/<personnelId>/<pageNo>/performanceList', views.performanceList, name='performanceList'),
    path('<id>/performanceDetail', views.performanceDetail, name='performanceDetail'),
    path('<id>/performanceNew', views.performanceNew, name='performanceNew'),
    path('<id>/performanceUpdate', views.performanceUpdate, name='performanceUpdate'),
    path('<id>/performanceDelete', views.performanceDelete, name='performanceDelete'),
    path('<id>/performanceDeleteFile', views.performanceDeleteFile, name='performanceDeleteFile'),
    path('<id>/performanceDeleteFileAll', views.performanceDeleteFileAll, name='performanceDeleteFileAll'),
    path('<id>/performanceDeleteURL', views.performanceDeleteURL, name='performanceDeleteURL'),
    path('<id>/performanceDeleteURLAll', views.performanceDeleteURLAll, name='performanceDeleteURLAll'),

    # คำสั่ง
    path('commandList', views.commandList, name='commandList'),
    path('<pageNo>/commandList', views.commandList, name='commandList'),
    path('<id>/commandDetail', views.commandDetail, name='commandDetail'),
    path('commandNew', views.commandNew, name='commandNew'),
    path('<id>/commandUpdate', views.commandUpdate, name='commandUpdate'),
    path('<id>/commandDelete', views.commandDelete, name='commandDelete'),
    path('<id>/commandDeleteFile', views.commandDeleteFile, name='commandDeleteFile'),
    path('<id>/commandDeleteFileAll', views.commandDeleteFileAll, name='commandDeleteFileAll'),
    path('<id>/commandDeleteURL', views.commandDeleteURL, name='commandDeleteURL'),
    path('<id>/commandDeleteURLAll', views.commandDeleteURLAll, name='commandDeleteURLAll'),
    path('<id>/commandDeleteCommandPerson', views.commandDeleteCommandPerson, name='commandDeleteCommandPerson'),
    path('<id>/commandDeleteCommandPersonAll', views.commandDeleteCommandPersonAll,
         name='commandDeleteCommandPersonAll'),

    # วิจัย
    path('researchList', views.researchList, name='researchList'),
    path('<pageNo>/researchList', views.researchList, name='researchList'),
    path('<id>/researchDetail', views.researchDetail, name='researchDetail'),
    path('researchNew', views.researchNew, name='researchNew'),
    path('<id>/researchUpdate', views.researchUpdate, name='researchUpdate'),
    path('<id>/researchDelete', views.researchDelete, name='researchDelete'),
    path('<id>/researchDeleteFile', views.researchDeleteFile, name='researchDeleteFile'),
    path('<id>/researchDeleteFileAll', views.researchDeleteFileAll, name='researchDeleteFileAll'),
    path('<id>/researchDeleteURL', views.researchDeleteURL, name='researchDeleteURL'),
    path('<id>/researchDeleteURLAll', views.researchDeleteURLAll, name='researchDeleteURLAll'),
    path('<id>/researchDeleteResearchPerson', views.researchDeleteResearchPerson, name='researchDeleteResearchPerson'),
    path('<id>/researchDeleteResearchPersonAll', views.researchDeleteResearchPersonAll,
         name='researchDeleteResearchPersonAll'),

    # บริการทางวิชาการแก่สังคม 
    path('socialserviceList', views.socialserviceList, name='socialserviceList'),
    path('<pageNo>/socialserviceList', views.socialserviceList, name='socialserviceList'),
    path('<id>/socialserviceDetail', views.socialserviceDetail, name='socialserviceDetail'),
    path('socialserviceNew', views.socialserviceNew, name='socialserviceNew'),
    path('<id>/socialserviceUpdate', views.socialserviceUpdate, name='socialserviceUpdate'),
    path('<id>/socialserviceDelete', views.socialserviceDelete, name='socialserviceDelete'),
    path('<id>/socialserviceDeleteFile', views.socialserviceDeleteFile, name='socialserviceDeleteFile'),
    path('<id>/socialserviceDeleteFileAll', views.socialserviceDeleteFileAll, name='socialserviceDeleteFileAll'),
    path('<id>/socialserviceDeleteURL', views.socialserviceDeleteURL, name='socialserviceDeleteURL'),
    path('<id>/socialserviceDeleteURLAll', views.socialserviceDeleteURLAll, name='socialserviceDeleteURLAll'),
    path('<id>/socialserviceDeleteSocialServicePerson', views.socialserviceDeleteSocialServicePerson, name='socialerviceDeleteSocialServicePerson'),
    path('<id>/socialserviceDeleteSocialServicePersonAll', views.socialserviceDeleteSocialServicePerson,
         name='socialserviceDeleteSocialServicePersonAll'),

]

