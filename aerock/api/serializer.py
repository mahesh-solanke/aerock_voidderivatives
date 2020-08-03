from rest_framework import serializers
# from rest_framework import salesemployee

from api.models import boardingday
from api.models import boardinghour
from api.models import cbavgday
from api.models import cbavghour
from api.models import cbperutilday
from api.models import cbperutilhour
from api.models import kioskday
from api.models import kioskpeakperiod
from api.models import parkavgduration
from api.models import parkday
from api.models import parkhour
from api.models import parkpeakperiod
from api.models import snareautilday
from api.models import snareautilhour
from api.models import snmaxconsume
from api.models import sntotalconsumeday
from api.models import sntotalconsumehour
from api.models import trolleycalcday
from api.models import trolleycalchour
from api.models import wifiday
from api.models import wifihour


class boardingdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = boardingday

        fields = [
        "_id",
        "date",
        "icao_code",
        "pct_utilization_usedseats",
        "avg_utilization_usedseats"]

class boardinghourSerializer(serializers.ModelSerializer):
    class Meta:
        model = boardinghour

        fields = [
        "_id",
        "avg_utilization_usedseats",
        "date",
        "hour",
        "icao_code",
        "pct_utilization_usedseats"]
class cbavgdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = cbavgday

        fields = [
        "_id",
        "date",
        "icao_code",
        "avg_opr_allconveyorbelts"]

class cbavghourSerializer(serializers.ModelSerializer):
    class Meta:
        model = cbavghour

        fields = [
        "_id",
        "avg_opr_allconveyorbelts",
        "date",
        "hour",
        "icao_code"]

class cbperutildaySerializer(serializers.ModelSerializer):
    class Meta:
        model = cbperutilday
        fields = [
        "_id",
        "cb_id",
        "pct_opr_eachconveyorbelt",
        "date",
        "icao_code"]

class cbperutilhourSerializer(serializers.ModelSerializer):
    class Meta:
        model = cbperutilhour
        fields = [
        "_id",
        "date",
        "hour",
        "icao_code",
        "cb_id",
        "pct_opr_eachconveyorbelt"]

class kioskdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = kioskday
        fields = [
        "_id",
        "date",
        "icao_code",
        "pct_utilization_day"]

class kioskpeakperiodSerializer(serializers.ModelSerializer):
    class Meta:
        model = kioskpeakperiod
        fields = [ "_id",
        "date",
        "icao_code",
        "hour",
        "num_of_visits"]

class parkavgdurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = parkavgduration
        fields = ["_id",
        "date",
        "icao_code",
        "slotid"]

class parkdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = parkday
        fields = ["_id",
        "date",
        "icao_code",
        "available_slots",
        "pct_occupied_slots"]

class parkhourSerializer(serializers.ModelSerializer):
    class Meta:
        model = parkhour
        fields = ["_id",
        "date",
        "icao_code",
        "hour",
        "available_slots",
        "pct_occupied_slots"]

class parkpeakperiodSerializer(serializers.ModelSerializer):
    class Meta:
        model = parkpeakperiod
        fields = ["_id",
        "date",
        "icao_code",
        "hour",
        "used_slots",
        "maxused_time"]

class snareautildaySerializer(serializers.ModelSerializer):
    class Meta:
        model = snareautilday
        fields = ["_id",
        "areaid",
        "pct_areawise_util",
        "date",
        "icao_code"]

class snareautilhourSerializer(serializers.ModelSerializer):
    class Meta:
        model = snareautilhour
        fields = ["_id",
        "areaid",
        "pct_areawise_util",
        "date",
        "hour",
        "icao_code"]

class snmaxconsumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = snmaxconsume
        fields = ["_id",
        "date",
        "hour",
        "icao_code",
        "max_dispenses"]

class sntotalconsumedaySerializer(serializers.ModelSerializer):
    class Meta:
        model = sntotalconsumeday
        fields = ["_id",
        "date",
        "icao_code",
        "total_dispenses"]

class sntotalconsumehourSerializer(serializers.ModelSerializer):
    class Meta:
        model = sntotalconsumehour
        fields = ["_id",
        "date",
        "hour",
        "icao_code",
        "total_dispenses"]

class trolleycalcdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = trolleycalcday
        fields = ["_id",
        "date",
        "pct_utilization_usedtrolley",
        "icao_code",
        "unused_trolleys",
        "used_trolleys"]

class trolleycalchourSerializer(serializers.ModelSerializer):
    class Meta:
        model = trolleycalchour
        
        fields = ["_id",
        "date",
        "hour",
        "icao_code",
        "pct_utilization_usedtrolley",
        "unused_trolleys",
        "used_trolleys"]

class wifidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = wifiday
        fields = ["_id",
        "avg_utilization",
        "date",
        "icao_code",
        "total_download",
        "total_upload",
        "total_used_minutes",
        "total_users"]

class wifihourSerializer(serializers.ModelSerializer):
    class Meta:
        model = wifihour 
        fields = ["_id",
        "avg_utilization",
        "date",
        "hour",
        "icao_code",
        "total_download",
        "total_upload",
        "total_used_minutes",
        "total_users"]
