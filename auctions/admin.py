from django.contrib import admin

from.models import Listing, Comment, Bid, Watchlist

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "item",  "description", "image", "category", "active", "creator")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "user" )

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "item",  "bid", "user")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)