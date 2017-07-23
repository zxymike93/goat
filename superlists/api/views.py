from django.http import JsonResponse

from lists.models import List, Todo


def lists(request, list_id):
    ls = List.objects.get(pk=list_id)
    if request.method == 'GET':
        todos = [{'id': t.id, 'task': t.task} for t in ls.todo_set.all()]
        return JsonResponse(todos, safe=False)
    else:
        Todo.objects.create(list=ls, task=request.POST['task'])
        return JsonResponse({}, status=201)
