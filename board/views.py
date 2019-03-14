from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Category, CoinAccount
from .forms import PostForm, CoinAccountForm

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def post_list(request, pk=0):
    categories = Category.objects.all().order_by('id')
    if pk > 0:
        selected_category = Category.objects.get(id__exact=pk)
        posts = Post.objects.filter(category__exact=selected_category).order_by('-created_date')
    else:
        selected_category = 0
        posts = Post.objects.all().order_by('-created_date')
    return render(request, 'board/post_list.html', {'posts': posts, 'categories': categories, 'selected_category':selected_category})

def post_detail(request, pk):
    categories = Category.objects.all().order_by('id')
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'board/post_detail.html', {'post': post, 'categories': categories})

# def post_search(request):
#     return null

@login_required
def post_new(request):
    categories = Category.objects.all().order_by('id')
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.localtime()
            post.save()
            return redirect('board:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'board/post_edit.html', {'form': form, 'categories': categories})

@login_required
def post_edit(request, pk):
    categories = Category.objects.all().order_by('id')
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.localtime()
            post.save()
            return redirect('board:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_edit.html', {'form': form, 'categories': categories})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('board:post_list')

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.liked()
    return redirect('board:post_detail', pk=post.pk)

@login_required
def my_info(request):
    categories = Category.objects.all().order_by('id')
    my_posts = Post.objects.filter(author__exact=request.user).order_by('-created_date')
    my_score = 0
    for post in my_posts:
        my_score += post.like
    try:
        my_account = CoinAccount.objects.get(owner__exact=request.user)
    except CoinAccount.DoesNotExist:
        my_account = 0
    # if request.method == "POST":

    return render(request, 'board/my_info.html', {'my_account': my_account, 'my_posts': my_posts, 'my_score': my_score, 'categories': categories})

@login_required
def make_account(request):
    categories = Category.objects.all().order_by('id')
    my_account = CoinAccount(owner=request.user,address='JUST_SOME_ADDRESS')
    my_account.save()
    my_posts = Post.objects.filter(author__exact=request.user).order_by('-created_date')
    my_score = 0
    for post in my_posts:
        my_score += post.like
    # todo: 가상화폐 연동
    return render(request, 'board/my_info.html', {'my_account': my_account, 'my_posts': my_posts, 'my_score': my_score, 'categories': categories})
