from django.urls import path
from baseapp import views

urlpatterns = [
    path('personnelList', views.personnelList, name='personnelList' ),
    path('personnelNew', views.personnelNew, name='personnelNew' ),
    path('<id>/personnelDetail', views.personnelDetail, name='personnelDetail'),
    path('<id>/personnelUpdate', views.personnelNew, name='personnelUpdate'),
    path('<id>/personnelDelete', views.personnelNew, name='personnelDelete'),

]
