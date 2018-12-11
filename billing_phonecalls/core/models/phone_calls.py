""" module to model of call and callEvent """
from django.db import models
from django.db.models.signals import post_save
from django.core.validators import MaxLengthValidator
from django.dispatch import receiver

from billing_phonecalls.core.utils import validate_phone
from .billing import Bill


class CallManager(models.Manager):
    """ manager class to Call model """

    def get_telephone_bill(self, telephone, year, month):
        """ return list of calls by period  """
        result = self.filter(source=telephone,
                             callevent__type_call="end",
                             callevent__timestamp__month=month,
                             callevent__timestamp__year=year)

        return result


class Call(models.Model):
    """ model of calls """

    call_id = models.IntegerField("Call Identifier", default=0)
    source = models.CharField("Source Phone", max_length=15,
                              validators=[validate_phone,
                                          MaxLengthValidator(15)])
    destination = models.CharField("Destination Phone", max_length=15,
                                   validators=[validate_phone,
                                               MaxLengthValidator(15)])

    objects = CallManager()

    def __str__(self):
        """ Str class """
        return "class_id: %s, Source: %s - Destination: %s" % (
            self.call_id, self.source, self.destination
        )

    @property
    def start_time(self):
        """ propert to return start time of call """
        record = self.callevent_set.filter(type_call="start").first()
        if record:
            return record.timestamp
        return None

    @property
    def end_time(self):
        """ propert to return end time of call """
        record = self.callevent_set.filter(type_call="end").last()
        if record:
            return record.timestamp
        return None

    @property
    def duration(self):
        """ propert to return duration of call """
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def format_duration(self):
        """ retunr duration of call in string format """
        total_sec = int(self.duration.total_seconds())
        hours, rem = divmod(total_sec, 60 * 60)
        minutes, seconds = divmod(rem, 60)
        return '%sh%sm%ss' % (hours, minutes, seconds)

    @property
    def price(self):
        """ propert to return price of call """
        return self.bill.price

    def valid_type(self, type_call):
        """ method to validate type to call """
        record = self.callevent_set.filter(type_call=type_call)
        return not record.exists()

    class Meta:
        """ Meta """
        verbose_name = 'Call'
        verbose_name_plural = 'Calls'


class CallEvent(models.Model):
    """ model to call event """

    CALL_START = "start"
    CALL_END = "end"
    EVENT_TYPES = [
        (CALL_START, 'Start Call'),
        (CALL_END, 'End Call'),
    ]

    call_id = models.ForeignKey(Call, on_delete=models.CASCADE)
    type_call = models.CharField(max_length=10, choices=EVENT_TYPES)
    timestamp = models.DateTimeField()

    class Meta:
        """ meta """
        unique_together = ("call_id", "type_call")
        ordering = ('timestamp',)
        verbose_name = 'Call Event'
        verbose_name_plural = 'Call Events'


@receiver(post_save, sender=CallEvent)
def create_bill(sender, instance, created, **kwargs):
    """
    On post save of a end call evente, a bill created
    """
    if created and instance.type_call == CallEvent.CALL_END:
        Bill.objects.create_bill(call_instance=instance.call_id)
