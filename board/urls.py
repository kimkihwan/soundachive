from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.post_list, name='home'),
    path('board/<int:pk>/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('me/', views.my_info, name='my_info'),
    path('me/make', views.make_account, name='make_account'),
    #path('search/', views.post_search, name='post_search'),
]