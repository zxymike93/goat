import json

from django.test import TestCase

from lists.models import List, Todo
from utils import log


class ListApiTest(TestCase):
    url = '/api/lists/{}/'

    def test_lists_api_return_json(self):
        ls = List.objects.create()
        resp = self.client.get(self.url.format(ls.id))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['content-type'], 'application/json')

    def test_get_returns_todo_for_correct_list(self):
        other_list = List.objects.create()
        our_list = List.objects.create()
        Todo.objects.create(list=other_list, task='other')
        t1 = Todo.objects.create(list=our_list, task='1')
        t2 = Todo.objects.create(list=our_list, task='2')
        resp = self.client.get(self.url.format(our_list.id))
        self.assertEqual(
            json.loads(resp.content.decode('utf-8')),
            [
                {'id': t1.id, 'task': t1.task},
                {'id': t2.id, 'task': t2.task},
            ]
        )

    def test_post(self):
        ls = List.objects.create()
        resp = self.client.post(self.url.format(ls.id), {'task': 'new'})
        todo = ls.todo_set.last()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(todo.task, 'new')
