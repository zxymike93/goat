from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Token


User = get_user_model()
TEST_EMAIL = 'test@example.com'


class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='test@example.com')
        user.full_clean()

    def test_email_is_pk(self):
        user = User(email='test@example.com')
        self.assertEqual(user.pk, 'test@example.com')


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email=TEST_EMAIL)
        token2 = Token.objects.create(email=TEST_EMAIL)
        self.assertNotEqual(token1.uid, token2.uid)
