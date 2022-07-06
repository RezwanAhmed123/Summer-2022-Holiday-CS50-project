from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Name of new page"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Please input the content of the webpage using MARKDOWN only!"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    entry_details = util.get_entry(entry)
    if entry_details != None:
        return render(request, "encyclopedia/entry_page.html",{
        "entry_name": entry,
        "entry_details": entry_details
        })
    else:
        return render(request,"encyclopedia/errorpage.html")

def errorpage(request):
    return render(request, "encyclopedia/errorpage.html")

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_content = form.cleaned_data["content"]
            if util.get_entry(entry_title):
                messages.error(request,"That page already exists, please find the page accordingly!")
            else:
                util.save_entry(entry_title,entry_content)
                return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[entry_title]))
        return render(request,"encyclopedia/newpage.html",{
                "form": form
                })
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })