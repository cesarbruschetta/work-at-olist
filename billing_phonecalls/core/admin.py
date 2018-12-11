""" Admin Core """
from django.contrib import admin

from .models.billing import Bill
from .models.price import Price
from .models.phone_calls import Call, CallEvent


# Register your models here.
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """ Admin class to Price """

    list_display = ("type_price", 'fixed_charge', 'periodic_charge',
                    'start_period', 'end_period')


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    """ Admin class to Call """

    class CallEventInline(admin.TabularInline):
        """ CallEvent inline admin """
        model = CallEvent
        extra = 0

    class BillInline(admin.TabularInline):
        """ Folder Bookmark inline admin """
        model = Bill
        extra = 0

    inlines = [CallEventInline, BillInline]
    list_display = ("__str__", "duration", "price")
