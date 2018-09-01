from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['POST'])
def input_data(request):
    """
    Request XML data and insert into DB
    """
    if request.method == 'POST':
        input_content = request.data
        if input_content:
            # validate XML
            # parse XML
            # insert into DB
            return Response(input_content, status=status.HTTP_200_OK, content_type=request.content_type)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_data(request, log_id):
    """
    Return specify log with corresponding id
    """
    if request.method == 'GET':
        # log_id = request.log_id
        return Response(log_id, status=status.HTTP_200_OK, content_type=request.content_type)
