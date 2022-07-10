from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=500)
    image = models.URLField(blank=True)
    listing_start_price = models.DecimalField(decimal_places=2,max_digits=10)
    current_price = models.DecimalField(default=0,decimal_places=2,max_digits=10)
    seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="seller")
    watchers = models.ManyToManyField(User, blank=True, related_name="current_watchers")
    active = True

    def __str__(self) -> str:
        return f'{self.title}'

    def set_seller(self,user):
        self.seller = user

    def set_price(self, price):
        self.current_price = price

    def close(self):
        self.active = False

class Bids(models.Model):
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, related_name="bid_for_item")
    bidder = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name="bid_made")
    bid_price = models.DecimalField(decimal_places=2,max_digits=10)
    
    def __str__(self) -> str:
        return f'{self.item} bid'
    
    def set_bidder(self,user):
        self.bidder = user
    
    def set_item(self,item):
        self.item = item

    def get_bid_price(self):
        return self.bid_price

    def accept_bid(self, item):
        if (item.listing_start_price < self.bid_price) and (item.current_price<self.bid_price):
            return True
        else:
            return False
