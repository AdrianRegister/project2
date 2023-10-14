from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    listing_name = models.CharField(max_length=64)
    starting_price = models.DecimalField(max_digits=6, decimal_places=2)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_description = models.TextField(max_length=5120, default="Default description")

    def __str__(self):
        return f"{self.id}: {self.listing_name}"

