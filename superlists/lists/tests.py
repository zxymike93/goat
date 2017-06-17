from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Todo, List
from lists.views import home_page


class ListAndTodoModelsTest(TestCase):

    def test_save_and_retrive_instances(self):
        list_ = List()
        list_.save()
        # create a todo with task and list
        todo = Todo()
        todo.task = 'The first (ever) list'
        todo.list = list_
        todo.save()
        # create another todo with task and the same list
        twodo = Todo()
        twodo.task = 'Todo the second'
        twodo.list = list_
        twodo.save()
        # check if the list created in db same as list_
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        # check if db contains the same data as instances above
        todos = Todo.objects.all()
        self.assertEqual(todos.count(), 2)
        self.assertEqual(todo.task, todos[0].task)
        self.assertEqual(twodo.task, todos[1].task)
        self.assertEqual(todo.list, todos[0].list)
        self.assertEqual(todo.list, todos[1].list)


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
        list_ = List.objects.create()

        Todo.objects.create(task='todo 1', list=list_)
        Todo.objects.create(task='todo 2', list=list_)

        resp = self.client.get('/lists/the-only-list-in-the-world/')

        self. assertContains(resp, 'todo 1')
        self. assertContains(resp, 'todo 2')
