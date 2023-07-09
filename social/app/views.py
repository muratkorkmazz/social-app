from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Post


def get_like_count_and_like_flag(request, posts):
    like_count = [len(post.liked_by.all()) for post in posts]
    if request.user.is_authenticated:
        like_flag = [request.user in post.liked_by.all() for post in posts]
    else:
        like_flag = [''] * len(posts)
    return like_count, like_flag


def index(request):
    posts = Post.objects.order_by("-posted_at").all()
    like_count, like_flag = get_like_count_and_like_flag(request, posts)

    data = list(zip(posts , like_count, like_flag))
    paginator = Paginator(data, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/index.html', {
        'page_obj': page_obj,
        "page_heading": "All Posts"
    })


def user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except:
        return JsonResponse({"error": "User not found."}, status=404)     
    posts = Post.objects.filter(poster=user).order_by("-posted_at").all()
    like_count, like_flag = get_like_count_and_like_flag(request, posts)
    data = list(zip(posts , like_count, like_flag))
    paginator = Paginator(data, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "app/index.html", {
        'page_obj': page_obj,
        "member" : user,
        "follower_count" : user.follower.all().count(),
        "following_count" : user.following.all().count(),
        "followers" : [follower.username for follower in user.follower.all()],
        "page_heading" : f"All posts from {user.username}"
    })



@csrf_exempt
@login_required(login_url='login')
def add_remove_follower(request, user_id):    
    if request.method == "PUT":
        try:
            user = User.objects.get(pk=user_id)
        except:
            return JsonResponse({"error": "User not found."}, status=404)
        data = json.loads(request.body)
        follower_id = int(data.get("follower_id"))
        try:
            follower = User.objects.get(pk=follower_id)
        except:
            return JsonResponse({"error": "User not found."}, status=404)
        if follower not in user.follower.all():
            user.follower.add(follower)
        else:
            user.follower.remove(follower)
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": " PUT request required."
        }, status=400)


@login_required(login_url='login')
def following(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except:
        return JsonResponse({"error": "User not found."}, status=404)
    posts = Post.objects.filter(poster__in = user.following.all()).order_by("-posted_at").all()
    like_count, like_flag = get_like_count_and_like_flag(request, posts)
    """  
    return render(request, "network/index.html", {
        "data": zip(posts , like_count, like_flag),
        "page_heading": f"Posts from people followed by {user.username}"
    })
    """
    data = list(zip(posts , like_count, like_flag))
    paginator = Paginator(data, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "app/index.html", {
        'page_obj': page_obj,
        "page_heading": f"Posts from people followed by {user.username}"
    })




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        try:
         username = request.POST["username"]
         password = request.POST["password"]
        except:
             return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"]
        except:
            return render(request, "app/register.html", {
                "message": "Invalid input."
            })

        # check if password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")


# api routes 1
@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        text = request.POST['text']
        post = Post(poster=request.user, text=text)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/create.html")


# api route 2
@csrf_exempt
@login_required(login_url='login')
def post(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
        except:
            return JsonResponse({"error": "Post not found."}, status=404)
        data = json.loads(request.body)
        if data.get("user_id") is not None:
            user_id = int(data.get("user_id"))
            try:
                user = User.objects.get(pk=user_id)
            except:
                return JsonResponse({"error": "User not found."}, status=404)
            if user not in post.liked_by.all():
                post.liked_by.add(user)
            else:
                post.liked_by.remove(user)
            post.save()
            return HttpResponse(status=204)
        if data.get("new_content") is not None:
            new_content = data.get("new_content")
            post.text = new_content
            post.save()
            return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": " PUT request required."
        }, status=400)


