from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        print(timestamp)
        print(six.text_type(timestamp))
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.username)
        )
account_activation_token = TokenGenerator()