from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=500)
    image = models.URLField(blank=True)
    listing_start_price = models.DecimalField(max_digits=10,decimal_places=2)
    current_price = None
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    watchers = models.ManyToManyField(User, blank=True, related_name="current_watchers")
    active = True

    def __str__(self) -> str:
        return f'{self.title}'

    def close(self):
        self.active = False

class Bids(models.Model):
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="item_name")
    bidder = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bidder")
    bid_price = models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self) -> str:
        return f'Bid of {self.bid_price} by {self.bidder}'

    def accept_bid(self):
        if self.item.current_price < self.bid_price:
            self.item.current_price = self.bid_price
            return True
        else:
            return False
