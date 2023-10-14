from django.forms import ModelForm
from auctions.models import AuctionListing

class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["listing_name", "starting_price", "listing_description"]

