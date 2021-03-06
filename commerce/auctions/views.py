from django import forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bids, Listings, User, Comments, Category
from . import utils

#forms
class EditMyInfo(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(EditMyInfo, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name', 'password']

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'image', 'listing_start_price','category']

class EditListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'image', 'active', 'category']

class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['bid_price']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']

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
def user_info(request, user_id):
    user = User.objects.get(pk=user_id)
    user_bids = user.bids_made.all().order_by('-bid_price')
    temp_data = []
    temp_bids = []
    for bid in user_bids:
        if bid.item not in temp_data:
            temp_data.append(bid.item)
            temp_bids.append(bid)
    user_bids = temp_bids
    user_selling_items = user.selling_items.all()
    context = {
        "user":user,
        "user_bids": user_bids,
        "user_selling_items": user_selling_items
    }
    context = utils.is_current_user(request,user,context)
    return render(request, "auctions/userinfo.html", context)

@login_required
def edit_myinfo(request):
    if request.method == "POST":
        editform = EditMyInfo(request.POST, instance=request.user)
        if editform.is_valid():
            editform.save()
            return HttpResponseRedirect(reverse("userinfo", args=(request.user.id,)))
        else:
            return render(request,"auctions/edit_myinfo.html",{
                "editform":editform
            })
    user = request.user
    return render(request, "auctions/edit_myinfo.html",{
        "editform": EditMyInfo(instance = user)
    })

@login_required
def changepassword(request):
    if request.method == "POST":
        password_form = PasswordChangeForm(data=request.POST, user=request.user)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return HttpResponseRedirect(reverse("userinfo", args=(request.user.id,)))
        else:
            return render(request,"auctions/changepassword.html",{
                "password_form":password_form
            })
    user = request.user
    return render(request, "auctions/changepassword.html",{
        "password_form": PasswordChangeForm(user=user)
    })

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
    print(request.POST)
    if request.method == "POST":
        return bidding(request,item_id)
    item = Listings.objects.get(pk=item_id)
    item_bids = item.bids_for_item.all()
    utils.update_past_bidders(item, item_bids)
    item_bid_prices = [bid.get_bid_price() for bid in item_bids]
    if item_bid_prices:
        current_highest_bid = max(item_bid_prices)
        item.current_bidder = item.bids_for_item.get(bid_price=current_highest_bid).bidder
    else:
        current_highest_bid = 0
        item.current_bidder = None
    item.current_price = current_highest_bid
    item.save()
    is_winning = (item.current_bidder == request.user)
    is_seller = (item.seller == request.user)
    item_active = item.active
    number_of_bids = utils.get_number_of_unique_bidders(item.past_bidders.all())
    comments = item.item_comments.all()
    on_watchlist = (request.user in item.watchers.all())
    return render(request, "auctions/listing.html",{
        "listing": item,
        "bidding": NewBidForm(),
        "is_winning": is_winning,
        "is_seller": is_seller,
        "number_of_bids": number_of_bids,
        "comments": comments,
        "item_active": item_active,
        "on_watchlist": on_watchlist
    })

@login_required
def bidding(request,item_id):
    item = Listings.objects.get(pk=item_id)
    number_of_bids = utils.get_number_of_unique_bidders(item.past_bidders.all())
    if request.method == "POST":
        bidform = NewBidForm(request.POST)
        if bidform.is_valid():
            madebid = bidform.save(commit=False)
            user = request.user
            madebid.set_item(item)
            if madebid.accept_bid(item.current_price):
                madebid.set_bidder(user)
                item.current_price = madebid.get_bid_price()
                item.current_bidder = madebid.bidder
                item.past_bidders.add(item.current_bidder)
                madebid.save()
                item.save()
                message = "Congrats! Your bid is successful and you are the current bidder!"
                number_of_bids += 1
                return render(request, "auctions/bid_status.html", {
                    "listing":item,
                    "bidding": NewBidForm(),
                    "number_of_bids": number_of_bids,
                    "message": message
                })
            else:
                current_min_bid = max(item.listing_start_price,item.current_price)
                is_winning = (item.current_bidder == request.user)
                is_seller = (item.seller == request.user)
                comments = item.item_comments.all()
                on_watchlist = (request.user in item.watchers.all())
                message = f"You need a higher bid! The current minimum bid is ${current_min_bid}!"
                return render(request, "auctions/listing.html",{
                "listing": item,
                "bidding": bidform,
                "is_winning": is_winning,
                "is_seller": is_seller,
                "message": message,
                "number_of_bids": number_of_bids,
                "item_price": item.current_price,
                "comments": comments,
                "on_watchlist": on_watchlist
            })
    item.save()
    is_winning = (item.current_bidder == request.user)
    return render(request, "auctions/bid_status.html",{
        "listing": item,
        "bidding": NewBidForm(),
        "is_winning": is_winning,
        "number_of_bids": number_of_bids
    })

@login_required
def edit_listing(request, item_id):
    item = Listings.objects.get(pk=item_id)
    if request.method == "POST":
        listing_form = EditListingForm(request.POST, instance=item)
        if listing_form.is_valid():
            listing_form.save()
            return HttpResponseRedirect(reverse("listing", args=(item_id,)))
        else:
            return render(request, "auctions/edit_listing.html", {
                "listing_form": listing_form,
                "item": item
            })
    return render(request, "auctions/edit_listing.html", {
                "listing_form": EditListingForm(instance=item),
                "item": item
                })

@login_required
def add_to_watchlist(request, item_id):
    user = request.user
    item = Listings.objects.get(pk=item_id)
    if request.method == "POST":
        if request.POST['confirm']=='confirm':
            if user in item.watchers.all():
                item.watchers.remove(user)
            else:
                item.watchers.add(user)
        return HttpResponseRedirect(reverse("listing", args=(item_id,)))
    return render(request, "auctions/add_to_watchlist.html", {
        "item":item
    })

@login_required
def add_comment(request,item_id):
    item = Listings.objects.get(pk=item_id)
    if request.method == "POST":
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.set_commenter(request.user)
            comment.set_item(item)
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=(item.id,)))
        else:
            return render(request, "auctions/add_comment.html",{
                "item": item,
                "comment_form": comment_form
            })
    return render(request, "auctions/add_comment.html",{
        "item": item,
        "comment_form": NewCommentForm()
    })

@login_required
def category(request, name):
    category = Category.objects.get(category=name)
    items = category.item_category.all()
    return render(request, "auctions/category.html",{
        "category": category,
        "items":items
    })

def add_category(request):
    if request.method == "POST":
        categoryform = CategoryForm(request.POST)
        if categoryform.is_valid():
            categoryform.save()
            return HttpResponseRedirect(reverse(index))
        else:
            return render(request, "auctions/add_category.html",{
                "categoryform": CategoryForm,
            })
    return render(request, "auctions/add_category.html",{
                "categoryform": CategoryForm,
            })
