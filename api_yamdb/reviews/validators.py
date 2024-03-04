import datetime

from django.core.validators import MaxValueValidator

from django.core.exceptions import ValidationError


def validate_year(value):

    def current_year():
        return datetime.date.today().year

    return MaxValueValidator(current_year())(value)


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя использовать "me" в качестве имени пользователя'
        )
