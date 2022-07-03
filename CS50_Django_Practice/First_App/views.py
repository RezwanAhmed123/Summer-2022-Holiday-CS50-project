from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("This is my first web application!")

def greet(request, name):
    return HttpResponse(f"Hello {name}! Welcome to my first web application!")