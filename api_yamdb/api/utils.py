import random

from reviews.models import User


def generate_confirmation_code(
        code_length=User.CONFIRMATION_CODE_LENGTH
):
    return random.randint(
        10**(code_length-1),
        10**code_length - 1
    )
