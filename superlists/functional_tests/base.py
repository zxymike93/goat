import platform
import sys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from utils import log


class FunctionalTest(StaticLiveServerTestCase):
    """LiveServerTestCase:
    Set up a live server for test and tear down when tests finished.
    """
    @classmethod
    def setUpClass(cls):
        """Optionally set up url for liveserver-testing
        >>> --liveserver=url
        """
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://{}'.format(arg.split('=')[1])
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = self._choose_webdriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def _choose_webdriver(self):
        if 'Ubuntu' in platform.platform():
            return webdriver.Firefox(
                executable_path='/usr/local/bin/geckodriver')
        else:
            return webdriver.Firefox(
                executable_path='/Applications/geckodriver')

    def _for_row_in_table(self, entry_text):
        time.sleep(10)
        table = self.browser.find_element_by_id('id-table-todo')
        log('find id-table-todo', table)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            entry_text,
            [row.text for row in rows]
        )
