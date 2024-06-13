from django.shortcuts import render


def home(request):
    return render(request, 'website/home.html')


def about(request):
    return render(request, 'website/about.html')


def book(request):
    return render(request, 'website/book.html')


def menu(request):
    return render(request, 'menu/menu.html')


def staff(request):
    return render(request, 'website/base.html', {})
