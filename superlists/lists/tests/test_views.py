from unittest import skip

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape

from lists.forms import EMPTY_INPUT_ERROR, DUPLICATE_INPUT_ERROR
from lists.forms import TodoForm, ExistingListTodoForm
from lists.models import Todo, List
from lists.views import home_page
from utils import log


class HomePageViewTest(TestCase):

    maxDiff = None

    @skip
    def test_root_url_mapping_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    @skip
    def test_home_page_render_correct_html(self):
        req = HttpRequest()
        req.method = 'GET'
        resp = home_page(req)
        html = render_to_string('lists/home_page.html', {'form': TodoForm})
        self.assertMultiLineEqual(resp.content.decode(), html)

    def test_home_page_renders_home_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, 'lists/home_page.html')

    def test_home_page_uses_todo_form(self):
        resp = self.client.get('/')
        self.assertIsInstance(resp.context['form'], TodoForm)


class NewListViewTest(TestCase):

    def test_can_save_post_in_db(self):
        self.client.post('/lists/new/', {'task': 'A new list item'})
        # model saving test
        self.assertEqual(Todo.objects.count(), 1)
        first = Todo.objects.first()
        self.assertEqual(first.task, 'A new list item')

    def test_redirects_after_post(self):
        resp = self.client.post('/lists/new/',
                                {'task': 'A new list item'})
        self.assertEqual(resp.status_code, 302)
        ls = List.objects.first()
        self.assertRedirects(resp, ('/lists/%d/' % ls.id))

    def test_for_invalid_input_renders_home_page(self):
        resp = self.client.post('/lists/new/', data={'task': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lists/home_page.html')

    def test_validation_errors_are_shown_on_home_page(self):
        resp = self.client.post('/lists/new/', data={'task': ''})
        self.assertContains(resp, escape(EMPTY_INPUT_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        resp = self.client.post('/lists/new/', data={'task': ''})
        self.assertIsInstance(resp.context['form'], TodoForm)

    def test_invalid_input_not_saved(self):
        self.client.post('/lists/new/', data={'task': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Todo.objects.count(), 0)


class ListViewTest(TestCase):
    """
    Tests for views.view_list
        test_duplicate_todo_validation_errors_end_up_on_lists_page:
    """
    def __post_invalid_input(self):
        ls = List.objects.create()
        resp = self.client.post('/lists/%d/' % ls.id, data={'task': ''})
        return resp

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

    def test_can_save_post_todo_to_its_own_list(self):
        other = List.objects.create()
        own = List.objects.create()

        self.client.post(
            ('/lists/%d/' % own.id),
            data={'task': 'New todo in its own list'}
        )
        self.assertEqual(Todo.objects.count(), 1)
        # TODO: should use last not first()
        todo = Todo.objects.first()
        log('todo last', todo)
        self.assertEqual(todo.task, 'New todo in its own list')
        self.assertEqual(todo.list, own)
        self.assertNotEqual(todo.list, other)

    def test_redirects_to_list_view_after_post(self):
        own = List.objects.create()

        resp = self.client.post(
            ('/lists/%d/' % own.id),
            data={'task': 'New todo in its own list'}
        )
        self.assertRedirects(resp, ('/lists/%d/' % own.id))

    def test_passes_correct_list_to_template(self):
        ls = List.objects.create()
        resp = self.client.get('/lists/%d/' % ls.id)
        self.assertEqual(resp.context['list'], ls)

    def test_validation_errors_are_sent_to_list_page_itself(self):
        resp = self.__post_invalid_input()
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lists/list.html')

    def test_for_invalid_input_shows_error(self):
        resp = self.__post_invalid_input()
        self.assertContains(resp, escape(EMPTY_INPUT_ERROR))

    def test_invalid_input_not_saved(self):
        self.__post_invalid_input()
        self.assertEqual(Todo.objects.count(), 0)

    def test_for_invalid_input_passes_form_to_template(self):
        resp = self.__post_invalid_input()
        self.assertIsInstance(resp.context['form'], ExistingListTodoForm)

    def test_duplicate_todo_validation_errors_end_up_on_lists_page(self):
        ls = List.objects.create()
        Todo.objects.create(list=ls, task='textey')
        resp = self.client.post(
            '/lists/%d/' % ls.id,
            data={'task': 'textey'}
        )

        err_msg = escape(DUPLICATE_INPUT_ERROR)
        self.assertContains(resp, err_msg)
        self.assertTemplateUsed(resp, 'lists/list.html')
        self.assertEqual(Todo.objects.all().count(), 1)


class MyListsTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        resp = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(resp, 'lists/my_lists.html')
