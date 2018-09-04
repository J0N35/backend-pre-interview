from rest_framework import serializers
from .models import RecordLog


class LogListS(serializers.ListSerializer):
    def create(self, validated_data):
        for entry in validated_data:
            RecordLog.objects.update_or_create(**entry)


class LogSerializers(serializers.ModelSerializer):
    class Meta:
        model = RecordLog
        list_serializer_class = LogListS
        fields = ('datetime', 'value', 'log_id', 'device_id', 'device_type')


class ListLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = RecordLog
        fields = ('datetime', 'value', 'unit')
