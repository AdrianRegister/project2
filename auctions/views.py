from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AuctionListingForm, ListingBidForm, ListingCommentForm
from .models import User, AuctionListing, Watchlist, ListingBid, ListingComment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })

@login_required
def create_listing(request):
    errors = None
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            form.instance.listed_by = request.user
            form.save()
            return redirect('index')
        else:
            errors = form.errors
    else:
        form = AuctionListingForm()        

    return render(request, "auctions/create_listing.html", {
        "form": form,
        "errors": errors
    })

def listing_info(request, listing_name):
    listing = AuctionListing.objects.get(listing_name=listing_name)
    highest_bid = ListingBid.objects.filter(for_listing=listing).order_by('-bid_amount').first()
    comments = ListingComment.objects.filter(on_listing=listing)
    if not highest_bid == None:
        highest_bidder = highest_bid.bidder_name
    else:
        highest_bidder = None   

    if request.method == 'POST':
        if 'add_to_watchlist' in request.POST:
            watchlist_item = Watchlist.objects.create(watchlist_owned_by=request.user, item_watched=listing) 
            watchlist_item.save()
            return redirect('my_watchlist')
        elif 'close_auction' in request.POST:
            listing.is_closed = True
            listing.save()       
    else:
        comment_form = ListingCommentForm()

    return render(request, "auctions/listing_info.html", {
        "listing_name": listing_name,
        "listing": listing,
        "highest_bidder": highest_bidder,
        "form": comment_form,
        "comments": comments
    })

def create_comment(request, listing_name):
    listing = AuctionListing.objects.get(listing_name=listing_name)
    if request.method == 'POST':
        comment_form = ListingCommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.made_by = request.user
            comment_form.instance.on_listing = listing
            comment_form.save()        
    else:
        comment_form = ListingCommentForm()    
    return render(request, 'auctions/create_comment.html', {
        "comment_form": comment_form,
        "listing": listing
    })

def my_watchlist(request):   
    if request.method == 'POST':
        watched_item_id = request.POST.get('watched_item_id')
        item_to_remove = Watchlist.objects.get(id=watched_item_id)
        item_to_remove.delete()
        return redirect('my_watchlist')

    return render(request, "auctions/my_watchlist.html", {
        "watched_items": Watchlist.objects.filter(watchlist_owned_by=request.user)
    })

@login_required
def bidding_page(request, listing_name):
    error_message = None
    success_message = None
    listing = AuctionListing.objects.get(listing_name=listing_name)
    if request.method == 'POST':
        bid_form = ListingBidForm(request.POST)
        bid_form.instance.bidder_name = request.user
        bid_form.instance.for_listing = listing
        if bid_form.is_valid():
            bid_amount = bid_form.cleaned_data['bid_amount']
            if listing.starting_price < bid_amount  and bid_amount > listing.current_price:
                listing.current_price = bid_amount
                bid_form.save()
                listing.save()
                success_message = "Bid placed successfully!"
            else:
                error_message = "Please ensure your bid amount is higher than the current price!"
    else:
        bid_form = ListingBidForm()

    return render(request, "auctions/bidding_page.html", {
        "listing": listing,
        "bid_form": bid_form,
        "error_message": error_message,
        "success_message": success_message
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
