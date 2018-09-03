from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status, viewsets
from rest_framework_xml.parsers import XMLParser
from rest_framework import generics
# from .serializers import DeviceSerializers, LogSerializers, GetLogSerializers
from .serializers import DeviceSerializers
from .models import Device, ValueLog
from .serializers import LogSerializers
from datetime import datetime


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
            # if the fist child tag is list-item means all children are list-item
            if children[0].tag in list_item_tag:
                data = []
                for child in children:
                    data.append(self._xml_convert(child))
            else:
                data = {}
                for child in children:
                    data[child.tag] = self._xml_convert(child)
        return data


# def _device_data_parser(content):
#     """
#     parse device data -> check and insert into DB
#     :param content: device_data dict
#     :return: bool if the data is inserted into DB
#     """
#     return_code = False
#     for key, value in content.items():
#         device_data = {
#             'device_id': key,
#             'device_type': value
#         }
#         serializer = DeviceSerializers(data=device_data)
#         if serializer.is_valid():
#             serializer.update(serializer.validated_data)
#             return_code = True
#         else:
#             return_code = False
#             break
#     return return_code
#
#
# def _value_data_parser(content, log_id, log_datetime):
#     """
#     parse log data -> check and insert into DB
#     :param content: log_data list
#     :return: bool if the data is inserted into DB
#     """
#     return_code = False
#     for item in content:
#         value_data = {
#             'device_id': item.get('device', None),
#             'value': item.get('value', None),
#             'log_id': int(log_id),
#             'datetime': datetime.fromtimestamp(log_datetime).isoformat()
#         }
#         serializer = LogSerializers(data=value_data)
#         if serializer.is_valid():
#             serializer.update(serializer.validated_data)
#             return_code = True
#         else:
#             return_code = False
#             break
#     return return_code
#
#
# @api_view(['POST'])
# @parser_classes((CustomizedXMLParser,))
# def input_data(request):
#     """
#     Request XML data and insert into DB
#     """
#     if request.method == 'POST':
#         input_content = CustomizedXMLParser().parse(request)
#         log_id = input_content.get('id')
#         log_datetime = input_content.get('record_time')
#         # handle device data
#         if not _device_data_parser(input_content['devices']):
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         # handle Log Data
#         if not _value_data_parser(input_content['data'], log_id, log_datetime):
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(input_content,
#                         status=status.HTTP_200_OK,
#                         content_type=request.content_type)


class DataViewSet(viewsets.ModelViewSet):
    queryset = ValueLog.objects.all()
    serializer_class = LogSerializers
    parser_classes = (CustomizedXMLParser,)

    def create(self, request, *args, **kwargs):
        record_id = request.data.get('id', None)
        record_datetime = request.data.get('record_time', None)
        record_value = request.data.get('data', None)
        devices = request.data.get('devices', None)
        is_device_added = False
        is_log_added = False
        # -device list handle-
        device_list = list()
        for key, value in devices.items():
            device_list.append(
                {'device_id': key, 'device_type': value}
            )
        _devices = DeviceSerializers(data=device_list, many=True)
        if _devices.is_valid():
            _devices.create(_devices.validated_data)
            is_device_added = True
        # -log handle-
        for entry in record_value:
            entry['device_id'] = entry['device']
            entry['log_id'] = record_id
            entry['datetime'] = datetime.fromtimestamp(record_datetime)
        _records = LogSerializers(data=record_value, many=True)
        if _records.is_valid():
            _records.create(_records.validated_data)
            is_log_added = True
        # -response-
        if is_device_added and is_log_added:
            return Response(
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ListData(generics.ListAPIView):
    serializer_class = LogSerializers

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        timestamp = self.kwargs['timestamp']
        timestamp = datetime.fromtimestamp(int(timestamp)).isoformat()
        log_result = ValueLog.objects.filter(datetime=timestamp)
        log_result = GetLogSerializers(data=log_result, many=True)
        log_result.is_valid()
        return log_result.data
