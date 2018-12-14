from django.shortcuts import render, redirect
from django.http import JsonResponse
from apps.login.models import User
from .models import Post, PostLike, Comment, CommentLike


# Create your views here.
def wall(request, start=0, end=10):
    if 'user_id' not in request.session or 'username' not in request.session:
        return redirect('/login')

    posts = Post.objects.all().order_by('-created_on')[start:end]

    context = {
        'posts': posts,
    }
    print(posts)
    return render(request, 'wall/wall.html', context)


def create_post(request):
    # validate
    # TODO

    post = Post.objects.create(
        creator=User.objects.get(id=request.session['user_id']),
        textcontent=request.POST.get('post-content'))
    return redirect(wall)


def add_comment(request, post_id):
    # validate
    # TODO
    if request.method != "POST":
        return redirect('/')
    if not request.POST.get('comment-content'):
        return redirect('/')

    comment = Comment.objects.create(
        creator=User.objects.get(id=request.session['user_id']),
        textcontent=request.POST.get('comment-content'),
        post=Post.objects.get(id=int(post_id))
        )
    return redirect(wall)


def like_post(request, post_id):
    resp = {}
    post = Post.objects.filter(id=post_id)
    if len(post):
        post = post[0]
        user = User.objects.get(id=request.session.get('user_id'))
        if not len(PostLike.objects.filter(post=post, user=user)):
            PostLike.objects.create(post=post, user=user)
    else:
        resp['errors'] = "There was an error processing the like."
    
    resp['post-likes'] = [like.user.username for like in PostLike.objects.filter(post=post)]
    return JsonResponse(resp)


def like_comment(request, comment_id):
    resp = {}
    comment = Post.objects.filter(id=comment_id)
    if len(comment):
        comment = comment[0]
        user = User.objects.get(id=request.session.get('user_id'))
        if not len(CommentLike.objects.filter(comment=comment, user=user)):
            CommentLike.objects.create(comment=comment, user=user)
    else:
        resp['errors'] = "There was an error processing the like."
    
    resp['comment-likes'] = [like.user.username for like in PostLike.objects.filter(comment=comment)]
    return JsonResponse(resp)