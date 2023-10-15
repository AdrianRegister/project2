from django.forms import ModelForm
from auctions.models import AuctionListing, ListingBid

class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        exclude = ["listed_by"]

class ListingBidForm(ModelForm):
    class Meta:
        model = ListingBid
        fields = ["bid_amount"]