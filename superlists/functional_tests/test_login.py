"""
测试登陆退出功能
"""

import re

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    """
    测试是否有email输入框，是否向该email发送验证消息和链接。
    点击后是否登陆，能否退出。
    """
    def test_can_get_email_link_to_log_in(self):
        self.browser.get(self.server_url)
        mail_box = self.browser.find_element_by_name('email')
        mail_box.send_keys(TEST_EMAIL)
        mail_box.send_keys(Keys.ENTER)
        # wait for a check e-mail message in html body
        self._wait_for(
            lambda: self.assertIn(
                'Check your email',
                self.browser.find_element_by_tag_name('body').text
            )
        )
        # check email and find a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        # an auth url
        self.assertIn('Use this link to log in', email.body)
        login_link = re.search(r'http://.+/.+$', email.body)
        if not login_link:
            self.fail('Could not find url in email body:\n{email.body}')
        url = login_link.group(0)
        self.assertIn(self.server_url, url)
        # logged in
        self.browser.get(url)
        self._wait_to_be_logged_in(email=TEST_EMAIL)
        # test log out
        self.browser.find_element_by_link_text('Log out').click()
        self._wait_to_be_logged_out(email=TEST_EMAIL)
