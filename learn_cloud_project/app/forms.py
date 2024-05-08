from app.models import Posts
from django import forms


class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ("skill_name",)
        labels = {"skill_name": "学びたいこと"}
