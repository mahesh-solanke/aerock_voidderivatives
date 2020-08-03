from djongo import models
from unixtimestampfield.fields import UnixTimeStampField
class exception_details(models.Model):
	_id = models.CharField(max_length = 255)
	event_time = UnixTimeStampField(use_numeric=True,default=0)
	facility = models.CharField(max_length = 255)
	deviceid = models.CharField(max_length = 255)
	areaid = models.CharField(max_length = 255)
	icao_code = models.CharField(max_length = 255)
	actual_value = models.IntegerField()
	threshold_value = models.IntegerField()
	state = models.CharField(max_length = 255)


class boardingday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	count_used = models.IntegerField()
	count_unused = models.IntegerField()
	total_count = models.IntegerField()
	pct_utilization = models.FloatField()

	def __str__(self):
		return self._id

class boardinghour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	count_used = models.IntegerField()
	count_unused = models.IntegerField()
	total_count = models.IntegerField()
	pct_utilization_usedseats = models.FloatField()
	def __str__(self):
		return self._id

class boardtop3utilization(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	rank = models.IntegerField()
	pct_utilization = models.FloatField()	

	def __str__(self):
		return self._id

class cbavgday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	avg_opr_allconveyorbelts_min = models.FloatField()
	
	def __str__(self):
		return self._id

class cbavghour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)

	def __str__(self):
		return self._id

class cbperutilday(models.Model):
	_id = models.CharField(max_length = 255)
	cb_id = models.CharField(max_length = 255)
	pct_opr_allconveyorbelts = models.FloatField()
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	
	def __str__(self):
		return self._id

class cbperutilhour(models.Model):
	_id = models.CharField(max_length = 255)
	cb_id = models.CharField(max_length = 255)
	pct_opr_allconveyorbelts = models.FloatField()
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	
	def __str__(self):
		return self._id

class cbtop3utilization(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	rank = models.IntegerField()
	pct_utilization = models.FloatField()

	def __str__(self):
		return self._id

class fbavgutilday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	rating_for_service = models.FloatField()
	service_id  = models.IntegerField()
	def __str__(self):
		return self._id

class fbavgutilsnapshot(models.Model):
	_id = models.CharField(max_length = 255)
	icao_code = models.CharField(max_length = 255)
	rating_for_service = models.FloatField()
	service_id  = models.IntegerField()
	
	def __str__(self):
		return self._id

class fbtop3utilization(models.Model):
	_id = models.CharField(max_length = 255)
	icao_code = models.CharField(max_length = 255)
	service_id  = models.IntegerField()
	rating_for_service = models.FloatField()
	rank = models.IntegerField()
	
	def __str__(self):
		return self._id

class kioskday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	pct_utilization = models.FloatField()
	count_of_visits = models.IntegerField()
	count_of_devices = models.IntegerField()
	
	def __str__(self):
		return self._id

class kioskhour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	count_of_visits = models.IntegerField()
	count_of_devices = models.IntegerField()
	pct_utilization = models.FloatField()
	
	def __str__(self):
		return self._id

class kiosktop3utilization(models.Model):

	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	rank = models.IntegerField()
	pct_utilization = models.FloatField()
	def __str__(self):
		return self._id

class parkingday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	pct_utilization = models.FloatField()
	count_of_occupancy = models.IntegerField()
	count_of_devices = models.IntegerField()

	def __str__(self):
		return self._id

class parkingkhour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	count_of_occupancy = models.IntegerField()
	count_of_slots = models.IntegerField()
	pct_utilization = models.FloatField()
	
	def __str__(self):
		return self._id

class parkingtop3utilization(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	rank = models.IntegerField()
	pct_utilization = models.FloatField()
	
	def __str__(self):
		return self._id

class sncalcday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	areaid = models.CharField(max_length = 255)
	count_dispenses = models.IntegerField()
	no_of_containers = models.IntegerField()
	refills = models.FloatField()
	avg_dispenses = models.FloatField()
	
	def __str__(self):
		return self._id

class sncalchour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	areaid = models.CharField(max_length = 255)
	hour = models.IntegerField()
	count_dispenses = models.IntegerField()
	no_of_containers = models.IntegerField()
	refills = models.FloatField()
	avg_dispenses = models.FloatField()
	
	def __str__(self):
		return self._id


class sntop3utilization(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	areaid = models.CharField(max_length = 255)
	rank = models.IntegerField()
	avg_dispenses = models.FloatField()
	hour = models.IntegerField()
	
	def __str__(self):
		return self._id

class trolleycalcday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	pct_utilization = models.FloatField()
	count_unused = models.IntegerField()
	count_used = models.IntegerField()
	total_count = models.IntegerField()
	
	def __str__(self):
		return self._id

class trolleycalchour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	pct_utilization = models.FloatField()
	count_unused = models.IntegerField()
	count_used = models.IntegerField()
	total_count = models.IntegerField()
	
	def __str__(self):
		return self._id

class trolleytop3utilization(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	rank = models.IntegerField()
	pct_utilization = models.FloatField()
	
	def __str__(self):
		return self._id

class wifiday(models.Model):
	_id = models.CharField(max_length = 255)
	avg_utilization_min = models.FloatField()
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	total_download = models.FloatField()
	total_upload = models.FloatField()
	total_used_minutes = models.IntegerField()
	total_unique_users = models.IntegerField()
	
	
	def __str__(self):
		return self._id

class wifihour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	total_download = models.FloatField()
	total_upload = models.FloatField()
	total_used_minutes = models.IntegerField()
	total_unique_users = models.IntegerField()
	avg_utilization_min = models.FloatField()
	
	def __str__(self):
		return self._id

class wifitop3utilization(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	rank = models.IntegerField()
	avg_utilization_min = models.FloatField()
	
	def __str__(self):
		return self._id
