from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Todo, List
# from utils import log


def home_page(request):
    return render(request, 'lists/home_page.html')


def new_list(request):
    ls = List.objects.create()
    t = request.POST['todo-entry']
    todo = Todo(task=t, list=ls)
    try:
        todo.full_clean()
        todo.save()
    except ValidationError:
        ls.delete()
        err = "You can't have an empty input"
        return render(request, 'lists/home_page.html', {'error': err})
    return redirect(ls)


def view_list(request, list_id):
    ls = List.objects.get(id=list_id)
    context = {'list': ls}
    if request.method == 'POST':
        try:
            todo = Todo(task=request.POST['todo-entry'], list=ls)
            todo.full_clean()
            todo.save()
            return redirect(ls)
        except ValidationError:
            context['error'] = "You can't have an empty input"

    todos = Todo.objects.filter(list=ls)
    context['todos'] = todos
    return render(request, 'lists/list.html', context)
