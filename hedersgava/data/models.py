from django.db import models


class Device(models.Model):
    unit_set = {
        'Temperature Sensor': '°C',
        'Voltage Meter': 'V',
        'Current Meter': 'A',
        'Power Meter': 'kWh'
    }

    device_id = models.CharField(primary_key=True, max_length=10)
    device_type = models.CharField(max_length=50)

    @property
    def device_unit(self):
        return self.unit_set[self.device_type.__str__()]


class ValueLog(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    log_datetime = models.DateTimeField()
    log_id = models.IntegerField()
    device_value = models.FloatField()
