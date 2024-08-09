from django import forms
from .models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ["content", "tags", "media"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['media'].widget.attrs.update({'class': 'form-control-file'})

    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        if tags:
            return [tag.strip() for tag in tags.split(",")]
        return []

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if commit:
            instance.save()
            for tag_name in self.cleaned_data["tags"]:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
