from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=500)
    image = models.URLField(blank=True)
    seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="selling_items")
    listing_start_price = models.DecimalField(decimal_places=2,max_digits=10)
    current_price = models.DecimalField(default=0,decimal_places=2,max_digits=10)
    current_bidder = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="currently_winning_item")
    past_bidders = models.ManyToManyField(User, blank=True, related_name="past_bids")
    watchers = models.ManyToManyField(User, blank=True, related_name="watching_item")
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.title}'

    def set_seller(self,user):
        self.seller = user
    
    def set_highest_bidder(self):
        if self.past_bidders:
            list_of_bidders = self.past_bidders.all()
            index = len(list_of_bidders)-1
            self.current_bidder = list_of_bidders[index]
            return self.current_bidder

    def set_price(self, price):
        self.current_price = price

    def close(self):
        self.active = False
        self.winner = self.current_bidder
        return self.winner

class Bids(models.Model):
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, related_name="bids_for_item")
    bidder = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name="bids_made")
    bid_price = models.DecimalField(decimal_places=2,max_digits=10)
    
    def __str__(self) -> str:
        return f'{self.item} bid'
    
    def set_bidder(self,user):
        self.bidder = user
    
    def set_item(self,item):
        self.item = item

    def get_bid_price(self):
        return self.bid_price

    def accept_bid(self, price):
        item_start_price = self.item.listing_start_price
        if max(item_start_price,price) < self.bid_price:
            return True
        else:
            return False
