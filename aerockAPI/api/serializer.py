from rest_framework import serializers
# from rest_framework import salesemployee


from api.models import boardingday
from api.models import boardinghour
from api.models import boardtop3utilization
from api.models import cbavgday
from api.models import cbavghour
from api.models import cbperutilday
from api.models import cbperutilhour
from api.models import cbtop3utilization
from api.models import fbavgutilday
from api.models import fbavgutilsnapshot
from api.models import fbtop3utilization
from api.models import kioskday
from api.models import kioskhour
from api.models import kiosktop3utilization
from api.models import parkingday
from api.models import parkingkhour
from api.models import parkingtop3utilization
from api.models import sncalcday
from api.models import sncalchour
from api.models import sntop3utilization
from api.models import trolleycalcday
from api.models import trolleycalchour
from api.models import trolleytop3utilization
from api.models import wifiday
from api.models import wifihour
from api.models import wifitop3utilization

from api.models import exception_details
from datetime import timedelta 
import time
#epoch = datetime.date(1970,1,1)
class exception_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = exception_details
        fields = ["_id",
        'event_time',
        "facility",
        "deviceid",
        "areaid",
        "icao_code",
        "actual_value",
        "threshold_value",
        "state"]

class boardingdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = boardingday
        fields = ["_id",
        "date",
        "icao_code",
        "count_used",
        "count_unused",
        "total_count",
        "pct_utilization"]
class boardinghourSerializer(serializers.ModelSerializer):
    class Meta:
        model = boardinghour
        fields = ["_id",
        "date",
        "hour",
        "icao_code",
        "count_used",
        "count_unused",
        "total_count",
        "pct_utilization_usedseats"]
class boardtop3utilizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = boardtop3utilization
        fields = ["_id",
        "date",
        "icao_code",
        "hour",
        "rank",
        "pct_utilization"]
class cbavgdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = cbavgday
        fields = ["_id" ,
        "date",
        "icao_code",
        "avg_opr_allconveyorbelts_min"]
class cbavghourSerializer(serializers.ModelSerializer):
    class Meta:
        model = cbavghour
        fields = [ "_id",
        "date",
        "hour",
        "icao_code"]
class cbperutildaySerializer(serializers.ModelSerializer):
    class Meta:
        model = cbperutilday
        fields = [ "_id",
        "cb_id",
        "pct_opr_allconveyorbelts",
        "date",
        "icao_code"]
class cbperutilhourSerializer(serializers.ModelSerializer):
    class Meta:
        model = cbperutilhour
        fields = ["_id",
        "cb_id",
        "pct_opr_allconveyorbelts",
        "date",
        "hour",
        "icao_code"]

class cbtop3utilizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = cbtop3utilization
        fields = ["_id",
        "date",
        "icao_code",
        "hour",
        "rank",
        "pct_utilization"]
class fbavgutildaySerializer(serializers.ModelSerializer):
    class Meta:
        model = fbavgutilday
        fields = ["_id",
        "date",
        "icao_code",
        "rating_for_service",
        "service_id"]
class fbavgutilsnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = fbavgutilsnapshot
        fields = ["_id",
        "icao_code",
        "rating_for_service",
        "service_id"]
class fbtop3utilizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = fbtop3utilization
        fields = ["_id",
        "icao_code",
        "service_id",
        "rating_for_service",
        "rank"]
class kioskdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = kioskday
        fields = ["_id",
        "date",
        "icao_code",
        "pct_utilization",
        "count_of_visits",
        "count_of_devices"]
class kioskhourSerializer(serializers.ModelSerializer):
    class Meta:
        model = kioskhour
        fields = ["_id",
        "date",
        "hour",
        "icao_code",
        "count_of_visits",
        "count_of_devices",
        "pct_utilization"]
class kiosktop3utilizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = kiosktop3utilization
        fields = ["_id",
        "date",
        "icao_code",
        "hour",
        "rank",
        "pct_utilization"]
class parkingdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = parkingday
        fields = ["_id",
        "date",
        "icao_code",
        "pct_utilization",
        "count_of_occupancy",
        "count_of_devices"]
class parkingkhourSerializer(serializers.ModelSerializer):
    class Meta:
        model = parkingkhour
        fields = ["_id",
        "date",
        "hour",
        "icao_code",
        "count_of_occupancy",
        "count_of_slots",
        "pct_utilization"]
class parkingtop3utilizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = parkingtop3utilization
        fields = ["_id",
        "date",
        "icao_code",
        "hour",
        "rank",
        "pct_utilization"]
class sncalcdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = sncalcday
        fields = ["_id",
        "date",
        "icao_code",
        "areaid",
        "count_dispenses",
        "no_of_containers",
        "refills",
        "avg_dispenses"]

class sncalchourSerializer(serializers.ModelSerializer):
    class Meta:
        model = sncalchour
        fields = ["_id",
        "date",
        "icao_code",
        "areaid",
        "hour",
        "count_dispenses",
        "no_of_containers",
        "refills",
        "avg_dispenses"]
class sntop3utilizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = sntop3utilization
        fields = ["_id",
        "date",
        "icao_code",
        "areaid",
        "rank",
        "avg_dispenses",
        "hour"]
class trolleycalcdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = trolleycalcday
        fields = ["_id",
        "date",
        "icao_code",
        "pct_utilization",
        "count_unused",
        "count_used",
        "total_count"]
class trolleycalchourSerializer(serializers.ModelSerializer):
    class Meta:
        model = trolleycalchour
        fields = ["_id",
        "date",
        "hour",
        "icao_code",
        "pct_utilization",
        "count_unused",
        "count_used",
        "total_count"]
class trolleytop3utilizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = trolleytop3utilization
        fields = ["_id",
        "date",
        "icao_code",
        "hour",
        "rank",
        "pct_utilization"]
class wifidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = wifiday
        fields = ["_id",
        "avg_utilization_min",
        "date",
        "icao_code",
        "total_download",
        "total_upload",
        "total_used_minutes",
        "total_unique_users"]
class wifihourSerializer(serializers.ModelSerializer):
    class Meta:
        model = wifihour
        fields = ["_id",
        "date",
        "hour",
        "icao_code",
        "total_download",
        "total_upload",
        "total_used_minutes",
        "total_unique_users",
        "avg_utilization_min"]
class wifitop3utilizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = wifitop3utilization
        fields = ["_id",
        "date",
        "icao_code",
        "hour",
        "rank",
        "avg_utilization_min"]