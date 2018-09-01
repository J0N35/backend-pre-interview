from django.db import models


class Device(models.Model):
    device_id = models.TextField(primary_key=True)
    device_type = models.TextField()


class ValueLog(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    date = models.DateTimeField()
    value = models.IntegerField()
