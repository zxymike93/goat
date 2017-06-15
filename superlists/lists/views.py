from django.shortcuts import render, redirect

from lists.models import Todo


def home_page(request):
    if request.method == 'POST':
        Todo.objects.create(task=request.POST['todo-entry'])
        return redirect('/')
    return render(request, 'lists/home_page.html',
                  {'todo-entries': Todo.objects.all()})
