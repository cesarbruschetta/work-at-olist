""" This module contains the model to price """
from django.db import models


class PriceManager(models.Manager):
    """ manager to price model """

    def get_standard_price(self):
        """ return standard price of DB """
        return self.get(type_price=self.model.STANDARD_PRICE)

    def get_reduced_price(self):
        """ return reduced price of DB """
        return self.get(type_price=self.model.REDUCED_PRICE)


class Price(models.Model):
    """ Model to price """

    STANDARD_PRICE = "1"
    REDUCED_PRICE = "2"
    PRICE_TYPES = [
        (STANDARD_PRICE, 'Standard time call'),
        (REDUCED_PRICE, 'Reduced tariff time call'),
    ]

    type_price = models.CharField(
        max_length=2,
        choices=PRICE_TYPES,
        unique=True,
        default=STANDARD_PRICE)
    fixed_charge = models.DecimalField('Value fixed by call', max_digits=7, decimal_places=2)
    periodic_charge = models.DecimalField('Value by minute', max_digits=7, decimal_places=2)
    start_period = models.TimeField('Hour of start')
    end_period = models.TimeField('Hour of end')

    objects = PriceManager()

    class Meta:
        """ Meta """
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'
