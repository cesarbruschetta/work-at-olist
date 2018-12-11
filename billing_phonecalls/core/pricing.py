""" module to generate pricing of calls """
from time import time
from datetime import datetime, timedelta
from decimal import Decimal

from .models.price import Price


class PriceGenerator:
    """ Class to calculator price of call """

    fixed_charge = None
    call_price = 0
    call = None
    call_start = datetime.now()
    call_end = datetime.now()

    STD_HOUR_START = time()
    STD_HOUR_END = time()
    STD_FIXED_CHARGE = 0.0
    STD_PERIODIC_CHARGE = 0.0

    RDC_HOUR_START = time()
    RDC_HOUR_START_HOUR_END = time()
    RDC_FIXED_CHARGE = 0.0
    RDC_PERIODIC_CHARGE = 0.0

    def __init__(self, call_instance):
        """ init attributes of call_instance in class """

        self.call = call_instance
        self.call_start = call_instance.start_time
        self.call_end = call_instance.end_time

        std_price = Price.objects.get_standard_price()
        rdc_price = Price.objects.get_reduced_price()

        self.STD_HOUR_START = std_price.start_period
        self.STD_HOUR_END = std_price.end_period
        self.STD_FIXED_CHARGE = std_price.fixed_charge
        self.STD_PERIODIC_CHARGE = std_price.periodic_charge

        self.RDC_HOUR_START = rdc_price.start_period
        self.RDC_HOUR_START_HOUR_END = rdc_price.end_period
        self.RDC_FIXED_CHARGE = rdc_price.fixed_charge
        self.RDC_PERIODIC_CHARGE = rdc_price.periodic_charge

    def total_minutes_of_call(self):
        """ Return total of minutes in call """
        minutes, _ = divmod(self.call.duration.total_seconds(), 60)
        return int(minutes)

    def standard_minutes(self):
        """ return minutes in stardard time price  """
        record_start = self.call_start.replace(second=0, microsecond=0)
        t_minutes = self.total_minutes_of_call()

        std_start = self.STD_HOUR_START
        std_end = self.STD_HOUR_END

        minutes = 0
        for _ in range(t_minutes):
            cond_1 = std_start <= record_start.time() < std_end
            # excluding end_limit
            cond_2 = (record_start + timedelta(minutes=1)).time() < std_end
            if all([cond_1, cond_2]):
                minutes += 1
            record_start += timedelta(minutes=1)
        return minutes

    def standing_charge(self):
        """ set of change default by call """
        record_start = self.call_start
        std_start_hour = self.STD_HOUR_START
        std_end_hour = self.STD_HOUR_END

        if std_start_hour.hour <= record_start.hour < std_end_hour.hour:
            st_charge = self.STD_FIXED_CHARGE
        else:
            st_charge = self.RDC_FIXED_CHARGE
        return st_charge

    def calculate_price(self):
        """ method to calculate price total of call """
        standard_minutes = self.standard_minutes()
        reduced_minutes = self.total_minutes_of_call() - standard_minutes

        std_minute_charge = self.STD_PERIODIC_CHARGE
        rdc_minute_charge = self.RDC_PERIODIC_CHARGE
        std_price = (Decimal(standard_minutes) * Decimal(std_minute_charge))
        rdc_price = Decimal(reduced_minutes) * Decimal(rdc_minute_charge)

        standing_charge = self.standing_charge()

        total = std_price + rdc_price + Decimal(standing_charge)
        return total.quantize(Decimal('0.01'))
