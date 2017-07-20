import unittest
from unittest.mock import patch, Mock

from django.test import TestCase

from lists.forms import EMPTY_INPUT_ERROR, DUPLICATE_INPUT_ERROR
from lists.forms import TodoForm, ExistingListTodoForm, NewListForm
from lists.models import List, Todo
from utils import log


class TodoFormTest(TestCase):

    def test_form_todo_input_has_placeholder_and_css_classes(self):
        form = TodoForm()
        self.assertIn('placeholder="What do you want to do?"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validate_blank_todo(self):
        form = TodoForm(data={'task': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['task'], [EMPTY_INPUT_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        ls = List.objects.create()
        form = TodoForm(data={'task': 'do me'})
        todo = form.save(for_list=ls)
        self.assertEqual(todo, Todo.objects.last())
        self.assertEqual(todo.task, 'do me')
        self.assertEqual(todo.list, ls)


class ExistingListTodoFormTest(TestCase):

    def test_form_renders_todo_input_box(self):
        ls = List.objects.create()
        form = ExistingListTodoForm(for_list=ls)
        self.assertIn('placeholder="What do you want to do?"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validate_blank(self):
        ls = List.objects.create()
        form = ExistingListTodoForm(for_list=ls, data={'task': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['task'], [EMPTY_INPUT_ERROR])

    def test_form_validate_duplicate(self):
        ls = List.objects.create()
        Todo.objects.create(list=ls, task='no twins')
        form = ExistingListTodoForm(for_list=ls, data={'task': 'no twins'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['task'], [DUPLICATE_INPUT_ERROR])

    def test_form_save(self):
        ls = List.objects.create()
        form = ExistingListTodoForm(for_list=ls, data={'task': 'hi'})
        todo = form.save()
        self.assertEqual(todo, Todo.objects.last())


class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_autenticated(
        self, mock_create_new
    ):
        user = Mock(is_authenticated=False)
        form = NewListForm({'task': 'new todo'})
        form.is_valid()
        form.save(user=user)
        mock_create_new.assert_called_once_with(first_todo='new todo')

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_is_autenticated(
        self, mock_create_new
    ):
        user = Mock(is_authenticated=True)
        form = NewListForm({'task': 'new todo'})
        form.is_valid()
        form.save(user=user)
        mock_create_new.assert_called_once_with(
            first_todo='new todo',
            user=user,
        )

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_instance(self, mock_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'task': 'new'})
        form.is_valid()
        ls = form.save(user=user)
        self.assertEqual(ls, mock_create_new.return_value)

    @unittest.skip
    @patch('lists.forms.List')
    @patch('lists.forms.Todo')
    def test_save_creates_new_list_and_todo_from_post_data(
        self, MockTodo, MockList
    ):
        mock_todo = MockTodo.return_value
        mock_list = MockList.return_value
        user = Mock()
        # 只往 form 里面写 task
        form = NewListForm(data={'task': 'new list'})
        form.is_valid()
        log('form clean data', form.cleaned_data)

        def check_todo_task_and_list():
            self.assertEqual(mock_todo.task, 'new list')
            self.assertEqual(mock_todo.list, mock_list)
            self.assertTrue(mock_list.save.called)
        # 调用 save() 会运行上面这个函数
        mock_todo.save.side_effect = check_todo_task_and_list

        form.save(user=user)
        self.assertTrue(mock_todo.save.called)
