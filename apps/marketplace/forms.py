from django import forms
from .models import MarketplaceItem


class MarketplaceItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ["title", "description", "price", "image"]


class MarketplaceFilterForm(forms.Form):
    search = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    sort_by = forms.ChoiceField(
        choices=[
            ("-created_at", "Newest"),
            ("created_at", "Oldest"),
            ("price", "Price Low to High"),
            ("-price", "Price High to Low"),
            ("title", "Title A-Z"),
            ("-title", "Title Z-A"),
        ],
        required=False,
    )
