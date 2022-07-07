from random import randint
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Name of new page"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Please input the content of the webpage using MARKDOWN only!"}))

class SearchExistingPage(forms.Form):
    search_term = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"search" , "placeholder": "Search Encyclopedia"}))

class EditExistingPage(forms.Form):
    title = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder": "Name of page"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Current contents"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_term": SearchExistingPage()
    })

def entry_page(request, entry):
    entry_details = util.get_entry(entry)
    if entry_details != None:
        return render(request, "encyclopedia/entry_page.html",{
        "entry_name": entry,
        "entry_details": entry_details,
        "search_term": SearchExistingPage()
        })
    else:
        related_entries = set()
        for filename in util.list_entries():
            if entry in filename:
                related_entries.add(filename)
        return render(request,"encyclopedia/errorpage.html",{
            "entry_name": entry,
            "related_entries": related_entries,
            "search_term": SearchExistingPage()
        })

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
        "form": NewPageForm(),
        "search_term": SearchExistingPage()
    })

def search(request):
    if request.method == "POST":
        search_term = SearchExistingPage(request.POST)
        if search_term.is_valid():
            entry_name = search_term.cleaned_data["search_term"]
            return entry_page(request, entry_name)
    else:
        return render(request, "encyclopedia/index.html", {
            "search_term": SearchExistingPage()
        })

def random(request):
    size_of_encyclopedia = len(util.list_entries())
    random_entry = randint(0,size_of_encyclopedia)
    chosen_entry = util.list_entries()[random_entry]
    return entry_page(request,chosen_entry)

def edit_page(request,entry):
    if request.method == "POST":
        edited_page_version = EditExistingPage(request.POST)
        if edited_page_version.is_valid():
            entry_title = edited_page_version.cleaned_data["title"]
            entry_content = edited_page_version.cleaned_data["content"]
            util.save_entry(entry_title,entry_content)
            return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[entry_title]))
        else:
            messages.error(request,"Something went wrong please look through the entry and try again!")
            return render(request,"encyclopedia/edit_page.html",{
                "entry":entry,
                "search_term": SearchExistingPage(),
                "complete_form": edited_page_version
            })
    current_contents = util.get_entry(entry)
    return render(request,"encyclopedia/edit_page.html",{
        "entry":entry,
        "search_term": SearchExistingPage(),
        "complete_form": EditExistingPage(initial={"title": entry, "content":current_contents}),
    })
        