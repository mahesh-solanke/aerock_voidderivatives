"""aeroGeeksapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
urlpatterns = [
    path('ExceptionDetails',views.ExceptionDetails.as_view()),
    path('BGDayWiseData',views.BoardingGateDailyData.as_view()),
    path('BGHourWiseData',views.BoardingGateHourlyData.as_view()),
    path('BGTop3Utilization',views.BoardingGateTop3Utilization.as_view()),
    path('CBAveragePerDay',views.ConveyorBeltDailyAverageData.as_view()),
    path('CBAveragePerHour',views.ConveyorBeltHourlyAverageData.as_view()),
    path('CBPercentUtilPerDay',views.ConveyorBeltDailyPercentageUtilization.as_view()),
    path('CBPercentUtilPerHour',views.ConveyorBeltHourlyPercentageUtilization.as_view()),
    path('CBTop3Utilization',views.ConveyorBeltTop3Utilization.as_view()),
    path('FeddbackAverageUtilDay',views.FeddbackAverageUtilizationDay.as_view()),
    path('FeddbackAverageUtilSnapshot',views.FeddbackAverageUtilizationSnapshot.as_view()),
    path('FeddbackTop3Utilization',views.FeddbackTop3Utilization.as_view()),
    path('KioskDayWiseData',views.CheckinKioskDailyData.as_view()),
    path('KioskHourWiseData',views.CheckinKioskHourlyData.as_view()),
    path('KioskTop3Utilization',views.CheckinKioskTop3Utilization.as_view()),    
    path('ParkingDayWiseData',views.parkingDailyData.as_view()),
    path('ParkingHourWiseData',views.ParkingHourlyData.as_view()),  
    path('ParkingTop3Utilization',views.ParkingTop3Utilization.as_view()),
    path('SnDayWise',views.SanitizerDailyCalculations.as_view()),
    path('SnHourWise',views.SanitizerHourlyCalculations.as_view()),
    path('SnTop3Utilization',views.SanitizerTop3Utilization.as_view()),
    path('TrolleyDayWiseData',views.TrolleyDailyData.as_view()),
    path('TrolleyHourWiseData',views.TrolleyHourlyData.as_view()),
    path('TrolleyTop3Utilization',views.TrolleyTop3Utilization.as_view()),
    path('WifiDayWiseData',views.WifiDailyData.as_view()),
    path('WifiHourWiseData',views.WifiHourlyData.as_view()),
    path('WifiTop3Utilization',views.WifiTop3Utilization.as_view()),
    ]
