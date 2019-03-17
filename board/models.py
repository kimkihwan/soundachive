from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

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
        like_split = self.like_list.split(',')
        dislike_split = self.dislike_list.split(',')
        if new not in like_split :
            self.like_list += ','
            self.like_list += new
            self.like += 1
            self.save()
        if new in dislike_split :
            dislike_split.remove(new)
            self.dislike_list = ','.join(dislike_split)
            self.dislike -= 1
            self.save()

    def disliked(self, new):
        like_split = self.like_list.split(',')
        dislike_split = self.dislike_list.split(',')
        if new not in dislike_split :
            self.dislike_list += ','
            self.dislike_list += new
            self.dislike += 1
            self.save()
        if new in like_split :
            like_split.remove(new)
            self.like_list = ','.join(like_split)
            self.like -= 1
            self.save()

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