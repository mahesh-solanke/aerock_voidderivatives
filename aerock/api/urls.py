from django.urls import path

from . import views
app_name='api'

urlpatterns = [
    path('BGDayWiseData',views.BoardingGateDailyData.as_view()),
    path('BGHourWiseData',views.BoardingGateHourlyData.as_view()),
    path('CBAveragePerDay',views.ConveyorBeltDailyAverageData.as_view()),
    path('CBAveragePerHour',views.ConveyorBeltHourlyAverageData.as_view()),
    path('CBPercentUtilPerDay',views.ConveyorBeltDailyPercentageUtilization.as_view()),
    path('CBPercentUtilPerHour',views.ConveyorBeltHourlyPercentageUtilization.as_view()),
    path('KioskDayWiseData',views.CheckinKioskDailyData.as_view()),
    path('KioskPeakPeriod',views.CheckinKioskPeakPeriod.as_view()),
    path('ParkingAvgDuration',views.ParkingAverageDuration.as_view()),
    path('ParkingDayWiseData',views.parkingDailyData.as_view()),
    path('ParkingHourWiseData',views.ParkingHourlyData.as_view()),
    path('ParkingPeakPeriod',views.ParkingPeakPeriod.as_view()),
    path('SnAreaWiseUtilPerDay',views.SanitizerDailyAreaWiseUtilization.as_view()),
    path('SnAreaWiseUtilPerHour',views.SanitizerHourlyAreaWiseUtilization.as_view()),
    path('SnMaxConsume',views.SanitizerMaximumConsumption.as_view()),
    path('SnTotalComsumPerDay',views.SanitizerDailyTotalConsumption.as_view()),
    path('SnTotalComsumPerHour',views.SanitizerHourlyTotalConsumption.as_view()),
    path('TrolleyDayWiseData',views.TrolleyDailyData.as_view()),
    path('TrolleyHourWiseData',views.TrolleyHourlyData.as_view()),
    path('WifiDayWiseData',views.WifiDailyData.as_view()),
    path('WifiHourWiseData',views.WifiHourlyData.as_view()),
    ]
