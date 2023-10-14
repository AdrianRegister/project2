from django.forms import ModelForm
from auctions.models import AuctionListing

class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        exclude = ["listed_by"]

