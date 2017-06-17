from django.shortcuts import render, redirect

from lists.models import Todo, List
from utils import log


def home_page(request):
    return render(request, 'lists/home_page.html')


def new_list(request):
    ls = List.objects.create()
    todo = request.POST['todo-entry']
    Todo.objects.create(task=todo, list=ls)
    return redirect('/lists/%d/' % ls.id)


def view_list(request, list_id):
    todos = Todo.objects.filter(list=list_id)
    return render(request, 'lists/list.html', {'todos': todos})
