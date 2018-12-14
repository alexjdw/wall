from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^create$', views.create),
    url(r'^submit$', views.login_submit),
    url(r'^logout', views.logout)
]
