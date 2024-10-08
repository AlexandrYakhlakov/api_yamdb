from datetime import date
import re

from django.core.exceptions import ValidationError

from reviews.constants import USER_PROFILE_PATH


def validate_year_title(value):
    """Валидатор проверки года выпуска произведения."""
    current_year = date.today().year
    if value > current_year:
        raise ValidationError(
            f'Год выпуска произведения ({value}) не должен '
            f'быть больше текущего года ({current_year}).'
        )
    return value


def validate_username(value):
    if value == USER_PROFILE_PATH:
        raise ValidationError('Логин не может принимать значение "me"')
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            (
                'Некорректный логин. Логин может содержать только символы из'
                ' набора: латинские буквы, цифры, знак подчёркивания, точка,'
                ' @, +, пробел.'
            )
        )
