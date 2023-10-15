from django.contrib import admin
from .models import AuctionListing, ListingBid, ListingComment, Watchlist

# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(ListingBid)
admin.site.register(ListingComment)
admin.site.register(Watchlist)