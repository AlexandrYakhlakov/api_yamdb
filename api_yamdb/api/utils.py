import random

from django.conf import settings


def generate_confirmation_code() -> str:
    return ''.join(
        random.choices(
            settings.CONFORMATION_CODE_CHARACTER_SET,
            k=settings.CONFIRMATION_CODE_LENGTH
        )
    )
