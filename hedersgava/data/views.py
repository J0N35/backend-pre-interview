from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_xml.parsers import XMLParser

from .models import RecordLog
from .serializers import ListLogSerializers
from .serializers import LogSerializers


class CustomizedXMLParser(XMLParser):
    def _xml_convert(self, element):
        """
                convert the xml `element` into the corresponding python object
                """
        list_item_tag = [
            "list_item",
            "element"
        ]
        children = list(element)

        if len(children) == 0:
            return self._type_convert(element.text)
        else:
            # if the fist child tag is list-item
            # means all children are list-item
            if children[0].tag in list_item_tag:
                data = []
                for child in children:
                    data.append(self._xml_convert(child))
            else:
                data = {}
                for child in children:
                    data[child.tag] = self._xml_convert(child)
        return data


class DataViewSet(viewsets.ModelViewSet):
    queryset = RecordLog.objects.all()
    serializer_class = LogSerializers
    parser_classes = (CustomizedXMLParser,)

    def create(self, request, *args, **kwargs):
        record_id = request.data.get('id', None)
        record_datetime = request.data.get('record_time', None)
        record_value = request.data.get('data', None)
        devices = request.data.get('devices', None)
        for entry in record_value:
            entry['device_id'] = entry['device']
            entry['device_type'] = devices.get(entry['device'], None)
            entry['log_id'] = record_id
            entry['datetime'] = datetime.fromtimestamp(record_datetime)

        _records = LogSerializers(data=record_value, many=True)
        if _records.is_valid():
            _records.create(_records.validated_data)

            return Response(
                data=_records.validated_data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, *args, **kwargs):
        timestamp = kwargs.get('pk')
        try:
            timestamp = datetime.fromtimestamp(int(timestamp))
        except Exception:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        instance = self.queryset.filter(datetime=timestamp)
        deserializer = ListLogSerializers(instance, many=True)
        return Response(deserializer.data)
