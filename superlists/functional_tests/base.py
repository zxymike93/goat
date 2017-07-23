import platform
import sys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from utils import log


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    """LiveServerTestCase:
    Set up a live server for test and tear down when tests finished.
    """
    @classmethod
    def setUpClass(cls):
        """Optionally set up url for liveserver-testing
        by >>> --liveserver=url
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

    def wait(fn):
        """
        @wait 相当于
        >>> wait(_wait_to_be_logged_in)
        >>> return modified_fn
        _wait_to_be_logged_in 已经作为参数传入 modified_fn 中
        _wait_to_be_logged_in() 才调用，相当于
        >>> wait(_wait_to_be_logged_in)()
        也就是
        >>> modified_fn()
        """
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn

    @wait
    def _wait_for(self, fn):
        return fn()

    def _todo_input(self):
        return self.browser.find_element_by_id('id_task')

    @wait
    def _get_error_message(self):
        return self.browser.find_element_by_css_selector('.has-error')

    @wait
    def _for_row_in_table(self, entry_text):
        table = self.browser.find_element_by_id('id-table-todo')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            entry_text,
            [row.text for row in rows]
        )

    def _add_todo(self, task):
        num_rows = len(
            self.browser.find_elements_by_css_selector('#id-table-todo tr')
        )
        input = self._todo_input()
        input.send_keys(task)
        input.send_keys(Keys.ENTER)
        num_task = num_rows + 1
        self._for_row_in_table('{}: {}'.format(num_task, task))

    @wait
    def _wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def _wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
