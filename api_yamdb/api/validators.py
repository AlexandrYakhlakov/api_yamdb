from datetime import date

from django.core.exceptions import ValidationError


def validator_year_title(value):
    """Валидатор проверки года выпуска произведения.
    Год выпуска не может быть больше текущего года.
    """
    if value > date.today().year:
        raise ValidationError(
            'Ошибка при вводе года произведения. '
            f'Вы ввели год - {value}, а текущий год - {date.today().year}! '
            'Необходимо исправить.'
        )
    return value
