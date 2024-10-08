import random

from django.conf import settings

from reviews.constants import CONFIRMATION_CODE_LENGTH


def generate_confirmation_code(code_length=CONFIRMATION_CODE_LENGTH):
    return ''.join(
        [random.choice(settings.CONFORMATION_CODE_CHARACTER_SET)
         for _ in range(code_length)]
    )
