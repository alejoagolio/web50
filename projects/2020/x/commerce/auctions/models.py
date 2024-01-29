from django.contrib.auth.models import AbstractUser
from django.db import models


CATEGORY_CHOICES = [
        ('Other', 'Other'),
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        ('Home and Garden', 'Home and Garden'),
        ('Sports and Outdoors', 'Sports and Outdoors'),
        ('Toys and Games', 'Toys and Games'),
        ('Beauty and Health', 'Beauty and Health'),
        ('Automotive', 'Automotive'),
        ('Furniture', 'Furniture'),
        ('Music and Instruments', 'Music and Instruments'),
        ('Collectibles and Art', 'Collectibles and Art'),
        ('Pets', 'Pets'),
        ('Food and Beverages', 'Food and Beverages'),   
    ]

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True,related_name="watchlisted_by")
    

class Listing(models.Model):

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_listings")
    current_winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="currently_winning")
    watchlist_users = models.ManyToManyField(User, blank=True,related_name='watchlist_listings')

    def __str__(self):
        return self.title

class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bid on {self.listing.title} by {self.bidder.username}"


class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.listing.title} by {self.commenter.username}'