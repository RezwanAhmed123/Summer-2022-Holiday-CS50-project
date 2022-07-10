from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bids, Listings, User

#forms
class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'image', 'listing_start_price']

class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['bid_price']
    

#views
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
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

@login_required
def new_listing(request):
    if request.method == "POST":
        new_listing_form = NewListingForm(request.POST)
        if new_listing_form.is_valid():
            new_listing = new_listing_form.save(commit=False)
            user = request.user
            new_listing.set_seller(user)
            new_listing.save()
            return HttpResponseRedirect(reverse("listing", args=(new_listing.id,)))
        else:
            return render(request, "auctions/newlisting.html",{
                "form": new_listing_form,
                "message": "Something went wrong please look over and complete the form correctly"
            })
    return render(request,"auctions/newlisting.html", {
        "form": NewListingForm()
    })

@login_required
def listing(request, item_id):
    if request.method == "POST":
        return bidding(request,item_id)
    item = Listings.objects.get(pk=item_id)
    item_bids = [bid.get_bid_price() for bid in item.bids_for_item.all()]
    if item_bids:
        current_highest_bid = max(item_bids)
    item.current_price = current_highest_bid
    item.save()
    return render(request, "auctions/listing.html",{
        "listing": item,
        "bidding": NewBidForm()
    })

@login_required
def bidding(request,item_id):
    if request.method == "POST":
        bidform = NewBidForm(request.POST)
        if bidform.is_valid():
            madebid = bidform.save(commit=False)
            item = Listings.objects.get(pk=item_id)
            item_bids = [bid.get_bid_price() for bid in item.bids_for_item.all()]
            if item_bids:
                current_highest_bid = max(item_bids)
            else:
                current_highest_bid = 0
            madebid.set_item(item)
            user = request.user
            if madebid.accept_bid(current_highest_bid):
                madebid.set_bidder(user)
                item.current_price = madebid.get_bid_price()
                madebid.save()
                item.save()
                return render(request, "auctions/listing.html", {
                    "listing":item,
                    "bidding": NewBidForm()
                })
            else:
                return render(request, "auctions/listing.html",{
                "listing": item,
                "bidding": bidform,
                "message": "You need a higher bid!",
                "item_price": item.current_price
            })
        