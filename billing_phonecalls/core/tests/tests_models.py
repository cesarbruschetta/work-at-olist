""" test to models  """
import random
from decimal import Decimal
from datetime import datetime, timedelta
from django.test import TestCase

from billing_phonecalls.core.models.phone_calls import Call, CallEvent
from billing_phonecalls.core.utils import generate_numbers


class CallModelTests(TestCase):

    fixtures = ['data_calls.json']

    def setUp(self):
        """ Set Up test """

        self.call_id = generate_numbers(2)
        self.source = generate_numbers(10)
        self.destination = generate_numbers(10)

        self.call = Call.objects.create(**{
            "call_id": self.call_id,
            "source": self.source,
            "destination": self.destination,
        })
        now = datetime.now().replace(hour=12, minute=0)
        CallEvent.objects.create(
            call_id=self.call,
            type_call="start",
            timestamp=now
        )
        CallEvent.objects.create(
            call_id=self.call,
            type_call="end",
            timestamp=(now + timedelta(minutes=2))
        )

    def test_start_time(self):
        """test start time of call """
        self.assertEqual(self.call.start_time.hour, 12)

    def test_end_time(self):
        """test end time of call """
        self.assertEqual(self.call.end_time.hour, 12)

    def test_duration(self):
        """test duration of call """
        self.assertEqual(self.call.duration.seconds, 2 * 60)

    def test_format_duration(self):
        """test fromat duration of call """
        self.assertEqual(self.call.format_duration, "0h2m0s")

    def test_price(self):
        """test price of call """
        self.assertEqual(self.call.price, Decimal(0.54).quantize(Decimal('0.01')))

    def test_valid_type(self):
        """test valid time of call """
        self.assertFalse(self.call.valid_type('start'))


class InvalidCallModelTests(TestCase):

    fixtures = ['data_calls.json']

    def setUp(self):
        """ Set Up test """

        self.call_id = generate_numbers(2)
        self.source = generate_numbers(10)
        self.destination = generate_numbers(10)

        self.call = Call.objects.create(**{
            "call_id": self.call_id,
            "source": self.source,
            "destination": self.destination,
        })

    def test_start_time(self):
        """test start time of call """
        self.assertFalse(self.call.start_time)

    def test_end_time(self):
        """test end time of call """
        self.assertFalse(self.call.end_time)
