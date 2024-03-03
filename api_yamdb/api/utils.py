from rest_framework.exceptions import ValidationError

import re


def validate_name(value):
    """Validate username length and consistency of using characters in it."""
    if len(value) > 150:
        raise ValidationError("Username must be 150 characters or fewer.")

    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            "Invalid username format."
            "Only letters, digits, and @/./+/-/ are allowed."
        )


def validate_email(value):
    """Validate email length."""
    if len(value) > 254:
        raise ValidationError("Email must be 254 characters or fewer.")
