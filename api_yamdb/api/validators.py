import datetime as dt

from django.core.exceptions import ValidationError


def my_year_validator(value):
    if value > dt.datetime.now().year:
        raise ValidationError(('%(value)s is not a correct year!'),
                              params={'value': value},)
