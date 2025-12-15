# blog/forms.py

from django import forms
from .models import Post, Comment, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    # Comma-separated list of tags
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated list of tags (e.g. django, python, web)."
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]  # add any other fields you use

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # When editing, pre-fill tags with existing names
        if self.instance.pk:
            current_tags = self.instance.tags.all().values_list("name", flat=True)
            self.fields["tags"].initial = ", ".join(current_tags)

    def save(self, commit=True):
        instance = super().save(commit=commit)

        # Handle tags
        tags_str = self.cleaned_data.get("tags", "")
        tag_names = [
            name.strip().lower()
            for name in tags_str.split(",")
            if name.strip()
        ]

        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        # Set tags after instance exists
        if commit:
            instance.tags.set(tags)
        else:
            # if commit=False, caller must call save_m2m()
            instance._pending_tags = tags

        return instance

    def save_m2m(self):
        """
        If using commit=False in views, this ensures M2M tags are saved.
        """
        if hasattr(self.instance, "_pending_tags"):
            self.instance.tags.set(self.instance._pending_tags)
            del self.instance._pending_tags


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")
