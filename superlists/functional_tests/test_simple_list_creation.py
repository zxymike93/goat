import time

from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest
from utils import log


class NewVisitorTest(FunctionalTest):

    def test_can_start_and_entry_and_retrive_it_later(self):
        self.browser.get(self.server_url)

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
        self._for_row_in_table('1: Buy peacock feathers')

        # have to re-find the input for another input test
        # or you'll get god knows what Error
        input = self.browser.find_element_by_id('id-input-todo')
        input.send_keys('Use peacock feathers to make a fly')
        input.send_keys(Keys.ENTER)
        time.sleep(5)
        self._for_row_in_table('2: Use peacock feathers to make a fly')

        #
        # start a new browser
        #
        self.browser.quit()
        self.browser = self._choose_webdriver()
        # self.browser = webdriver.Firefox(
        #     executable_path='/Applications/geckodriver')

        self.browser.get(self.server_url)
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
