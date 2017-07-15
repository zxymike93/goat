import platform
import sys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from utils import log


MAX_WAIT = 10


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

    def _todo_input(self):
        return self.browser.find_element_by_id('id_task')

    def _wait_for(self, fn):
        """显式等待 0.5*10秒
        用于在页面寻找一个元素
        或者一个断言
        (接收一个函数作为参数，try调用它，调用成功作为return)
        """
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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
    def _for_row_in_table(self, entry_text):
        table = self.browser.find_element_by_id('id-table-todo')
        log('find id-table-todo', table)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            entry_text,
            [row.text for row in rows]
        )

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
