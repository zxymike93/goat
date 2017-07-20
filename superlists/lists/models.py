from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class List(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True
    )

    @property
    def name(self):
        return self.todo_set.first().task

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    def create_new(self):
        pass


class Todo(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    task = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        unique_together = ('list', 'task')

    def __str__(self):
        return self.task
