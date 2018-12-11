""" module to test views to api """
from datetime import datetime, timedelta
from rest_framework.test import APITestCase

from billing_phonecalls.core.models.phone_calls import Call, CallEvent
from billing_phonecalls.core.utils import generate_numbers


class TestRegisterCallView(APITestCase):
    """ Teste to register call in API """

    fixtures = ['data_calls.json']
    
    def setUp(self):
        """ Set Up test """
    
        self.call_id = generate_numbers(2)
        self.source = 11988442211
        self.destination = 11998776622
        self.date = datetime.now().replace(hour=12, minute=0)

    def test_register_start_call(self):
        """ teste to method register call in api """

        data = {
          "type":  "start",
          "timestamp": self.date,
          "call_id":  self.call_id,
          "source":  self.source,
          "destination": self.destination
        }

        resp = self.client.post("/api/call", data=data)
        self.assertEqual(resp.status_code, 201)

    def test_register_end_call(self):
        """ teste to method register end of call in api """
        
        call = Call.objects.create(**{
            "call_id": self.call_id,
            "source": self.source,
            "destination": self.destination,
        })
        CallEvent.objects.create(
            call_id=call,
            type_call="start",
            timestamp=self.date
        )

        data = {
          "type":  "end",
          "timestamp": self.date + timedelta(minutes=2),
          "call_id":  self.call_id
        }

        resp = self.client.post("/api/call", data=data)
        self.assertEqual(resp.status_code, 201)

    def test_register_start_call_not_destination(self):
        """ teste to method register call in api not destination """

        data = {
          "type":  "start",
          "timestamp": self.date,
          "call_id":  self.call_id,
          "source":  self.source
        }

        resp = self.client.post("/api/call", data=data)
        self.assertEqual(resp.status_code, 400)

        data = resp.json()
        self.assertEqual(data['non_field_errors'][0], "This field is required when type is \"start\"")

    def test_register_start_call_not_source(self):
        """ teste to method register call in api not source """

        data = {
          "type":  "start",
          "timestamp": self.date,
          "call_id":  self.call_id,
          "destination":  self.destination
        }

        resp = self.client.post("/api/call", data=data)
        self.assertEqual(resp.status_code, 400)
    
        data = resp.json()
        self.assertEqual(data['non_field_errors'][0], "This field is required when type is \"start\"")
    
    def test_register_start_call_repeat(self):
        """ teste to method register call in api repeat start """

        call = Call.objects.create(**{
            "call_id": self.call_id,
            "source": self.source,
            "destination": self.destination,
        })
        CallEvent.objects.create(
            call_id=call,
            type_call="start",
            timestamp=self.date
        )

        data = {
          "type":  "start",
          "timestamp": self.date,
          "call_id":  self.call_id,
          "source": self.source,
          "destination":  self.destination
        }

        resp = self.client.post("/api/call", data=data)
        self.assertEqual(resp.status_code, 400)

        data = resp.json()
        self.assertIn("This call have is event type", data)


class TestTelephoneBillApi(APITestCase):
    """ Teste to telephone bill in API """

    fixtures = ['data_calls.json']
    
    
    def test_get_billing(self):
        """ teste to get call of last period """
        
        resp = self.client.get("/api/billing/99988526423/")
        self.assertEqual(resp.status_code, 200)
        
        data = resp.json()
        self.assertEqual(data['calls'], [])
        
    def test_get_billing_by_period(self):
        """ teste to get call of period """
        
        resp = self.client.get("/api/billing/99988526423/", 
                               {'year':2017, 'month':12})
        self.assertEqual(resp.status_code, 200)
        
        data = resp.json()
        self.assertEqual(len(data['calls']), 6)
        
    def test_get_billing_by_period_invalid(self):
        """ teste to get call of period invalid"""
        today = datetime.today()
        
        resp = self.client.get("/api/billing/99988526423/", 
                               {'year':today.year, 'month':today.month})
        self.assertEqual(resp.status_code, 400)
        
        data = resp.json()
        print(data)
        self.assertEqual(data['detail'], "Period is invalid, period not closed.")
        