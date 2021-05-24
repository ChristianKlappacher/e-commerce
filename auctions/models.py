from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    categories = [
        "Collectibles & Art",
        "Electronics",
        "Fashion",
        "Home & Garden",
        "Motors",
        "Sport",
        "Toys & hobbies",
        "Other Catagories"
    ]
    categoryChoices = []
    for category in categories:
        categoryChoices.append((category, category))

    item = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=128, blank=True)
    category = models.CharField(
        max_length=64, choices=categoryChoices, blank=True)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    highestBid = models.DecimalField(decimal_places=2, max_digits=19)

    def __str__(self):
        return f"{self.item}"


class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=19)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
