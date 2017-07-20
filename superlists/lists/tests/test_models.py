from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import List, Todo


User = get_user_model()


class ListModelTest(TestCase):
    """
        test_get_absolute_url: get_absolute_url 返回 /lists/<id>
    """
    def test_get_absolute_url(self):
        ls = List.objects.create()
        self.assertEqual(ls.get_absolute_url(), '/lists/%d/' % (ls.id))

    def test_lists_can_have_owners(self):
        user = User.objects.create(email='a@b.com')
        ls = List.objects.create(user=user)
        self.assertIn(ls, user.list_set.all())

    def test_list_owner_is_optional(self):
        List.objects.create()  # should not raise

    def test_list_name_is_the_first_todo(self):
        ls = List.objects.create()
        Todo.objects.create(list=ls, task='first todo')
        Todo.objects.create(list=ls, task='second todo')
        self.assertEqual(ls.name, 'first todo')

    def test_create_new_creates_list_and_first_todo(self):
        List.create_new(first_todo='new todo')
        todo = Todo.objects.last()
        ls = List.objects.last()
        self.assertEqual(todo.task, 'new todo')
        self.assertEqual(todo.list, ls)

    def test_create_new_optionally_saves_user(self):
        user = User.objects.create()
        List.create_new('new one', user=user)
        ls = List.objects.last()
        self.assertEqual(ls.user, user)

    # the two following tests just instantial User
    # and not calling save() / objects.create()
    # won't hit database, so that they run faster
    def test_list_can_have_user(self):
        List(user=User())  # should not raise

    def test_list_attribute_user_is_optional(self):
        List().full_clean()  # should not raise


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
