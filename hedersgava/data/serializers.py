from rest_framework import serializers
from .models import Device, ValueLog

class DeviceSerializers(serializers.Serializer):
    device_id = serializers.CharField(max_length=10)
    device_type = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Device.objects.create(**validated_data)

    def update(self, validated_data):
        return Device.objects.get_or_create(
            device_id=validated_data.get('device_id', None),
            device_type=validated_data.get('device_type', None)
        )


class LogSerializers(serializers.Serializer):
    device_id = serializers.CharField(max_length=10)
    device_value = serializers.FloatField()
    log_datetime = serializers.DateTimeField()
    log_id = serializers.IntegerField()

    def create(self, validated_data):
        return ValueLog.objects.create(**validated_data)

    def update(self, validated_data):
        return ValueLog.objects.get_or_create(
            device_id_id=validated_data.get('device_id', None),
            device_value=validated_data.get('device_value', None),
            log_id=validated_data.get('log_id', None),
            log_datetime=validated_data.get('log_datetime', None)
        )
