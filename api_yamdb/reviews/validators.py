from datetime import date
import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_year_title(value):
    """Валидатор проверки года выпуска произведения."""
    current_year = date.today().year
    if value > current_year:
        raise ValidationError(
            f'Год выпуска произведения ({value}) не должен '
            f'быть больше текущего года ({current_year}).'
        )
    return value


def validate_username(username):
    if username == settings.USER_PROFILE_PATH:
        raise ValidationError(
            f'Логин не может принимать значение "{settings.USER_PROFILE_PATH}"'
        )
    username_pattern = r'^[\w.@+-]+\Z'
    if not re.match(username_pattern, username):
        invalid_chars = ''.join(
            [char for char in username if not re.match(username_pattern, char)]
        )
        raise ValidationError(
            'Некорректный логин. Логин не должен содержать символы:'
            f'{invalid_chars} .'
        )
    return username
