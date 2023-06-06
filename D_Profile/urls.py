"""
URL configuration for D_Profile project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import baseapp.views
from baseapp import views
from workapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', baseapp.views.home, name='home'),
    path('userAuthen', baseapp.views.userAuthen, name='userAuthen'),
    path('userLogout', baseapp.views.userLogout, name='userLogout'),
    path('userChgPassword', baseapp.views.userChgPassword, name='userChgPassword'),
    path('<id>/userResetPassword', baseapp.views.userResetPassword, name='userResetPassword'),
    path('helpme', baseapp.views.helpme, name='helpme'),
    path('helpReset', baseapp.views.helpReset, name='helpReset'),
    # path('permissionerror', baseapp.views.permissionerror, name='permissionerror'),
    path('devteam', baseapp.views.devteam, name='devteam'),
    path('objective', baseapp.views.objective, name='objective'),
    path('baseapp/', include('baseapp.urls')),
    path('workapp/', include('workapp.urls')),

]
