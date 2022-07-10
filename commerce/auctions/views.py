from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Listings, User

#forms
class NewListingForm(forms.Form):
    title = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"Name of item"}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Please provide a short description of the item here"}))
    image = forms.URLField(required=False)
    listing_start_price = forms.FloatField(help_text="Input starting price")

#views
@login_required(login_url="auctions/login.html")
def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="auctions/login.html")
def new_listing(request):
    if request.method == "POST":
        new_listing_form = NewListingForm(request.POST)
        if new_listing_form.is_valid():
            new_listing = Listings()
            new_listing.title = new_listing_form.cleaned_data["title"]
            new_listing.description = new_listing_form.cleaned_data["description"]
            new_listing.image = new_listing_form.cleaned_data["image"]
            new_listing.listing_start_price = new_listing_form.cleaned_data["listing_start_price"]
            user = request.user
            new_listing.seller = user.id
            new_listing.save()
            new_listing_id = new_listing.id
            return HttpResponseRedirect(reverse("listing"), args=(new_listing_id))
        else:
            return render(request, "auctions/newlisting.html",{
                "form": new_listing_form,
                "message": "Something went wrong please look over and complete the form correctly"
            })
    return render(request,"auctions/newlisting.html", {
        "form": NewListingForm()
    })

@login_required(login_url="auctions/login.html")
def listing(request, item_id):
    item = Listings.objects.get(pk=item_id)
    return render(request, "auctions/listing.html",{
        "listing": item
    })
