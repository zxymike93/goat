from django.shortcuts import render


def home_page(request):
    return render(request, 'lists/home_page.html')
