from datetime import date
import re

from django.core.exceptions import ValidationError


def validator_year(value):
    """Валидатор проверки года выпуска произведения."""
    if value > date.today().year:
        raise ValidationError(
            'Год выпуска не должен быть больше текущего больше текущего года.'
        )
    return value


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя')
    if not re.match('[a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'Имя содержит недопустимые символы'
        )
