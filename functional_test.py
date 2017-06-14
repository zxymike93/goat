import platform
import unittest

from selenium import webdriver


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
        self.fail('browser title is %s' % self.browser.title)

        # entry: "buy something"
        # update >> shows "1. buy something"
        # entry: "buy more"
        # update >> shows "2. buy more"
        # check


if __name__ == '__main__':
    unittest.main()
