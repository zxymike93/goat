from django.contrib.auth import (BACKEND_SESSION_KEY, SESSION_KEY,
                                 get_user_model)
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

from functional_tests.base import FunctionalTest


User = get_user_model()


class MyListTest(FunctionalTest):
    """
    __create_pre_authenticated_session: 辅助函数
    test_create_pre_authenticated_session_create_session_for_a_user:
        测试辅助函数能成功生成cookie
    """
    def __create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        # session 类
        session = SessionStore()
        # SESSION_KEY == '_auth_user_id'
        session[SESSION_KEY] = user.pk
        # BACKEND_SESSION_KEY == '_auth_user_backend'
        # settings.AUTHENTICATION_BACKENDS[0] ==
        # ['accounts.authentication.PasswordlessAuthenticationBackend']
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        self.browser.get(self.server_url + '/unavailable_url/')
        # request headers 中用于验证身份，格式如下：
        # Cookie:
        #     sessionid=90s9olod6nppgfgk8rfq3a5injvtvmpa;
        #     csrftoken=rAqDLBTQR8QQdXII3iLXEGTugFYxeaoF
        self.browser.add_cookie(
            {
                'name': settings.SESSION_COOKIE_NAME,  # 'sessionid'
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

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.__create_pre_authenticated_session('edith@example.com')

        self.browser.get(self.server_url)
        self._add_todo('simens')
        self._add_todo('I got hired')
        first_list_url = self.browser.current_url
        # enter personal lists
        self.browser.find_element_by_link_text('My lists').click()
        self._wait_for(
            lambda: self.browser.find_element_by_link_text('simens')
        )
        # return to first list
        self.browser.find_element_by_link_text('I got hired')
        self._wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # start another list
        self.browser.get(self.server_url)
        self._add_todo('hello')
        second_list_url = self.browser.current_url
        self.browser.find_element_by_link_text('My lists').click()
        self._wait_for(
            lambda: self.browser.find_element_by_link_text('hello')
        )
        self.browser.find_element_by_link_text('hello').click()
        self._wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # logout
        self.browser.find_element_by_link_text('Log out').click()
        self._wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_link_text('My lists'),
            []
        ))
