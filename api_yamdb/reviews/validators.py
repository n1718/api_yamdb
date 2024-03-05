# import datetime

# from django.core.validators import MaxValueValidator

import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    year = dt.date.today().year
    if value > year:
        raise ValidationError('Этот год еще не наступил.')
    return value
