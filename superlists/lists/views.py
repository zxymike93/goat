# from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    if request.method == 'POST':
        # return HttpResponse(request.POST['todo-entry'])
        return render(request, 'lists/home_page.html',
                      {'todo_entries': request.POST['todo-entry']})
    return render(request, 'lists/home_page.html')
