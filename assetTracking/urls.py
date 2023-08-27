"""
URL configuration for assetTracking project.

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
from django.urls import path
from assetManagement.views import *

urlpatterns = [
    path('',employee,name="employee"),
    path('device/',device,name="device"),
    path('check-out/<id>/', check_out, name="check_out"),
    path('return-back/<id>/', return_back, name="return_back"),
    path('device-log/',device_log,name="device_log"),
    path('admin/', admin.site.urls),
]
