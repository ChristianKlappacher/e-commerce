from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from .models import User, Listing, Bid, Comment, Watchlist


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["item", "image", "description", "category"]
        widgets = {
            "description": Textarea(attrs={"cols": 80, "rows": 3}),
        }


class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": Textarea(attrs={"cols": 80, "rows": 3}),
        }


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True).all()
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


@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        bidForm = NewBidForm(request.POST)
        if form.is_valid() and bidForm.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            bid = bidForm.save(commit=False)
            bid.user = request.user
            bid.item = listing
            listing.highestBid = bid.bid
            listing.save()
            bid.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse(status=400)
    else:
        return render(request, "auctions/create.html", {
            "form": NewListingForm(),
            "bidForm": NewBidForm()
        })


def listingPage(request, itemId):

    listing = Listing.objects.get(id=itemId)

    highestBid = Bid.objects.filter(
        item=listing).order_by('-bid')[0]
    # get the highest bid and updates the highest bid of the listing
    listing.highestBid = highestBid.bid
    listing.save()

    # attempt to get their Watchlist
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(item=listing, user=request.user)
    else:
        watchlist = []

    if request.method == "POST":

        # add/remove item to watchlist
        if request.POST.get("addWatchlist"):
            Watchlist.objects.create(item=listing, user=request.user).save()
        elif request.POST.get("removeWatchlist"):
            Watchlist.objects.filter(item=listing, user=request.user).delete()

        # process bid form
        elif request.POST.get("bid"):
            form = NewBidForm(request.POST)
            if form.is_valid() and form.cleaned_data["bid"] > listing.highestBid:
                bid = form.save(commit=False)
                bid.user = request.user
                bid.item = listing
                bid.save()
                listing.highestBid = bid.bid
                listing.save()
                return HttpResponseRedirect(reverse("listingPage", args=(itemId,)))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "watchlist": watchlist,
                    "form": NewBidForm(),
                    "highestBid": highestBid,
                    "comments": Comment.objects.filter(item=listing).all(),
                    "commentForm": NewCommentForm(),
                    "message": "Bid too low!"
                })

        # closes the Auction
        elif request.POST.get("closeAuction") and request.user == listing.creator:
            listing.active = False
            listing.save()

        elif request.POST.get("comment"):
            commentForm = NewCommentForm(request.POST)
            if commentForm.is_valid():
                comment = commentForm.save(commit=False)
                comment.user = request.user
                comment.item = listing
                comment = commentForm.save()
            return HttpResponseRedirect(reverse("listingPage", args=(itemId,)))

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "form": NewBidForm(),
        "highestBid": highestBid,
        "comments": Comment.objects.filter(item=listing).all(),
        "commentForm": NewCommentForm(),
    })


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user=request.user).all()
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.categories
    })


def categoryPage(request, category):
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category=category, active=True).all(),
        "category": category
    })
