from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta


from . models import boardingday
from . models import boardinghour
from . models import boardtop3utilization
from . models import cbavgday
from . models import cbavghour
from . models import cbperutilday
from . models import cbperutilhour
from . models import cbtop3utilization
from . models import fbavgutilday
from . models import fbavgutilsnapshot
from . models import fbtop3utilization
from . models import kioskday
from . models import kioskhour
from . models import kiosktop3utilization
from . models import parkingday
from . models import parkingkhour
from . models import parkingtop3utilization
from . models import sncalcday
from . models import sncalchour
from . models import sntop3utilization
from . models import trolleycalcday
from . models import trolleycalchour
from . models import trolleytop3utilization
from . models import wifiday
from . models import wifihour
from . models import wifitop3utilization



from . serializer import boardingdaySerializer
from . serializer import boardinghourSerializer
from . serializer import boardtop3utilizationSerializer
from . serializer import cbavgdaySerializer
from . serializer import cbavghourSerializer
from . serializer import cbperutildaySerializer
from . serializer import cbperutilhourSerializer
from . serializer import cbtop3utilizationSerializer
from . serializer import fbavgutildaySerializer
from . serializer import fbavgutilsnapshotSerializer
from . serializer import fbtop3utilizationSerializer
from . serializer import kioskdaySerializer
from . serializer import kioskhourSerializer
from . serializer import kiosktop3utilizationSerializer
from . serializer import parkingdaySerializer
from . serializer import parkingkhourSerializer
from . serializer import parkingtop3utilizationSerializer
from . serializer import sncalcdaySerializer
from . serializer import sncalchourSerializer
from . serializer import sntop3utilizationSerializer
from . serializer import trolleycalcdaySerializer
from . serializer import trolleycalchourSerializer
from . serializer import trolleytop3utilizationSerializer
from . serializer import wifidaySerializer
from . serializer import wifihourSerializer
from . serializer import wifitop3utilizationSerializer
from . models import exception_details
from . serializer import exception_detailsSerializer

from datetime import timedelta 
import time
from calendar import timegm

class ExceptionDetails(APIView):
    def get(self,request):
        event_time = request.GET.get('event_time')
        if event_time is None:
            time_threshold = datetime.now() - timedelta(minutes=1)
            strdate = str(time_threshold.strftime('%Y,%m,%d, %H,%M,%S'))
            utc_time = time.strptime(strdate, '%Y,%m,%d, %H,%M,%S')
            epoch_time = timegm(utc_time)
            utilization = exception_details.objects.filter(event_time__gt = epoch_time)
            serializer = exception_detailsSerializer(utilization,many=True)
            return Response(serializer.data)
        else:
            utilization = exception_details.objects.filter(event_time__gt = event_time)
            serializer = exception_detailsSerializer(utilization,many=True)
            return Response(serializer.data)

    def post(self):
        pass

class BoardingGateDailyData(APIView):
    def get(self,request):
        
        utilization = boardingday.objects.all()
        serializer = boardingdaySerializer(utilization,many=True)
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

class BoardingGateTop3Utilization(APIView):
    def get(self,request):
        utilization = boardtop3utilization.objects.all()
        serializer = boardtop3utilizationSerializer(utilization,many=True)
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

class ConveyorBeltTop3Utilization(APIView):
    def get(self,request):
        utilization = cbtop3utilization.objects.all()
        serializer = cbtop3utilizationSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass


class FeddbackAverageUtilizationDay(APIView):
    def get(self,request):
        utilization = fbavgutilday.objects.all()
        serializer = fbavgutildaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class FeddbackAverageUtilizationSnapshot(APIView):
    def get(self,request):
        utilization = fbavgutilsnapshot.objects.all()
        serializer = fbavgutilsnapshotSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class FeddbackTop3Utilization(APIView):
    def get(self,request):
        utilization = fbtop3utilization.objects.all()
        serializer = fbtop3utilizationSerializer(utilization,many=True)
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

class CheckinKioskHourlyData(APIView):
    def get(self,request):
        utilization = kioskhour.objects.all()
        serializer = kioskhourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class CheckinKioskTop3Utilization(APIView):
    def get(self,request):
        utilization = kiosktop3utilization.objects.all()
        serializer = kiosktop3utilizationSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
    
class parkingDailyData(APIView):
    def get(self,request):
        utilization = parkingday.objects.all()
        serializer = parkingdaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class ParkingHourlyData(APIView):
    def get(self,request):
        utilization = parkingkhour.objects.all()
        serializer = parkingkhourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
  
class ParkingTop3Utilization(APIView):
    def get(self,request):
        utilization = parkingtop3utilization.objects.all()
        serializer = parkingtop3utilizationSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class SanitizerDailyCalculations(APIView):
    def get(self,request):
        utilization = sncalcday.objects.all()
        serializer = sncalcdaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class SanitizerHourlyCalculations(APIView):
    def get(self,request):
        utilization = sncalchour.objects.all()
        serializer = sncalchourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class SanitizerTop3Utilization(APIView):
    def get(self,request):
        utilization = sntop3utilization.objects.all()
        serializer = sntop3utilizationSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class TrolleyDailyData(APIView):
    def get(self,request):
        utilization = trolleycalcday.objects.all()
        serializer = trolleycalcdaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class TrolleyHourlyData(APIView):
    def get(self,request):
        utilization = trolleycalchour.objects.all()
        serializer = trolleycalchourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class TrolleyTop3Utilization(APIView):
    def get(self,request):
        utilization = trolleytop3utilization.objects.all()
        serializer = trolleytop3utilizationSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class WifiDailyData(APIView):
    def get(self,request):
        utilization = wifiday.objects.all()
        serializer = wifidaySerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class WifiHourlyData(APIView):
    def get(self,request):
        utilization = wifihour.objects.all()
        serializer = wifihourSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class WifiTop3Utilization(APIView):
    def get(self,request):
        utilization = wifitop3utilization.objects.all()
        serializer = wifitop3utilizationSerializer(utilization,many=True)
        return Response(serializer.data)
    def post(self):
        pass
