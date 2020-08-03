from djongo import models


class boardingday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	pct_utilization_usedseats = models.FloatField()
	avg_utilization_usedseats = models.FloatField()

	def __str__(self):
		return self._id

class boardinghour(models.Model):
	_id = models.CharField(max_length = 255)
	avg_utilization_usedseats = models.FloatField()
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	pct_utilization_usedseats = models.FloatField()

	def __str__(self):
		return self._id

class cbavgday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	avg_opr_allconveyorbelts = models.FloatField()

	def __str__(self):
		return self._id


class cbavghour(models.Model):
	_id = models.CharField(max_length = 255)
	avg_opr_allconveyorbelts = models.FloatField()
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	
	def __str__(self):
		return self._id

class cbperutilday(models.Model):
	_id = models.CharField(max_length = 255)
	cb_id = models.CharField(max_length = 255)
	pct_opr_eachconveyorbelt = models.FloatField()
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)

	def __str__(self):
		return self._id


class cbperutilhour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	cb_id = models.CharField(max_length = 255)
	pct_opr_eachconveyorbelt = models.FloatField()

	def __str__(self):
		return self._id


class kioskday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	pct_utilization_day = models.FloatField()
	
	def __str__(self):
		return self._id

class kioskpeakperiod(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	num_of_visits = models.IntegerField()

	def __str__(self):
		return self._id


class parkavgduration(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	slotid = models.CharField(max_length = 255)
	def __str__(self):
		return self._id

class parkday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	available_slots = models.IntegerField()
	pct_occupied_slots = models.FloatField()
	
	def __str__(self):
		return self._id

class parkhour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	available_slots = models.IntegerField()
	pct_occupied_slots = models.FloatField()
	
	def __str__(self):
		return self._id

class parkpeakperiod(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	hour = models.IntegerField()
	used_slots = models.IntegerField()
	maxused_time = models.FloatField()

	def __str__(self):
		return self._id

class snareautilday(models.Model):
	_id = models.CharField(max_length = 255)
	areaid = models.CharField(max_length = 255)
	pct_areawise_util = models.FloatField()
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)

	def __str__(self):
		return self._id

class snareautilhour(models.Model):
	_id = models.CharField(max_length = 255)
	areaid = models.CharField(max_length = 255)
	pct_areawise_util = models.FloatField()
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	
	def __str__(self):
		return self._id

class snmaxconsume(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	max_dispenses = models.IntegerField()
	
	def __str__(self):
		return self._id

class sntotalconsumeday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	total_dispenses = models.IntegerField()
	
	def __str__(self):
		return self._id

class sntotalconsumehour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	total_dispenses = models.IntegerField()
	
	def __str__(self):
		return self._id

class trolleycalcday(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	pct_utilization_usedtrolley = models.FloatField()
	icao_code = models.CharField(max_length = 255)
	unused_trolleys = models.IntegerField()
	used_trolleys = models.IntegerField()

	
	def __str__(self):
		return self._id

class trolleycalchour(models.Model):
	_id = models.CharField(max_length = 255)
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	pct_utilization_usedtrolley = models.FloatField()
	unused_trolleys = models.IntegerField()
	used_trolleys = models.IntegerField()
	
	def __str__(self):
		return self._id

class wifiday(models.Model):
	_id = models.CharField(max_length = 255)
	avg_utilization = models.FloatField()
	date = models.DateField()
	icao_code = models.CharField(max_length = 255)
	total_download = models.FloatField()
	total_upload = models.FloatField()
	total_used_minutes =models.IntegerField()
	total_users = models.IntegerField()
	
	def __str__(self):
		return self._id

class wifihour(models.Model):
	_id = models.CharField(max_length = 255)
	avg_utilization = models.FloatField()
	date = models.DateField()
	hour = models.IntegerField()
	icao_code = models.CharField(max_length = 255)
	total_download = models.FloatField()
	total_upload = models.FloatField()
	total_used_minutes = models.IntegerField()
	total_users = models.IntegerField()
	def __str__(self):
		return self._id

	
