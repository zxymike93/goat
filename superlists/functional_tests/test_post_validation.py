from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ValidationTest(FunctionalTest):

    def test_cannot_add_empty(self):
        self.browser.get(self.server_url)
        # you post an empty input
        input = self._todo_input()
        input.send_keys('')
        input.send_keys(Keys.ENTER)
        # refreshed # warning: no empty input
        err = self.browser.find_element_by_css_selector('.has-error')
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
        err = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(err.text, "You can't have an empty input")
        # you enter something again # ok
        input = self._todo_input()
        input.send_keys('Make tea')
        input.send_keys(Keys.ENTER)
        self._for_row_in_table('1: Buy milk')
        self._for_row_in_table('2: Make tea')

        self.fail('Write me!')
