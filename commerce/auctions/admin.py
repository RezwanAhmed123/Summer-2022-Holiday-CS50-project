from django.contrib import admin

from .models import User,Listings, Bids

# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Bids)