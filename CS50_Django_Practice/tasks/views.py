from django.urls import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task") #This "task" variable corresponds to the ["task"] in line 23.


# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request,"tasks/index.html",{
        "tasks": request.session["tasks"]
    })

def add_task(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task] #explanation below why append does not work
            return HttpResponseRedirect(reverse("tasks:index")) #redirects user back to list of tasks after he has submitted the form
        else:
            return render(request,"tasks/add_task.html",{
                "form": form
                })
    return render(request, "tasks/add_task.html", {
        "form": NewTaskForm()
    })


# The reason why it does not work is because django does not see that you have changed anything in the session by using the append() method on a list that is in the session.

# What you are doing here is essentially pulling out the reference to the list and making changes to it without the session backend knowing anything about it. An other way to explain:

# The append() method is on the list itself not on the session object
# When you call append() on the list you are only talking to the list and the list's parent (the session) has no idea what you guys are doing
# When you however do an assignment on the session itself session['whatever'] = 'something' then it knows that something is up and changes are made
# So the key here is that you need to operate on the session object directly if you want your changes to be updated automatically
# Django only thinks it needs to save a changed session item if the item got reassigned to the session. See here: django session base code the __setitem__ method containing a self.modified = True statement.

# The session['list'] += [new_element] adds a new list item (mutates the list so reference stays the same) and then gets it reassigned to the session -> thus triggering a __setitem__ call on the session and marking it as modified.

# The session['list'] = session['list'] + [new_item] mode of doing the same does create a new list every time it's run so its a bit less efficient, but you should not store hundreds of items in the session anyway. So you're probably fine. This also works exactly as above.

# However if you use sub-keys in the session like session['list']['x'] = 'whatever' the session will not see itself as modified so you need to mark it as by request.session.modified = True
