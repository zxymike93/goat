from django.contrib.auth import (BACKEND_SESSION_KEY, SESSION_KEY,
                                 get_user_model)
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

from functional_tests.base import FunctionalTest


User = get_user_model()


class MyListTest(FunctionalTest):

    def __create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        # session 类
        # request headers 中用于验证身份，格式如下：
        # Cookie:
        #     sessionid=90s9olod6nppgfgk8rfq3a5injvtvmpa;
        #     csrftoken=rAqDLBTQR8QQdXII3iLXEGTugFYxeaoF
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        self.browser.get(self.server_url + '/unavailable_url/')
        self.browser.add_cookie(
            {
                'name': settings.SESSION_COOKIE_NAME,
                'value': session.session_key,
                'path': '/'
            }
        )

    def test_create_pre_authenticated_session_create_session_for_a_user(self):
        """
        测试上面的辅助函数是否正常运行，即：
        调用之前没登陆，调用之后通过session能直接登陆
        """
        email = 'edith@example.com'
        self.browser.get(self.server_url)
        self._wait_to_be_logged_out(email)

        self.__create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self._wait_to_be_logged_in(email)
