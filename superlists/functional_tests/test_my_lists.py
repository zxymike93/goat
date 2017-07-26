from functional_tests.base import FunctionalTest


class MyListTest(FunctionalTest):
    """
    test_create_pre_authenticated_session_create_session_for_a_user:
        测试辅助函数能成功生成cookie
    test_logged_in_users_lists_are_saved_as_my_lists:
        测试登陆用户能保存多个list并能回访
    """
    def test_create_pre_authenticated_session_create_session_for_a_user(self):
        """
        测试上面的辅助函数是否正常运行，即：
        调用之前没登陆，调用之后通过session能直接登陆
        """
        email = 'edith@example.com'
        self.browser.get(self.server_url)
        self._wait_to_be_logged_out(email)

        self._create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self._wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self._create_pre_authenticated_session('edith@example.com')

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
        self.browser.find_element_by_link_text('simens').click()
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
        self._wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text('My lists'),
                []
            )
        )
