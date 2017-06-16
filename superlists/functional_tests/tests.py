import platform
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utils import log


class NewVisitorTest(LiveServerTestCase):
    """LiveServerTestCase:
    Set up a live server for test and tear down when tests finished.
    """
    def setUp(self):
        if 'Ubuntu' in platform.platform():
            self.browser = webdriver.Firefox(
                executable_path='/usr/local/bin/geckodriver')
        else:
            self.browser = webdriver.Firefox(
                executable_path='/Applications/geckodriver')
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def __for_row_in_table(self, entry_text):
        time.sleep(10)
        table = self.browser.find_element_by_id('id-table-todo')
        log('find id-table-todo', table)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            entry_text,
            [row.text for row in rows]
        )

    def test_can_start_and_entry_and_retrive_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input = self.browser.find_element_by_id('id-input-todo')
        self.assertEqual(
            input.get_attribute('placeholder'),
            'What do you want to do?'
        )

        input.send_keys('Buy peacock feathers')
        input.send_keys(Keys.ENTER)
        self.__for_row_in_table('1: Buy peacock feathers')

        # have to re-find the input for another input test
        # or you'll get god knows what Error
        input = self.browser.find_element_by_id('id-input-todo')
        input.send_keys('Use peacock feathers to make a fly')
        input.send_keys(Keys.ENTER)
        self.__for_row_in_table('2: Use peacock feathers to make a fly')

        self.fail('Finish functional test')
