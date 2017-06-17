from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Todo, List
from lists.views import home_page
from utils import log


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


class NewListTest(TestCase):

    def test_can_save_post_in_db(self):
        self.client.post('/lists/new/', {'todo-entry': 'A new list item'})
        # model saving test
        self.assertEqual(Todo.objects.count(), 1)
        first = Todo.objects.first()
        self.assertEqual(first.task, 'A new list item')

    def test_redirects_after_post(self):
        resp = self.client.post('/lists/new/',
                                {'todo-entry': 'A new list item'})
        self.assertEqual(resp.status_code, 302)
        ls = List.objects.first()
        self.assertRedirects(resp, '/lists/%d/' % ls.id)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        ls = List.objects.create()
        resp = self.client.get('/lists/%d/' % ls.id)
        self.assertTemplateUsed(resp, 'lists/list.html')

    def test_displays_only_todos_for_unique_list(self):
        list1 = List.objects.create()
        todo1 = Todo.objects.create(task='todo 1', list=list1)
        todo2 = Todo.objects.create(task='todo 2', list=list1)

        list2 = List.objects.create()
        todo3 = Todo.objects.create(task='todo 3', list=list2)
        todo4 = Todo.objects.create(task='todo 4', list=list2)

        log('list1 id', list1.id)
        resp = self.client.get('/lists/%d/' % list1.id)
        log('test_displays_only_todo_for_unique_list', resp)

        self.assertContains(resp, todo1.task)
        self.assertContains(resp, todo2.task)
        self.assertNotContains(resp, todo3.task)
        self.assertNotContains(resp, todo4.task)


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
