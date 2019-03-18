from django import forms
from .models import Post, CoinAccount
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'title', 'text', 'audio_file', 'tag_list')
        labels = {
            'category': '카테고리',
            'title': '제목',
            'text': '내용',
            'audio_file': '첨부파일(오디오)',
            'tag_list': '해시태그',
        }

class CoinAccountForm(forms.ModelForm):

    class Meta:
        model = CoinAccount
        fields = ('address',)
        labels = {
            'address': '계좌번호',
        }