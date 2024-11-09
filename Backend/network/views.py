from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator 
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

def index(request):
    post_list = Post.objects.all().order_by('-time')

    new_type = []
    for post in post_list:
        is_liked = post.likes.filter(id=request.user.id).exists()
        new_type.append({"post": post, "is_liked": is_liked})

    paginator = Paginator(new_type, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/index.html', {'page_obj': page_obj})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            network = Network(user=user)
            user.save()
            network.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@login_required
def create_post(request):
    print('create_post called')
    if request.method == "POST":
        content = request.POST["content"]
        poster = request.user
        post = Post(poster=poster,content=content)
        post.save()
        print(post.time)
        return HttpResponseRedirect(reverse("index"))
    else :
        return HttpResponseRedirect(reverse("index"))

def view_profile(request, username):
    print('view_profile called')
    print(username)

    user = User.objects.get(username=username)
    network = Network.objects.get(user=user)
    
    followers = network.followers
    followers_count = followers.count()

    following = user.following
    following_count = following.count()

    others_profile = True
    others_profile_follow = True

    if user == request.user:
        others_profile = False
    else:
        print('alive')
        # has to use the id / primary key
        if followers.filter(pk=request.user.pk).exists():
            others_profile_follow = False
        print('dead')

    user_post = Post.objects.filter(poster=user).order_by('-time')

    new_type = []
    for post in user_post:
        is_liked = post.likes.filter(id=request.user.id).exists()
        new_type.append({"post": post, "is_liked": is_liked})

    paginator = Paginator(new_type, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "network" : network, 
        "followers_count" : followers_count,
        "following_count" : following_count,
        "others_profile" : others_profile,
        "others_profile_follow" : others_profile_follow,
        'page_obj': page_obj
    })

@login_required
def press_follow(request, username):
    user = User.objects.get(username=username)
    network = Network.objects.get(user=user)
    network.followers.add(request.user) # use add instead of append
    network.save()

    # redirect instead of calling view_profile direct so that the link stays at the profile
    return redirect(reverse('view_profile', args=[username]))

@login_required
def press_unfollow(request, username):
    user = User.objects.get(username=username)
    network = Network.objects.get(user=user)
    network.followers.remove(request.user)
    network.save()

    return redirect(reverse('view_profile', args=[username]))

@login_required
def following(request):
    user = request.user
    posts = []
    all_post = Post.objects.all()
    following_list = user.following.all()

    for item in following_list:
        person = item.user
        current_post = all_post.filter(poster=person)
        posts.extend(current_post)

    posts = sorted(posts, key=lambda post: post.time, reverse=True)

    new_type = []
    for post in posts:
        is_liked = post.likes.filter(id=request.user.id).exists()
        new_type.append({"post": post, "is_liked": is_liked})

    paginator = Paginator(new_type, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html', {'page_obj': page_obj})

@require_http_methods(["POST"])
def save_post(request):
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        content = data.get('content')

        if not content:
            return JsonResponse({
                'status': 'error',
                'message': 'Content cannot be empty.'
            }, status=400)

        try:
            post = Post.objects.get(id=post_id, poster=request.user)
        except Post.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Post not found or you do not have permission to edit it.'
            }, status=404)

        post.content = content
        post.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Post saved successfully.'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_http_methods(["POST"])
def like_post(request):
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Post not found or you do not have permission to edit it.',
            }, status=404)

        post.likes.add(request.user)
        post.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Post saved successfully.',
            'likes_count' : post.likes.count()
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@require_http_methods(["POST"])
def unlike_post(request):
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Post not found or you do not have permission to edit it.',
            }, status=404)

        post.likes.remove(request.user)
        post.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Post saved successfully.',
            'likes_count' : post.likes.count()
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
   