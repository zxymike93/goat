from unittest.mock import patch, call

from django.test import TestCase

from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        resp = self.client.post(
            '/accounts/send_login_email/',
            data={'email': 'edith@example.com'}
        )
        self.assertRedirects(resp, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        """使用 patch 装饰器
        运行这个测试函数之前会把 send_mail 赋值为 mock 函数
        运行结束之后 send_mail 回到原有值
        (简单来说就是装饰器该有的特性)

        第二个参数是一个 mock 对象，由@patch得到
        """
        self.client.post(
            '/accounts/send_login_email/',
            data={'email': 'edith@example.com'}
        )

        self.assertTrue(mock_send_mail)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'zxymike93@163.com')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        """
        跟随 redirect
        """
        resp = self.client.post(
            '/accounts/send_login_email/',
            data={'email': 'edith@example.com'},
            follow=True
        )
        msg = list(resp.context['messages'])[0]

        self.assertEqual(
            msg.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(msg.tags, 'success')

    def test_creates_token_associated_with_email(self):
        self.client.post(
            '/accounts/send_login_email/',
            data={'email': 'edith@example.com'},
        )
        token = Token.objects.last()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post(
            '/accounts/send_login_email/',
            data={'email': 'edith@example.com'},
        )
        token = Token.objects.last()
        expected_url = ('http://testserver/'
                        'accounts/login?token={}').format(token.uid)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self, mock_auth):
        resp = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(resp, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abc123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        resp = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(resp.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abc123')
        self.assertFalse(mock_auth.login.called)


class LogoutViewTest(TestCase):

    def test_redirects_to_home_page(self):
        resp = self.client.get('/accounts/logout')
        self.assertRedirects(resp, '/')
