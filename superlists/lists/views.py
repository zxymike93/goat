from django.shortcuts import render, redirect

from lists.models import Todo
from utils import log


def home_page(request):
    if request.method == 'POST':
        if request.POST:
            Todo.objects.create(task=request.POST['todo-entry'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'lists/home_page.html')


def view_list(request):
    todos = Todo.objects.all()
    return render(request, 'lists/list.html', {'todos': todos})
