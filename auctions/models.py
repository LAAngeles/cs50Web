from asyncio.windows_events import NULL
from operator import truediv
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    len_watchlist = models.IntegerField(null=True)
    userwatchlist = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.username}"


class New_Listings(models.Model):
    title        = models.CharField(max_length=30)
    description  = models.CharField(max_length=128)
    starting_bid = models.IntegerField(null=True)
    category     = models.CharField(max_length=21)
    URL_image    = models.URLField(blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user_listings")

    def __str__(self):
        return f"{self.user}, {self.title}, {self.description}, {self.starting_bid}, {self.category}"


class add_watchlist(models.Model):
    userwatchlist = models.IntegerField(null=True)
    title        = models.CharField(max_length=30)
    starting_bid = models.IntegerField(null=True)
    URL_image    = models.URLField(blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user_watchlist")

    def __str__(self):
        return f"{self.id}, {self.user}, {self.userwatchlist}, {self.title}, {self.starting_bid}"


class New_Coments(models.Model):
    coment = models.CharField(max_length=128)
    usercoment = models.IntegerField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user_Coments")

    def __str__(self):
        return f"{self.id}, {self.user}: coment = {self.usercoment}, usercoment = {self.coment}"


class New_bid(models.Model):
    user = models.CharField(max_length=30)
    Listings_id = models.IntegerField(null=True)
    bid = models.IntegerField(null=True)
    starting_bid = models.ForeignKey(New_Listings,null=True, on_delete=models.CASCADE, related_name="star_bid")
    userbid = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user_userbid")

    def __str__(self):
        return f"{self.id}: user = {self.userbid}, user = {self.user}, Listings_id = {self.Listings_id}"

class close_listing_action(models.Model):

    title        = models.CharField(max_length=30,null=True)
    description  = models.CharField(max_length=128,null=True)
    starting_bid = models.IntegerField(null=True)
    category     = models.CharField(max_length=21,null=True)
    URL_image    = models.URLField(blank=True)
    user = models.CharField(max_length=30,null=True)

    userbid = models.CharField(max_length=30,null=True)
    Listings_id = models.IntegerField(null=True)
    bid = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.Listings_id}: {self.title}, {self.user}, {self.starting_bid}, {self.bid}"