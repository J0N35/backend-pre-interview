"""echo api testing
"""
import json
from string import printable

from hypothesis import strategies as st
from hypothesis import given
from django.test import Client

from .views import echo

json_data = st.recursive(
    st.booleans() | st.floats() | st.text(printable),
    lambda children: st.dictionaries(st.text(printable), children)
)


class TestEcho:
    @given(json_data=json_data)
    def test_echo_json_status_result(self, json_data, rf):
        """Testing echo api response status result is function correctly with json data
        """
        data = {'null': json.dumps(json_data)}
        request = rf.post('/echo/', data, content_type='application/json')
        response = echo(request)
        assert response.status_code == 200
        response.render()
        assert response.data == data
