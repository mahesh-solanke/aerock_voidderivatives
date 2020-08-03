"""aerock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('adminpage/',include('dashboard.urls')),
    path('',include('dashboard.urls')),
 #   path('contactus/',include('dashboard.urls')),
  #  path('login/',include('dashboard.urls')),
#    path('aai/',include('dashboard.urls')),
#   path('support/',include('dashboard.urls')),
#    path('airport/',include('dashboard.urls')),
#    path('staff/',include('dashboard.urls')),
#    path('enablefacility',include('dashboard.urls')),
#    path('logout',include('dashboard.urls')),
#    path('addairport/',include('dashboard.urls')),
#    path('forgotpassword/',include('dashboard.urls')),
#    path('resetpassword/',include('dashboard.urls')),
#    path('changethreshold/',include('dashboard.urls')),
    ]
