from django.urls import path
from reportapp import views

urlpatterns = [
    path('personnelReport', views.personnelReport, name='personnelReport'),
    path('<reportType>/personnelReport', views.personnelReport, name='personnelReport'),
    

]
