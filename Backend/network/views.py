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
    return render(request, 'network/index.html')

def posts(request):
    post_list = Post.objects.all().order_by('-pinned', '-time')

    new_type = []
    for post in post_list:
        is_liked = post.likes.filter(id=request.user.id).exists()
        new_type.append({"post": post, "is_liked": is_liked})

    # paginator = Paginator(new_type, 10)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(request, 'network/posts.html', {'page_obj': new_type})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("posts"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("posts"))

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
        return HttpResponseRedirect(reverse("posts"))
    else:
        return render(request, "network/register.html")
    
@login_required
def create_post(request):
    print('create_post called')
    if request.method == "POST":
        content = request.POST["content"]
        latitude = request.POST["latitude"]
        longitude = request.POST["longitude"]
        picture = request.FILES.get("image")
        poster = request.user
        post = Post(poster=poster,content=content,latitude=latitude,longitude=longitude,picture=picture)
        post.save()
        return HttpResponseRedirect(reverse("posts"))
    else :
        return render(request,"network/create.html")

def view_profile(request, username):
    print('view_profile called')
    print(username)

    user = User.objects.get(username=username)
    
    # in cases where network is not yet created
    if not Network.objects.all().filter(user=user).exists():
        network = Network(user=user)
        network.save()
        
    network = Network.objects.get(user=user)

    print("helooooooo")
    
    followers = network.followers
    followers_count = followers.count()

    following = user.following
    following_count = following.count()

    others_profile = True
    others_profile_follow = True

    if user == request.user:
        others_profile = False
    else:
        # has to use the id / primary key
        if followers.filter(pk=request.user.pk).exists():
            others_profile_follow = False

    user_post = Post.objects.filter(poster=user).order_by('-time')

    new_type = []
    for post in user_post:
        is_liked = post.likes.filter(id=request.user.id).exists()
        new_type.append({"post": post, "is_liked": is_liked})

    # paginator = Paginator(new_type, 10)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "network" : network, 
        "followers_count" : followers_count,
        "following_count" : following_count,
        "others_profile" : others_profile,
        "others_profile_follow" : others_profile_follow,
        'page_obj': new_type
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
    
def postpage(request, post_id):
    post = Post.objects.get(id=post_id)
    is_liked = post.likes.filter(id=request.user.id).exists()

    return render(request, 'network/postpage.html', {
        'post' : post,
        'post_id' : post_id,
        'is_liked' : is_liked,
    })
   
@require_http_methods(["POST"])
def mark_button(request):        
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

        post.found=True
        post.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Post saved successfully.',
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
def unmark_button(request):        
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

        post.found=False
        post.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Post saved successfully.',
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
    
def search(request):
    if request.method == "POST":
        search_content = request.POST["content"].upper()
        list = []
        all_post = Post.objects.all()
        for post in all_post:
            P = post.content.upper()
            if P.find(search_content) != -1:
                list.append(post)
        return render(request, "network/search.html", {
            "posts" : list,
        })
    else:
        return render(request, "network/search.html")
    
def maps(request):
    return render(request, "network/maps.html")

def points(request, post_id):
    all_post = Post.objects.all()
    point_list = []
    for post in all_post:
        if not post.found and post_id == post.id:
            print(post.content)
            url = reverse('postpage', args=[post.id])
            point_list.append({"lat": post.latitude, "lng": post.longitude, "description":post.content, "id": post.id, "url": url})

    return JsonResponse(point_list, safe=False)

def all_points(request):
    all_post = Post.objects.all()
    point_list = []
    for post in all_post:
        if not post.found:
            print(post.content)
            url = reverse('postpage', args=[post.id])
            point_list.append({"lat": post.latitude, "lng": post.longitude, "description":post.content, "id": post.id, "url": url})

    return JsonResponse(point_list, safe=False)

@login_required
def chat(request,username):  
    sender = request.user
    receiver = User.objects.get(username=username)
    texts = []
    for message in sender.sent_messages.all():
        if message.receiver == receiver:
            texts.append(message)
    for message in sender.received_messages.all():
        if message.sender == receiver:
            texts.append(message)
        
    texts.sort(key=lambda x: x.time)

    return render(request, "network/chat.html", {
        'texts' : texts,
    })
