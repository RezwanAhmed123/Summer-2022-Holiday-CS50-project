from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


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