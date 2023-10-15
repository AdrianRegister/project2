from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AuctionListingForm
from .models import User, AuctionListing, Watchlist


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
    if request.method == 'POST':
        watchlist_item = Watchlist.objects.create(watchlist_owned_by=request.user, item_watched=listing) 
        watchlist_item.save()
        return redirect('my_watchlist')
                   
    return render(request, "auctions/listing_info.html", {
        "listing_name": listing_name,
        "listing": listing
    })

def my_watchlist(request):   
    if request.method == 'POST':
        watched_item_id = request.POST.get('watched_item_id')
        item_to_remove = Watchlist.objects.get(id=watched_item_id)
        item_to_remove.delete()
        return redirect(my_watchlist)

    return render(request, "auctions/my_watchlist.html", {
        "watched_items": Watchlist.objects.all()
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
