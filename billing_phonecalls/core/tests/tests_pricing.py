""" test to pricing generator  """
import random
from decimal import Decimal
from datetime import datetime, timedelta
from django.test import TestCase

from billing_phonecalls.core.models.phone_calls import Call, CallEvent
from billing_phonecalls.core.utils import generate_numbers
from billing_phonecalls.core.pricing import PriceGenerator


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
    
    def test_calculate_price(self):
        """ test to calcule price of PriceGenerator class """
        
        price_generator = PriceGenerator(self.call)
        price = price_generator.calculate_price()
        self.assertEqual(price, Decimal(0.54).quantize(Decimal('0.01')))
                
                