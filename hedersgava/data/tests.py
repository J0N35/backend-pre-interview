from django.test import TestCase
import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient, RequestsClient
from hypothesis import strategies as st
from string import printable
from hypothesis import given
from dicttoxml import dicttoxml
import json
from .views import input_data

xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<root>
   <data>
      <element>
         <device>SGD-12344</device>
         <value>1234.266</value>
      </element>
      <element>
         <device>SGB-11233</device>
         <value>60</value>
      </element>
      <element>
         <device>SCC-525</device>
         <value>220</value>
      </element>
      <element>
         <device>SGC-1552</device>
         <value>5266.66</value>
      </element>
      <element>
         <device>SGB-11233</device>
         <value>440</value>
      </element>
      <element>
         <device>G3112</device>
         <value>32.266</value>
      </element>
      <element>
         <device>SGD-12344</device>
         <value>1234.266</value>
      </element>
   </data>
   <devices>
      <G3112>Temperature Sensor</G3112>
      <SCC-525>Voltage Meter</SCC-525>
      <SGB-11233>Current Meter</SGB-11233>
      <SGC-1552>Power Meter</SGC-1552>
      <SGD-12344>Power Meter</SGD-12344>
   </devices>
   <id>2314</id>
   <record_time>1008910273</record_time>
</root>"""


class GetLog(TestCase):
    def setUpTestData(cls):
        pass
    pass


@pytest.mark.django_db
class PostLog(TestCase):
    factory = APIRequestFactory()
    request = factory.post('/data/', xml_data, content_type='application/xml')
    # client = RequestsClient()
    # response = client.post('/data/', xml_data, content_type='application/xml')
    response = input_data(request)
    pass
