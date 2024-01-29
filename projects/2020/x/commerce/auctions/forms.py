from django import forms
from .models import *

class ListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.DecimalField(min_value=0.01, max_digits=10, decimal_places=2)
    img_url = forms.URLField(required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

class CommentForm(forms.Form):
    text = forms.CharField()

class BidForm(forms.Form):
    amount = forms.CharField()