import random

from reviews.constants import CONFIRMATION_CODE_LENGTH


def generate_confirmation_code(
        code_length=CONFIRMATION_CODE_LENGTH
):
    return random.randint(
        10 ** (code_length - 1),
        10 ** code_length - 1
    )
