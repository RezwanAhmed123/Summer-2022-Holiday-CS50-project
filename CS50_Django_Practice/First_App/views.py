from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "first_app/index.html")

def greet(request, name):
    return render(request, "first_app/greet.html", {
            "name": name.capitalize()
        }) # we are providing additional context to the webpage -> using the dictionary included and giving the website access to a variable called name and the value that was an argument to the function: greet