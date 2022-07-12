from django.contrib import admin

from .models import User, Listings, Bids, Comments, Category

# customise the admin view
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "date_joined", "last_login")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "listing_start_price","current_price", "current_bidder")
    filter_horizontal = ("past_bidders",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("commenter", "item")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "item", "bid_price")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listings, ListingAdmin)
admin.site.register(Bids, BidAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Category)