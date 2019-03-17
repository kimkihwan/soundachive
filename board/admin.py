from django.contrib import admin
from .models import Post, Category, Tag, CoinAccount

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(CoinAccount)