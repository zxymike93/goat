from functional_tests.base import FunctionalTest


class ValidationTest(FunctionalTest):
    def test_cannot_add_empty(self):
        # you post an empty input
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id-input-todo').send_keys('\n')
        # refresh the page
        # warning: no empty input
        err = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(err.text, "You can't have an empty input")
        # enter something
        # ok
        self.browser.find_element_by_id(
            'id-input-todo').send_keys('Buy milk\n')
        self._for_row_in_table('1: Buy milk')
        # post another empty input
        # warning again
        self.browser.find_element_by_id('id-input-todo').send_keys('\n')
        err = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(err.text, "You can't have an empty input")

        self.browser.find_element_by_id(
            'id-input-todo').send_keys('Make tea\n')
        self._for_row_in_table('1: Buy milk')
        self._for_row_in_table('2: Make tea')

        self.fail('Write me!')
