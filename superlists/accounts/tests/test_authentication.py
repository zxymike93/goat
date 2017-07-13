from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend as Auth
from accounts.models import Token


User = get_user_model()


class AuthenticateTest(TestCase):

    def test_returns_None_if_no_such_token(self):
        result = Auth().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = 'edith@example.com'
        token = Token.objects.create(email=email)
        user = Auth().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'edith@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = Auth().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def setUp(self):
        self.email = 'edith@example.com'

    def test_get_user_by_email(self):
        expected_user = User.objects.create(email=self.email)
        user = Auth().get_user(email=self.email)
        self.assertEqual(user, expected_user)

    def test_returns_None_if_cannot_get_user_with_THE_email(self):
        self.assertIsNone(Auth().get_user(email=self.email))
