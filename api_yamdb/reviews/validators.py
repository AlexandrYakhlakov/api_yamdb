from datetime import date
import re

from django.core.exceptions import ValidationError

from reviews.constants import USER_PROFILE_PATH


def validate_year(value):
    """Валидатор проверки года выпуска произведения."""
    if value > date.today().year:
        raise ValidationError(
            'Год выпуска не должен быть больше текущего года.'
        )
    return value


def validate_username(username):
    if username == USER_PROFILE_PATH:
        raise ValidationError(
            f'Логин не может принимать значение "{USER_PROFILE_PATH}"'
        )
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise ValidationError(
            (
                'Некорректный логин. Логин может содержать только символы из'
                ' набора: латинские буквы, цифры, знак подчёркивания, точка,'
                ' @, +, пробел.'
            )
        )
    return username
