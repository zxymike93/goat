from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_matches_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_response_right_html(self):
        req = HttpRequest()
        resp = home_page(req)
        html = render_to_string('lists/home_page.html')
        self.assertEqual(resp.content.decode(), html)

    def test_home_page_can_save_post_request(self):
        req = HttpRequest()
        req.method = 'POST'
        req.POST['todo-entry'] = 'A new list item'

        resp = home_page(req)
        self.assertIn('A new list item', resp.content.decode())
        html = render_to_string(
            'lists/home_page.html',
            {'todo_entries': 'A new list item'}  # pass value to template
        )
        self.assertEqual(resp.content.decode(), html)
