from django.test import TestCase

import accounts.views


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        resp = self.client.post(
            '/accounts/send_login_email/',
            data={'email': 'edith@example.com'}
        )
        self.assertRedirects(resp, '/')

    def test_sends_mail_to_address_from_post(self):
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_email_list):
            """
            This is a mock
            """
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_email_list = to_email_list

        # 要这样引用才能引入完整的 accounts.views 命名空间
        accounts.views.send_mail = fake_send_mail

        # 于是现在 invoke accounts.views.send_login_email 这个 function 的时候
        # 才会动态改变 self.send_mail_called 属性
        self.client.post(
            '/accounts/send_login_email/',
            data={'email': 'edith@example.com'}
        )

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_email_list, ['edith@example.com'])
