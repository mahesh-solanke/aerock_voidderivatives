from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here

# Groups Creation
Admin, created = Group.objects.get_or_create(name='Admin')
AAI, created = Group.objects.get_or_create(name='AAI')
AirportManager, created = Group.objects.get_or_create(name='Airport Manager')
AirportStaff, created = Group.objects.get_or_create(name='Airport Staff')

#Airport Master Table
class airport(models.Model):
    icao_code = models.CharField(max_length=10, unique = 'True')
    iata_code = models.CharField(max_length=10,null ='True',blank='True')
    airport_name = models.TextField(max_length=500)
    state = models.TextField(max_length = 100)
    city = models.TextField(max_length = 100)
    category = models.TextField(max_length= 50, default='000')
    type = models.TextField(max_length = 20)
    active = models.BooleanField(default=True)

#UserAirport Table
class userairport(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    air = models.ForeignKey(airport, on_delete = models.CASCADE)


#Support Table
class support(models.Model):
    email = models.EmailField(max_length=250)
    query = models.TextField(max_length = 500)

#Facility Master Table
class facility(models.Model):
    name = models.TextField(max_length =50)

#Airport-Facility Table
class airportfacility(models.Model):
    air = models.ForeignKey(airport,on_delete=models.CASCADE)
    fac = models.ForeignKey(facility,on_delete=models.CASCADE)
    status = models.BooleanField(default = False)


#Threshold Table
class threshold(models.Model):
    sensor_type = models.TextField(max_length=20)
    threshold_type = models.TextField(max_length = 30)
    threshold_value_high = models.IntegerField()
    threshold_value_low = models.IntegerField()
    capacity = models.IntegerField()
    airfac = models.ForeignKey(airportfacility,on_delete=models.CASCADE)


