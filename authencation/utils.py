from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGanerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


token_ganetor = AppTokenGanerator()