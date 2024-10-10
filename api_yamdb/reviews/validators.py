from datetime import date
import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_year(year):
    """Валидатор проверки года выпуска произведения."""
    current_year = date.today().year
    if year > current_year:
        raise ValidationError(
            f'Год выпуска произведения ({year}) не должен '
            f'быть больше текущего года ({current_year}).'
        )
    return year


def validate_username(username):
    if username == settings.USER_PROFILE_PATH:
        raise ValidationError(
            f'Логин не может принимать значение "{settings.USER_PROFILE_PATH}"'
        )
    username_pattern = r'^[\w.@+-]+\Z'
    if not re.match(username_pattern, username):
        invalid_chars = ''.join(
            set(re.findall(r'[^\w.@+-]', username))
        )
        raise ValidationError(
            'Некорректный логин. Логин не должен содержать символы: '
            f'{invalid_chars}'
        )
    return username
