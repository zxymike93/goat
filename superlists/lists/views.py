from django.shortcuts import render, redirect

from lists.models import Todo
# from utils import log


def home_page(request):
    return render(request, 'lists/home_page.html')


def new_list(request):
    Todo.objects.create(task=request.POST['todo-entry'])
    return redirect('/lists/the-only-list-in-the-world/')


def view_list(request, list_id):

    todos = Todo.objects.filter(list=list_id)
    return render(request, 'lists/list.html', {'todos': todos})
