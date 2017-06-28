from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import List, Todo


class ListModelTest(TestCase):
    """
        test_get_absolute_url: get_absolute_url 返回 /lists/<id>
    """
    def test_get_absolute_url(self):
        ls = List.objects.create()
        self.assertEqual(ls.get_absolute_url(), '/lists/%d/' % (ls.id))


class TodoModelsTest(TestCase):
    """
        test_default_task_value: 生成新实例时带默认值
        test_todo_is_related_to_list: 测试外建的正反关联
        test_save_in_correct_order: 保存的顺序和创建的顺序一致
        test_empty_task_cannot_be_saved: 不能保存空 task 的 Todo
        test_duplicate_task_cannot_be_saved: 不能保存重复的 task
        test_can_save_same_task_to_different_lists: 不同 list 中可以保存重复的 task
    """
    def test_default_task_value(self):
        todo = Todo()
        self.assertEqual(todo.task, '')

    def test_todo_is_related_to_list(self):
        ls = List.objects.create()
        todo = Todo()
        todo.list = ls
        todo.save()
        self.assertIn(todo, ls.todo_set.all())

    def test_save_in_correct_order(self):
        ls = List.objects.create()
        todo = Todo.objects.create(
            list=ls, task='The first (ever) list')
        twodo = Todo.objects.create(
            list=ls, task='Todo the second')
        threedo = Todo.objects.create(
            list=ls, task='Todo the third')
        self.assertEqual(
            list(Todo.objects.all()),
            [todo, twodo, threedo]
        )

    def test_empty_task_cannot_be_saved(self):
        ls = List.objects.create()
        todo = Todo(list=ls, task='')
        # assert: should raise validationerror, else the assertion false
        with self.assertRaises(ValidationError):
            todo.save()
            todo.full_clean()

    def test_duplicate_task_cannot_be_saved(self):
        ls = List.objects.create()
        Todo.objects.create(list=ls, task='bar')
        with self.assertRaises(ValidationError):
            todo = Todo(list=ls, task='bar')
            todo.full_clean()
            # todo.save()

    def test_can_save_same_task_to_different_lists(self):
        ls1 = List.objects.create()
        ls2 = List.objects.create()
        Todo.objects.create(list=ls1, task='bar')
        todo = Todo(list=ls2, task='bar')
        todo.full_clean()
