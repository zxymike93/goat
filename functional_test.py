import platform
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        if 'Ubuntu' in platform.platform():
            self.browser = webdriver.Firefox(
                executable_path='/usr/local/bin/geckodriver')
        else:
            self.browser = webdriver.Firefox(
                executable_path='/Applications/geckodriver')
        self.browser.implicitly_wait(5)

    def tearDown(self):
        """
        Calls whether test succeed or not,
        unless.. setUp() fails.
        """
        self.browser.quit()

    def test_can_start_and_entry_and_retrive_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input = self.browser.find_element_by_id('id-input-todo')
        self.assertEqual(
            input.get_attribute('placeholder'),
            'What do you want to do?'
        )

        input.send_keys('Write a todo app')
        input.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id-table-todo')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. Write a todo app' for row in rows),
            'Entries do not appear on table.'
        )

        self.fail('Finish functional test')

        # entry: "buy something"
        # update >> shows "1. buy something"
        # entry: "buy more"
        # update >> shows "2. buy more"
        # check


if __name__ == '__main__':
    unittest.main()
