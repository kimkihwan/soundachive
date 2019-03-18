from django import forms
from .models import Post, CoinAccount
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'title', 'text', 'audio_file', 'tag_list')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'enter title here'}),
            'text': forms.Textarea(attrs={'placeholder': 'enter description here'}),
            'tag_list': forms.TextInput(attrs={'placeholder': '#add #hashtag #freely'}),
        }
        labels = {
            'category': 'Category',
            'title': 'Title',
            'text': 'Description',
            'audio_file': 'Audio file',
            'tag_list': '#hashtag',
        }

class CoinAccountForm(forms.ModelForm):

    class Meta:
        model = CoinAccount
        fields = ('address',)
        labels = {
            'address': 'Account address',
        }