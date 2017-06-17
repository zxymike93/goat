from django.shortcuts import render, redirect

from lists.models import Todo
from utils import log


def home_page(request):
    if request.method == 'POST':
        log('-' * 7)
        log('POST:', request.POST)
        if request.POST:
            Todo.objects.create(task=request.POST['todo-entry'])
        return redirect('/lists/the-only-list-in-the-world/')
    elif request.method == 'GET':
        log('-' * 7)
        log('Request:', request.method)
        context = {'todo_entries': Todo.objects.all()}
        log('Context:', context)
        resp = render(request, 'lists/home_page.html', context)
        log('Response:', resp.content)
        return resp


def view_list(request):
    todos = Todo.objects.all()
    return render(request, 'list.html', {'todos': todos})
