from django.http.response import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("<h1>hello</h1>")


def about(request):
    return HttpResponse("<h1>about</h1>")

def index(request):
    
    return render(request, 'main/index.html')
