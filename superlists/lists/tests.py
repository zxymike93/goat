from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_matches_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_index_response_right_html(self):
        req = HttpRequest()
        resp = home_page(req)
        html = render_to_string('lists/home_page.html')
        self.assertEqual(resp.content.decode(), html)
