from django.contrib import admin

from .models import User, Listings, Bids, Comments, Category

# customise the admin view
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "date_joined", "last_login")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "current_bidder", "current_price")
    filter_horizontal = ("category",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("commenter", "item")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "item", "bid_price")

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listings, ListingAdmin)
admin.site.register(Bids, BidAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Category, CategoryAdmin)