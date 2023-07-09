
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("users/<int:user_id>", views.user, name="user"),
    path("add_remove_follower/<int:user_id>", views.add_remove_follower, name="add_remove_follower"),
    path("following/<int:user_id>", views.following, name="following")
]
