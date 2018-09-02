from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer
from .serializers import DeviceSerializers, LogSerializers
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


def _device_data_parser(content):
    """
    parse device data -> check and insert into DB
    :param content: device_data dict
    :return: bool if the data is inserted into DB
    """
    return_code = False
    for key, value in content.items():
        device_data = {
            'device_id': key,
            'device_type': value
        }
        serializer = DeviceSerializers(data=device_data)
        if serializer.is_valid():
            serializer.update(serializer.validated_data)
            return_code = True
        else:
            return_code = False
            break
    return return_code


def _value_data_parser(content, log_id, log_datetime):
    """
    parse log data -> check and insert into DB
    :param content: log_data list
    :return: bool if the data is inserted into DB
    """
    return_code = False
    for item in content:
        value_data = {
            'device_id': item.get('device', None),
            'device_value': item.get('value', None),
            'log_id': int(log_id),
            'log_datetime': datetime.fromtimestamp(log_datetime).isoformat()
        }
        serializer = LogSerializers(data=value_data)
        if serializer.is_valid():
            serializer.update(serializer.validated_data)
            return_code = True
        else:
            return_code = False
            break
    return return_code

@api_view(['POST'])
@parser_classes((CustomizedXMLParser,))
def input_data(request):
    """
    Request XML data and insert into DB
    """
    if request.method == 'POST':
        input_content = CustomizedXMLParser().parse(request)
        log_id = input_content.get('id')
        log_datetime = input_content.get('record_time')
        # handle device data
        if not _device_data_parser(input_content['devices']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # handle Log Data
        if not _value_data_parser(input_content['data'], log_id, log_datetime):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(input_content,
                        status=status.HTTP_200_OK,
                        content_type=request.content_type)


@api_view(['GET'])
def get_data(request, log_id):
    """
    Return specify log with corresponding id
    """
    if request.method == 'GET':
        # log_id = request.log_id
        return Response(log_id, status=status.HTTP_200_OK, content_type=request.content_type)


