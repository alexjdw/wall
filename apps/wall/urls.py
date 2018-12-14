from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.wall),
    url(r'^new-post$', views.create_post),
    url(r'^add-comment/(?P<post_id>[0-9]+)$', views.add_comment),
    url(r'^like-post/(?P<post_id>[0-9]+)', views.like_post)
]
