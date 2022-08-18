from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import format_html_join, format_html
import base64
import re


class Base64Validator:

    def __init__(self):
        self.RE_BASE64 = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
        self.HASH_SIZE = 44

    def validate(self, password, user=None):

        validation_error = ValidationError(
                "Anomalous password received, please check the integrity of your client. The password should be a base64-encoded string of your password hash, see documentation.",
                code='anomalous_password_encoding',
            )

        if not re.search(self.RE_BASE64, password) or len(password) != self.HASH_SIZE:
            raise validation_error

        try:
            base64.b64encode(base64.b64decode(password)) == password
        except Exception:
            raise validation_error

    def get_help_text(self):
        help_texts = [
            "Your password should contain at least 8 characters.",
            "Your password should contain letters, numbers and symbols.",
            "Your password shouldn't be too similar to your other personal information.",
            "Your password shouldn't be a commonly used password."
        ]
        help_items = format_html_join('', '<li>{}</li>', ((help_text,) for help_text in help_texts))
        return format_html('<ul>{}</ul>', help_items) if help_items else ''
