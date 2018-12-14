from django.db import models
from apps.login.models import User


# Create your models here.
class Post(models.Model):
    creator = models.ForeignKey(User, related_name='posts')
    link = models.CharField(max_length=255, null=True)
    heading = models.CharField(max_length=100, null=True)
    textcontent = models.TextField(max_length=2000)
    imgurl = models.CharField(max_length=60, null=True)
    created_on = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Share(Post):
    original_post = models.ForeignKey(Post, related_name='shares')


class PostLike(models.Model):
    user = models.ForeignKey(User, related_name='postlikes')
    post = models.ForeignKey(Post, related_name='likes')
    created_on = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # obj.icon maps to Class.icons[obj.icon] as the index of the array
    icons = ['like', 'love', 'angry', 'drink']
    icon_fas = ['fas fa-thumbs-up', 'fas fa-kiss-wink-heart', 'fas fa-angry', 'fas fa-beer']


class Comment(models.Model):
    creator = models.ForeignKey(User, related_name='comments')
    post = models.ForeignKey(Post, related_name='comments')
    textcontent = models.TextField(max_length=2000)
    created_on = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class CommentLike(models.Model):
    user = models.ForeignKey(User, related_name='commentlikes')
    comment = models.ForeignKey(Comment, related_name='likes')
    icon = models.PositiveSmallIntegerField()
    created_on = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # obj.icon maps to Class.icons[obj.icon] as the index of the array
    icons = ['like', 'love', 'grabasnickers', 'grabadrink']
    icon_fas = ['fas fa-thumbs-up', 'fas fa-kiss-wink-heart', 'fas fa-angry', 'fas fa-beer']