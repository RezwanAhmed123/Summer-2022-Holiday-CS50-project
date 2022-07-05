from django.shortcuts import render

tasks = [
    "Take out the trash",
    "Fix the toilet seat",
    "Fix the wifi-router"
]

# Create your views here.
def index(request):
    return render(request,"tasks/index.html",{
        "tasks": tasks
    })

def add_task(request):
    return render(request, "tasks/add_task.html")