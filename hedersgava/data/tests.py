from django.test import TestCase
import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from hypothesis import strategies as st
from string import printable
from hypothesis import given
from dicttoxml import dicttoxml
import json
# from .views import input_data
from .models import Device, ValueLog, RecordLog
from datetime import datetime

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


@pytest.mark.django_db
class TestGetMethod(APITestCase):
    def setUp(self):
        RecordLog.objects.create(
            device_id="G3112",
            device_type="Temperature Sensor",
            value=14.0524,
            datetime=datetime.fromtimestamp(1008910273).isoformat(),
            log_id=2314
        )
        RecordLog.objects.create(
            device_id="SGB-11232",
            device_type="Current Meter",
            value=25.253,
            datetime=datetime.fromtimestamp(1008910273).isoformat(),
            log_id=2314
        )
        RecordLog.objects.create(
            device_id="SGB-11232",
            device_type="Current Meter",
            value=30.123,
            datetime=datetime.fromtimestamp(1008912222).isoformat(),
            log_id=2320
        )
        # Device.objects.create(device_id="G3112", )
        # Device.objects.create(device_id="SGB-11233", device_type="Current Meter")
        # ValueLog.objects.create(
        #     device_id_id="SGB-11233",
        #     value=25.253,
        #     datetime=datetime.fromtimestamp(1008910273).isoformat(),
        #     log_id=2314
        # )
        # ValueLog.objects.create(
        #     device_id_id="G3112",
        #     value=14.0524,
        #     datetime=datetime.fromtimestamp(1008911111).isoformat(),
        #     log_id=2318
        # )

    def test_01_post_success(self):
        response = self.client.post('/data/', xml_data, content_type='application/xml')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecordLog.objects.count(), 8)

    def test_02_get_log_by_request(self):
        response = self.client.get('/data/1008910273/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = json.dumps([
            {"datetime": datetime.fromtimestamp(1008910273).isoformat(),
             "value": 14.0524,
             "unit": "°C"},
            {"datetime": datetime.fromtimestamp(1008910273).isoformat(),
             "value": 25.253,
             "unit": "A"},
        ])
        self.assertEqual(response.content, expected)
