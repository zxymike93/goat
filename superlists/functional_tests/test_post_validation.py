import time

from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ValidationTest(FunctionalTest):
    """
    输入框的验证测试
        test_cannot_add_empty: 输入不能为空
        test_cannot_add_duplicate: 输入不能重复
        test_error_messages_are_cleared_on_input: 错误提示后更正输入，动态取消错误提示。
    """
    def __get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty(self):
        self.browser.get(self.server_url)
        # you post an empty input
        input = self._todo_input()
        input.send_keys('')
        input.send_keys(Keys.ENTER)
        # refreshed # warning: no empty input
        err = self.__get_error_element()
        self.assertEqual(err.text, "You can't have an empty input")
        # if you enter something # ok
        input = self._todo_input()
        input.send_keys('Buy milk')
        input.send_keys(Keys.ENTER)
        self._for_row_in_table('1: Buy milk')
        # you're now at your list view
        # post another empty input # warning again
        input = self._todo_input()
        input.send_keys('')
        input.send_keys(Keys.ENTER)
        err = self.__get_error_element()
        self.assertEqual(err.text, "You can't have an empty input")
        # you enter something again # ok
        input = self._todo_input()
        input.send_keys('Make tea')
        input.send_keys(Keys.ENTER)
        self._for_row_in_table('1: Buy milk')
        self._for_row_in_table('2: Make tea')

    def test_cannot_add_duplicate(self):
        self.browser.get(self.server_url)
        input = self._todo_input()
        input.send_keys('Buy milk')
        input.send_keys(Keys.ENTER)
        self._for_row_in_table('1: Buy milk')
        # repeat
        input = self._todo_input()
        input.send_keys('Buy milk')
        input.send_keys(Keys.ENTER)
        # error message
        self._for_row_in_table('1: Buy milk')
        err = self.__get_error_element()
        self.assertEqual(err.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.server_url)
        input = self._todo_input()
        input.send_keys('')
        input.send_keys(Keys.ENTER)
        err = self.__get_error_element()
        self.assertTrue(err.is_displayed())

        time.sleep(5)
        input = self._todo_input()
        input.send_keys('a')
        input.send_keys(Keys.ENTER)

        err = self.__get_error_element()
        self.assertFalse(err.is_displayed())
