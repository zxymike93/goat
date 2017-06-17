from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Todo
from lists.views import home_page


class TodoModelTest(TestCase):

    def test_save_and_retrive_instances(self):
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

    def test_root_url_mapping_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_render_correct_html(self):
        req = HttpRequest()
        req.method = 'GET'
        resp = home_page(req)
        html = render_to_string('lists/home_page.html')
        self.assertEqual(resp.content.decode(), html)

    def test_home_page_not_saving_empty_post(self):
        req = HttpRequest()
        req.method = 'POST'
        home_page(req)
        self.assertEqual(Todo.objects.count(), 0)

    def test_home_page_can_save_post_in_db(self):
        req = HttpRequest()
        req.method = 'POST'
        req.POST['todo-entry'] = 'A new list item'
        # model saving test
        home_page(req)
        self.assertEqual(Todo.objects.count(), 1)
        first = Todo.objects.first()
        self.assertEqual(first.task, 'A new list item')

    def test_home_page_redirects_after_post(self):
        req = HttpRequest()
        req.method = 'POST'
        resp = home_page(req)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp['location'],
            '/lists/the-only-list-in-the-world/'
        )


class ListViewTest(TestCase):
    """Use Django's test client"""
    def test_uses_list_template(self):
        resp = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(resp, 'lists/list.html')

    def test_displays_all_todos(self):
        Todo.objects.create(task='todo 1')
        Todo.objects.create(task='todo 2')

        resp = self.client.get('/lists/the-only-list-in-the-world/')

        self. assertContains(resp, 'todo 1')
        self. assertContains(resp, 'todo 2')
