from django import forms
from .models import Confession

class ConfessionForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, initial=True, label="Submit anonymously")

    class Meta:
        model = Confession
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 10:
            raise forms.ValidationError("Confession must be at least 10 characters long.")
        return content

