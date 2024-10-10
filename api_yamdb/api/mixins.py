from reviews.validators import validate_username


class UserNameValidationMixin:
    def validate_username(self, username):
        return validate_username(username)