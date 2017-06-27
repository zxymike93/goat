from django.test import TestCase

from lists.forms import EMPTY_INPUT_ERROR
from lists.forms import TodoForm
from lists.models import List, Todo


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
