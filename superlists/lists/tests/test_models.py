from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import List, Todo


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

    def test_empty_task_cannot_be_saved(self):
        list_ = List.objects.create()
        todo = Todo(list=list_, task='')
        # assert: should raise validationerror, else the assertion false
        with self.assertRaises(ValidationError):
            todo.save()
            todo.full_clean()
