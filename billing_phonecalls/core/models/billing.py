""" This module contains the model to bill """
from django.db import models
from billing_phonecalls.core.pricing import PriceGenerator


class BillManager(models.Manager):
    """ manager class to bill model """

    def create_bill(self, call_instance):
        """ create bill or return old record """
        old_record = self.filter(call=call_instance)
        if old_record.exists():
            return old_record.get()

        price_generator = PriceGenerator(call_instance)
        return self.create(
            call=call_instance,
            price=price_generator.calculate_price()
        )


class Bill(models.Model):
    """ Bill model """

    call = models.OneToOneField('core.Call', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    objects = BillManager()

    class Meta:
        """ Meta """
        verbose_name = 'Bill'
        verbose_name_plural = 'Billing'

    def __str__(self):
        """ str method to class  """
        return 'call_id: %s - price: %s' % (
            self.call, self.price)

    @property
    def total_minutes(self):
        """ Return total minuts of call """
        minutes, _ = divmod(self.call.duration.total_seconds(), 60)
        return int(minutes)
