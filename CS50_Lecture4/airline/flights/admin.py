from django.contrib import admin

from .models import Flight,Airport,Passenger

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id","origin","destination","duration")
#in the above class we are just configuring the flight admin interface

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)


admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin) # this means register the flight but use FlightAdmin settings
admin.site.register(Passenger, PassengerAdmin)