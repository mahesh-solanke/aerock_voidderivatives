from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import boardingday
from . models import boardinghour
from . models import cbavgday
from . models import cbavghour
from . models import cbperutilday
from . models import cbperutilhour
from . models import kioskday
from . models import kioskpeakperiod
from . models import parkavgduration
from . models import parkday
from . models import parkhour
from . models import parkpeakperiod
from . models import snareautilday
from . models import snareautilhour
from . models import snmaxconsume
from . models import sntotalconsumeday
from . models import sntotalconsumehour
from . models import trolleycalcday
from . models import trolleycalchour
from . models import wifiday
from . models import wifihour

from . serializer import boardingdaySerializer
from . serializer import boardinghourSerializer
from . serializer import cbavgdaySerializer
from . serializer import cbavghourSerializer
from . serializer import cbperutildaySerializer
from . serializer import cbperutilhourSerializer
from . serializer import kioskdaySerializer
from . serializer import kioskpeakperiodSerializer
from . serializer import parkavgdurationSerializer
from . serializer import parkdaySerializer
from . serializer import parkhourSerializer
from . serializer import parkpeakperiodSerializer
from . serializer import snareautildaySerializer
from . serializer import snareautilhourSerializer
from . serializer import snmaxconsumeSerializer
from . serializer import sntotalconsumedaySerializer
from . serializer import sntotalconsumehourSerializer
from . serializer import trolleycalcdaySerializer
from . serializer import trolleycalchourSerializer
from . serializer import wifidaySerializer
from . serializer import wifihourSerializer

class BoardingGateDailyData(APIView):
    def get(self, request):
        utilization = boardingday.objects.all()
        serializer = boardingdaySerializer(utilization,many = True)
        return Response(serializer.data)
    def post(self):
        pass

class BoardingGateHourlyData(APIView):
    def get(self,request):
        utilization = boardinghour.objects.all()
        serializer = boardinghourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class ConveyorBeltDailyAverageData(APIView):
    def get(self,request):
        utilization = cbavgday.objects.all()
        serializer = cbavgdaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class ConveyorBeltHourlyAverageData(APIView):
    def get(self,request):
        utilization = cbavghour.objects.all()
        serializer = cbavghourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class ConveyorBeltDailyPercentageUtilization(APIView):
    def get(self,request):
        utilization = cbperutilday.objects.all()
        serializer = cbperutildaySerializer(utilization,many=True)
        return Response(serializer.data) 
    def post(self):
        pass


class ConveyorBeltHourlyPercentageUtilization(APIView):
    def get(self,request):
        utilization = cbperutilhour.objects.all()
        serializer = cbperutilhourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class CheckinKioskDailyData(APIView):
    def get(self,request):
        utilization = kioskday.objects.all()
        serializer = kioskdaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
 #----------------------------------------------------------   
class CheckinKioskPeakPeriod(APIView):
    def get(self,request):
        utilization = kioskpeakperiod.objects.all()
        serializer =  kioskpeakperiodSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass


class ParkingAverageDuration(APIView):
    def get(self,request):
        utilization = parkavgduration.objects.all()
        serializer =  parkavgdurationSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class parkingDailyData(APIView):
    def get(self,request):
        utilization = parkday.objects.all()
        serializer =  parkdaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class ParkingHourlyData(APIView):
    def get(self,request):
        utilization = parkhour.objects.all()
        serializer =  parkhourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class ParkingPeakPeriod(APIView):
    def get(self,request):
        utilization = parkpeakperiod.objects.all()
        serializer =  parkpeakperiodSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class SanitizerDailyAreaWiseUtilization(APIView):
    def get(self,request):
        utilization = snareautilday.objects.all()
        serializer =  snareautildaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class SanitizerHourlyAreaWiseUtilization(APIView):
    def get(self,request):
        utilization = snareautilhour.objects.all()
        serializer =  snareautilhourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class SanitizerMaximumConsumption(APIView):
    def get(self,request):
        utilization = snmaxconsume.objects.all()
        serializer =  snmaxconsumeSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class SanitizerDailyTotalConsumption(APIView):
    def get(self,request):
        utilization = sntotalconsumeday.objects.all()
        serializer =  sntotalconsumedaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class SanitizerHourlyTotalConsumption(APIView):
    def get(self,request):
        utilization = sntotalconsumehour.objects.all()
        serializer =  sntotalconsumehourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class TrolleyDailyData(APIView):
    def get(self,request):
        utilization = trolleycalcday.objects.all()
        serializer =  trolleycalcdaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class TrolleyHourlyData(APIView):
    def get(self,request):
        utilization = trolleycalchour.objects.all()
        serializer =  trolleycalchourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class WifiDailyData(APIView):
    def get(self,request):
        utilization = wifiday.objects.all()
        serializer =  wifidaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
class WifiHourlyData(APIView):
    def get(self,request):
        utilization = wifihour.objects.all()
        serializer =  wifihourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass