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

]

