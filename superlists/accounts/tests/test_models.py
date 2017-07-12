from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='test@example.com')
        user.full_clean()

    def test_email_is_pk(self):
        user = User(email='test@example.com')
        self.assertEqual(user.pk, 'test@example.com')
