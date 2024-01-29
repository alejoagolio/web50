from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, Listing, Bids, Comments
from .forms import *
from .models import User


def index(request):
    listings_list = Listing.objects.filter(active=True).order_by('-created_at')
    paginator = Paginator(listings_list, 3) 

    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    return render(request, 'auctions/index.html', {'listings': listings})


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

def watchlist(request):
    user = request.user
    watchlist_list = user.watchlist.all()
    paginator = Paginator(watchlist_list, 3)

    page = request.GET.get('page')
    try:
        watchlist = paginator.page(page)
    except PageNotAnInteger:
        watchlist = paginator.page(1)
    except EmptyPage:
        watchlist = paginator.page(paginator.num_pages)

    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist})

def categories0(request):
    cats = []
    for category in CATEGORY_CHOICES:
        cats.append(category[0])
    return render(request, 'auctions/categories.html', {'categories': cats})

def categories1(request, category):
    listings_list = Listing.objects.filter(category=category).order_by('-created_at')
    paginator = Paginator(listings_list, 3) 

    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    return render(request, 'auctions/categories1.html', {
        'listings': listings,
        'category': category
        })

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    wl = False

    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        wl = listing in watchlist

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "wl": wl
    })
        
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = Decimal(form.cleaned_data['starting_bid'])
            img_url = form.cleaned_data['img_url']
            category = form.cleaned_data['category']
            creator = request.user
            new_listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=img_url, category=category, creator=creator)
            new_listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Unable to create listing, check your inputs')
            return HttpResponseRedirect(reverse('create'))
    else:
        form = ListingForm()
        return render(request, "auctions/create.html", {
            'form': form,
            })

@login_required
def edit_wl(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    user = request.user
    watchlist = user.watchlist.all()
    if listing in watchlist:
        user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        user.watchlist.add(listing)
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    
@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            listing = get_object_or_404(Listing, pk=listing_id)
            text = form.cleaned_data["text"]
            commenter = request.user
            new_comment = Comments(listing=listing, commenter=commenter, text=text)
            new_comment.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            listing = get_object_or_404(Listing, pk=listing_id)
            current_bid = listing.current_bid
            starting_bid = listing.starting_bid
            bidder = request.user
            try:
                amount = Decimal(form.cleaned_data["amount"])
            except:
                messages.error(request, 'Bid unsuccessful. Please check your bid amount.')
                return HttpResponseRedirect(reverse('listing', args=[listing_id]))
            if amount > current_bid and amount >= starting_bid:
                new_bid = Bids(listing=listing, bidder=bidder, amount=amount)
                new_bid.save()
                listing.current_bid = amount
                listing.current_winner = bidder
                listing.save()
                messages.success(request, 'Bid successful!')
            else:
                messages.error(request, 'Bid unsuccessful. Please check your bid amount.')
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        
@login_required
def close(request, listing_id):
    listing = listing = get_object_or_404(Listing, pk=listing_id)
    if listing.current_winner != None:
        listing.winner = listing.current_winner
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse('index'))

