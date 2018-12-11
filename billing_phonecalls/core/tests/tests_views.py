""" module to test views to api """
from datetime import datetime
from rest_framework.test import APITestCase

from billing_phonecalls.core.utils import generate_numbers


class TestRegisterCallView(APITestCase):
    """ Teste to register call in API """

    fixtures = ['data_users.json']
    
    def setUp(self):
        """ Set Up test """
    
        self.call_id = '20'
        self.source = 119988442211
        self.destination = 1199776622
        self.date = datetime.now().replace(hour=12, minute=0)

    def test_register_start_call(self):
        """ teste to method get in api """

        data = {
          "type":  "start",
          "timestamp": self.date,
          "call_id":  self.call_id,
          "source":  self.source,
          "destination": self.destination
        }

        resp = self.client.post("/api/call", data=data)
        self.assertEqual(resp.status_code, 200)
