from django import forms
from .models import Post, CoinAccount
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'title', 'text', 'audio_file',)
        labels = {
            'category': '카테고리',
            'title': '제목',
            'text': '내용',
            'audio_file': '첨부파일(오디오)',
        }

class CoinAccountForm(forms.ModelForm):

    class Meta:
        model = CoinAccount
        fields = ('address',)
        labels = {
            'address': '계좌번호',
        }

# class UserInfoForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "email", "address")
#         labels = {
#             'first_name': '이름',
#             'last_name': '성',
#             'email': '이메일',
#             'address': '가상화폐 계좌',
#         }