from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    post_count = models.IntegerField(default=0)

    def refresh_count(self):
        posts = Post.objects.filter(category__exact=self.id)
        self.post_count = len(posts)
        self.save()

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    post_id_list = models.TextField(blank=True)
    post_count = models.IntegerField(default=0)

    def is_post_listed(self,post):
        post_id_split = list(filter(None, self.post_id_list.split('#')))
        if post in post_id_split :
            return True
        else :
            return False

    def add_post(self,post):
        new = '#'+post
        self.post_id_list += new
        self.post_count += 1
        self.save()
    
    def refresh_count(self):
        post_id_split = list(filter(None, self.post_id_list.split('#')))
        for post in post_id_split :
            try:
                old = Post.objects.get(id__exact=int(post))
                if not old.is_tag_listed(self.name):
                    post_id_split.remove(post)
            except Post.DoesNotExist:
                post_id_split.remove(post)
        self.post_id_list = '#'+'#'.join(post_id_split)
        self.post_count = len(post_id_split)
        self.save()

    def get_posts(self):
        self.refresh_count()
        post_id_split = list(filter(None, self.post_id_list.split('#')))
        posts = Post.objects.filter(id__in=post_id_split).order_by('-like')
        return posts

    def __str__(self):
        return self.name


def upload_audio(instance, filename):
    return 'board/%s/%s/%s' % (instance.author, str(timezone.localtime()).replace(':',''), filename)

class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey('board.Category', related_name='posts', default=0, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    audio_file = models.FileField(blank=True, upload_to=upload_audio)
    created_date = models.DateTimeField(default=timezone.localtime)
    published_date = models.DateTimeField(blank=True, null=True)

    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    like_list = models.TextField(blank=True)
    dislike_list = models.TextField(blank=True)
    tag_list = models.TextField(blank=True)

    def publish(self):
        self.published_date = timezone.localtime()
        self.save()

    def liked(self, new):
        like_split = list(filter(None, self.like_list.split(',')))
        dislike_split = list(filter(None, self.dislike_list.split(',')))
        if new in like_split :
            like_split.remove(new)
            self.like_list = ','.join(like_split)
            self.like -= 1
        else :
            if len(like_split) > 0 :
                self.like_list += ','
            self.like_list += new
            self.like += 1
        if new in dislike_split :
            dislike_split.remove(new)
            self.dislike_list = ','.join(dislike_split)
            self.dislike -= 1
        self.save()

    def disliked(self, new):
        like_split = list(filter(None, self.like_list.split(',')))
        dislike_split = list(filter(None, self.dislike_list.split(',')))
        if new in dislike_split :
            dislike_split.remove(new)
            self.dislike_list = ','.join(dislike_split)
            self.dislike -= 1
        else :
            if len(dislike_split) > 0 :
                self.dislike_list += ','
            self.dislike_list += new
            self.dislike += 1
        if new in like_split :
            like_split.remove(new)
            self.like_list = ','.join(like_split)
            self.like -= 1
        self.save()

    def add_tag(self):
        tag_split = list(filter(None, self.tag_list.split('#')))
        formatted_list = ''
        for i in range(len(tag_split)) :
            tag_split[i] = tag_split[i].strip()
            try:
                old = Tag.objects.get(name__exact=tag_split[i])
                if not old.is_post_listed(str(self.id)) :
                    old.add_post(str(self.id))
            except Tag.DoesNotExist:
                new = Tag(name=tag_split[i])
                new.add_post(str(self.id))
            formatted_list += '#'+tag_split[i]+' '
        self.tag_list = formatted_list
        self.save()

    def is_tag_listed(self,tag):
        tag_split = list(filter(None, self.tag_list.split('#')))
        tag += ' '
        if tag in tag_split :
            return True
        else :
            return False
        
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('board.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return self.text

class CoinAccount(models.Model):
    owner = models.OneToOneField('auth.User', related_name='coinaccount', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    deposit = models.IntegerField(default=0)

    def set_deposit(self, amount):
        self.deposit = amount
        self.save()

    def get_deposit(self):
        return self.deposit

    def __str__(self):
        return self.address