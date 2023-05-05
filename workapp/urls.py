from django.urls import path
from workapp import views

urlpatterns = [
    path('leaveList', views.leaveList, name='leaveList'),
    path('<divisionId>/<personnelId>/leaveList', views.leaveList, name='leaveList'),
    path('<id>/leaveDetail', views.leaveDetail, name='leaveDetail'),
    path('<id>/leaveNew', views.leaveNew, name='leaveNew'),
    path('<id>/leaveUpdate', views.leaveUpdate, name='leaveUpdate'),
    path('<id>/leaveDelete', views.leaveDelete, name='leaveDelete'),


]

