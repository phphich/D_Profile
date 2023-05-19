from django.urls import path
from workapp import views

urlpatterns = [
    path('leaveList', views.leaveList, name='leaveList'),
    path('<divisionId>/<personnelId>/leaveList', views.leaveList, name='leaveList'),
    path('<id>/leaveDetail', views.leaveDetail, name='leaveDetail'),
    path('<id>/leaveNew', views.leaveNew, name='leaveNew'),
    path('<id>/leaveUpdate', views.leaveUpdate, name='leaveUpdate'),
    path('<id>/leaveDelete', views.leaveDelete, name='leaveDelete'),
    path('<id>/leaveDeleteFile', views.leaveDeleteFile, name='leaveDeleteFile'),
    path('<id>/leaveDeleteFileAll', views.leaveDeleteFileAll, name='leaveDeleteFileAll'),
    path('<id>/leaveDeleteURL', views.leaveDeleteURL, name='leaveDeleteURL'),
    path('<id>/leaveDeleteURLAll', views.leaveDeleteURLAll, name='leaveDeleteURLAll'),

    path('trainingList', views.trainingList, name='trainingList'),
    path('<divisionId>/<personnelId>/trainingList', views.trainingList, name='trainingList'),
    path('<id>/trainingDetail', views.trainingDetail, name='trainingDetail'),
    path('<id>/trainingNew', views.trainingNew, name='trainingNew'),
    path('<id>/trainingUpdate', views.trainingUpdate, name='trainingUpdate'),
    path('<id>/trainingDelete', views.trainingDelete, name='trainingDelete'),
    path('<id>/trainingDeleteFile', views.trainingDeleteFile, name='trainingDeleteFile'),
    path('<id>/trainingDeleteFileAll', views.trainingDeleteFileAll, name='trainingDeleteFileAll'),
    path('<id>/trainingDeleteURL', views.trainingDeleteURL, name='trainingDeleteURL'),
    path('<id>/trainingDeleteURLAll', views.trainingDeleteURLAll, name='trainingDeleteURLAll'),

]

