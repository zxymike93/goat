import platform
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utils import log


class NewVisitorTest(StaticLiveServerTestCase):
    """LiveServerTestCase:
    Set up a live server for test and tear down when tests finished.
    """
    def setUp(self):
        self.browser = self.__chose_webdriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def __chose_webdriver(self):
        if 'Ubuntu' in platform.platform():
            return webdriver.Firefox(
                executable_path='/usr/local/bin/geckodriver')
        else:
            return webdriver.Firefox(
                executable_path='/Applications/geckodriver')

    def __for_row_in_table(self, entry_text):
        time.sleep(10)
        table = self.browser.find_element_by_id('id-table-todo')
        log('find id-table-todo', table)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            entry_text,
            [row.text for row in rows]
        )

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input = self.browser.find_element_by_id('id-input-todo')
        self.assertAlmostEqual(
            input.location['x'] + input.size['width'] / 2,
            512,
            delta=5
        )
        # see if it keeps center after post
        input.send_keys('testing for center\n')
        input = self.browser.find_element_by_id('id-input-todo')
        self.assertAlmostEqual(
            input.location['x'] + input.size['width'] / 2,
            512,
            delta=5
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
        # wait and redirect to personal list url
        time.sleep(5)
        list_identifier = self.browser.current_url
        log('list_identifier', list_identifier)
        self.assertRegex(list_identifier, '/lists/.+')
        self.__for_row_in_table('1: Buy peacock feathers')

        # have to re-find the input for another input test
        # or you'll get god knows what Error
        input = self.browser.find_element_by_id('id-input-todo')
        input.send_keys('Use peacock feathers to make a fly')
        input.send_keys(Keys.ENTER)
        time.sleep(5)
        self.__for_row_in_table('2: Use peacock feathers to make a fly')

        #
        # start a new browser
        #
        self.browser.quit()
        self.browser = self.__chose_webdriver()
        # self.browser = webdriver.Firefox(
        #     executable_path='/Applications/geckodriver')

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        input = self.browser.find_element_by_id('id-input-todo')
        input.send_keys('Buy milk')
        input.send_keys(Keys.ENTER)

        time.sleep(5)
        another_list_identifier = self.browser.current_url
        self.assertRegex(another_list_identifier, '/lists/.+')
        self.assertNotEqual(another_list_identifier, list_identifier)

        # check again after enter
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        self.fail('Finish functional test')
