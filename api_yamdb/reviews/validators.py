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


def validate_username(username):
    if username == USER_PROFILE_PATH:
        raise ValidationError(
            f'Логин не может принимать значение "{USER_PROFILE_PATH}"'
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
