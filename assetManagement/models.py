from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    employee_id = models.IntegerField()
    employee_name = models.CharField(max_length=50)
    employee_position = models.CharField(max_length=50)
    employee_comp_name = models.CharField(max_length=50)

class Device(models.Model):
    device_id = models.IntegerField()
    device_model = models.CharField(max_length=50,null=True,blank=True)
    device_type = models.CharField(max_length=50)
    device_condition = models.CharField(max_length=20)
    device_comp_name = models.CharField(max_length=50)
    device_occupied_by = models.IntegerField(default=0)

class DeviceLogInfo(models.Model):
    device_id = models.IntegerField()
    device_comp_name = models.CharField(max_length=50)
    device_occupied_by = models.IntegerField(default=0)
    device_checkout_time = models.DateTimeField()
    device_checkout_condition = models.CharField(max_length=50)
    device_return_back_time = models.DateTimeField(null=True,blank=True)
    device_return_back_condition = models.CharField(max_length=50,null=True,blank=True)
