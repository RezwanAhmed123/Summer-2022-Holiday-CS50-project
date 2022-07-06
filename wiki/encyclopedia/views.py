from turtle import title
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    entry_details = util.get_entry(entry)
    return render(request, "encyclopedia/entry_page.html",{
        "entry_name": entry,
        "entry_details": entry_details
    })
