""" module to utils methods """
import random
from datetime import datetime, timedelta
from django.core.validators import RegexValidator


def generate_numbers(size):
    """ generate numbers by size """
    
    return ''.join(
        [str(random.randint(1,9)) for x in range(2)]
    )


def validate_phone(value):
    """ validate phone number """
    return RegexValidator(
        regex=r'^(([1-9]{2})(?:[2-8]|9[1-9])[0-9]{7})$',
        message='Invalid phone number.'
    )(value)


def last_period():
    """ return of last moth and year """

    today = datetime.today()
    last_date = today.replace(day=1) - timedelta(days=1)

    return last_date.year, last_date.month


def valid_period(year, month):
    """ check if year oy month is current period """
    today = datetime.today()

    if year and month and\
            today.year == year and today.month == month:
        return False

    return True
