from rest_framework import serializers
from .models import Device, ValueLog
from django_bulk_update.helper import bulk_update


class DeviceListS(serializers.ListSerializer):
    def create(self, validated_data):
        devices = [Device(**item) for item in validated_data]
        return Device.objects.bulk_create(devices)


class DeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Device
        list_serializer_class = DeviceListS
        fields = (
            'device_id', 'device_type', 'unit'
        )


class LogListS(serializers.ListSerializer):
    def create(self, validated_data):
        for entry in validated_data:
            ValueLog.objects.update_or_create(**entry)


class LogSerializers(serializers.ModelSerializer):
    class Meta:
        model = ValueLog
        list_serializer_class = LogListS
        fields = ('datetime', 'value', 'log_id', 'device_id')

# class LogSerializers(serializers.Serializer):
#     device_id = serializers.CharField(max_length=10)
#     value = serializers.FloatField()
#     datetime = serializers.DateTimeField()
#     log_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return ValueLog.objects.create(**validated_data)
#
#     def update(self, validated_data):
#         return ValueLog.objects.get_or_create(
#             device_id_id=validated_data.get('device_id', None),
#             value=validated_data.get('value', None),
#             log_id=validated_data.get('log_id', None),
#             datetime=validated_data.get('datetime', None)
#         )
#
#
# class GetLogSerializers(serializers.Serializer):
#     datetime = serializers.DateTimeField()
#     value = serializers.FloatField()
#     unit = serializers.CharField(source='device_id')
#
#     def create(self):
#         return
#
#     def update(self):
#         return
