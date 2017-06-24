from django.db import models


class List(models.Model):
    pass


class Todo(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    task = models.TextField()
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.task
