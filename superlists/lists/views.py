from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.forms import TodoForm
from lists.models import Todo, List
from utils import log


def home_page(request):
    form = TodoForm()
    return render(request, 'lists/home_page.html', {'form': form})


def new_list(request):
    form = TodoForm(data=request.POST)
    if form.is_valid():
        ls = List.objects.create()
        Todo.objects.create(task=request.POST['task'], list=ls)
        return redirect(ls)
    else:
        return render(request, 'lists/home_page.html', {'form': form})


def view_list(request, list_id):
    ls = List.objects.get(id=list_id)
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(data=request.POST)
        if form.is_valid():
            Todo.objects.create(task=request.POST['task'], list=ls)
            return redirect(ls)

    todos = Todo.objects.filter(list=ls)
    context = {
        'list': ls,
        'todos': todos,
        'form': form
    }
    return render(request, 'lists/list.html', context)
