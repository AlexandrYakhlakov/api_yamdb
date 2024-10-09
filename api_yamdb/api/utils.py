import random

from django.conf import settings


def generate_confirmation_code(is_use_code: bool = False) -> str:
    if is_use_code:
        return settings.USED_CODE_VALUE
    while True:
        code = ''.join(
            random.choices(
                settings.CONFORMATION_CODE_CHARACTER_SET,
                k=settings.CONFIRMATION_CODE_LENGTH
            )
        )
        if code != settings.USED_CODE_VALUE:
            return code
