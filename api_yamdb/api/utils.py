import random

from django.conf import settings

from reviews.models import User


def generate_confirmation_code() -> str:
    return ''.join(
        random.choices(
            settings.CONFORMATION_CODE_CHARACTER_SET,
            k=settings.CONFIRMATION_CODE_LENGTH
        )
    )


def save_use_confirmation_code(user: User) -> None:
    user.confirmation_code = settings.USED_CODE_VALUE
    user.save(update_fields=['confirmation_code'])
