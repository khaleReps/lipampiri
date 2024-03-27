from django.db import models

class LogBook(models.Model):
    vehicle_reg = models.CharField(max_length=20)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    speedometer_reading = models.FloatField()
    km = models.FloatField()
    detail_of_journey = models.TextField()
    order_no = models.CharField(max_length=50)
    driver_signature = models.CharField(max_length=100)
    litres_petrol = models.FloatField()
    militres_oil = models.FloatField()
    remarks = models.TextField()
