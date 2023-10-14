from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    listing_name = models.CharField(max_length=64)
    starting_price = models.DecimalField(max_digits=6, decimal_places=2)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_description = models.TextField(max_length=5120)

    def __str__(self):
        return f"{self.id}: {self.listing_name}"

class ListingBid(models.Model):
    bid_amount = models.DecimalField(max_digits=6, decimal_places=2)
    for_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bidder_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.bid_amount} on {self.for_listing}"

class ListingComment(models.Model):
    comment_text = models.TextField(max_length=1024)
    on_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    made_by = models.ForeignKey(User, on_delete=models.CASCADE)