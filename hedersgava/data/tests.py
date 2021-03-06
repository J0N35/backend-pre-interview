from rest_framework.test import APITestCase
import pytest
from rest_framework import status
from pytz import timezone
import json
from .models import RecordLog
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
class TestAPI(APITestCase):
    def setUp(self):
        RecordLog.objects.create(
            device_id="G3112",
            device_type="Temperature Sensor",
            value=14.0524,
            datetime=datetime.fromtimestamp(1008910273),
            log_id=2314
        )
        RecordLog.objects.create(
            device_id="SGB-11232",
            device_type="Current Meter",
            value=25.253,
            datetime=datetime.fromtimestamp(1008910273),
            log_id=2314
        )
        RecordLog.objects.create(
            device_id="SGB-11232",
            device_type="Current Meter",
            value=30.123,
            datetime=datetime.fromtimestamp(1008912222),
            log_id=2320
        )

    def test_01_post_success(self):
        response = self.client.post('/data/',
                                    xml_data,
                                    content_type='application/xml')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecordLog.objects.count(), 9)

    def test_02_get_log(self):
        response = self.client.get('/data/1008910273/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        _test_time = datetime.fromtimestamp(1008910273, tz=timezone('Asia/Hong_Kong'))
        _test_time = _test_time.isoformat()
        expected = json.dumps([
            {"datetime": _test_time,
             "value": 14.0524,
             "unit": "°C"},
            {"datetime": _test_time,
             "value": 25.253,
             "unit": "A"},
        ])
        actual = json.dumps(json.loads(response.content.decode('utf-8')))
        self.assertEqual(actual, expected)

    def test_03_get_log_no_result(self):
        response = self.client.get('/data/1008910555/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = json.dumps([])
        actual = json.dumps(json.loads(response.content.decode('utf-8')))
        self.assertEqual(actual, expected)
