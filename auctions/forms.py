from django.forms import ModelForm
from auctions.models import AuctionListing, ListingBid, ListingComment

class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        exclude = ["listed_by", "current_price", "is_closed"]

class ListingBidForm(ModelForm):
    class Meta:
        model = ListingBid
        fields = ["bid_amount"]

class ListingCommentForm(ModelForm):
    class Meta:
        model = ListingComment
        fields = ["comment_text"]
        