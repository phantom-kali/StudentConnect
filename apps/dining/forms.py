from django import forms
from .models import DiningHallReview

class DiningHallReviewForm(forms.ModelForm):
    class Meta:
        model = DiningHallReview
        fields = ['rating', 'comment']