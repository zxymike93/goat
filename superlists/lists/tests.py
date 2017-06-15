from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Todo
from lists.views import home_page


class TodoModelTest(TestCase):

    def test_save_and_retrive_todos(self):
        todo = Todo()
        todo.task = 'Write a Django test'
        todo.save()

        twodo = Todo()
        twodo.task = 'Write two Django test'
        twodo.save()

        todos = Todo.objects.all()
        self.assertEqual(todos.count(), 2)
        self.assertEqual(todo.task, todos[0].task)
        self.assertEqual(twodo.task, todos[1].task)


class HomePageViewTest(TestCase):

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

        # model saving test
        self.assertEqual(Todo.objects.count(), 1)
        first = Todo.objects.first()
        self.assertEqual(first.task, 'A new list item')
        # redirect after post
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], '/')
