from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator
from django.http import JsonResponse
import json

@csrf_exempt
@login_required
def edit_post(request):
    if request.method == "POST":
        form = EditPostForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data["pk"]
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            editPost = Post.objects.get(pk=pk, user=request.user.id)
            editPost.title = title
            editPost.body = body
            editPost.save()
        else:
            print(form.errors.as_data())

    posts = Post.objects.filter(user=request.user.id)
    # Return posts in reverse chronologial order
    order_posts = posts.order_by("-timestamp").all()

    try:
        followers = Follower.objects.filter(userYouFollowId=request.user.id, follow=True)
        num_followers = Paginator(followers, 2)
        follow = Follower.objects.get(user=request.user.id, userYouFollowId=request.user.id)
        userYouFollowId = Follower.objects.filter(user=request.user.id)
        num_userYouFollowId = Paginator(userYouFollowId, 2)
        
        return render(request,"network/profile.html",{
            "posts": order_posts,
            "num_followers": num_followers.count,
            "userYouFollowId": num_userYouFollowId.count,
            "form": PutForm,
            "follow": follow.follow,
            "EditPostForm": EditPostForm,
        })
    except Follower.DoesNotExist:
        followers = Follower.objects.filter(userYouFollowId=request.user.id, follow=True)
        num_followers = Paginator(followers, 2)
        userYouFollowId = Follower.objects.filter(user=request.user.id)
        num_userYouFollowId = Paginator(userYouFollowId, 2)
        return render(request,"network/profile.html",{
            "posts": order_posts,
            "num_followers": num_followers.count,
            "userYouFollowId": num_userYouFollowId.count,
            "form": PutForm,
            "follow": False,
            "EditPostForm": EditPostForm,
        })

@csrf_exempt
@login_required
def like(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Check recipient like
    data = json.loads(request.body)

    if data["likeUnlike"] == "True":

        try:
            post_id = Like.objects.get(user=data["user"], post_id=data["post_id"])
            # post_id = Like.objects.get(post_id=data["post_id"])
            post_id.likeUnlike = True
            post_id.save()

            likes = Post.objects.get(pk=data["post_id"])
            likes.num_likes += 1
            likes.save()
            likes.likes.add(post_id.id)

        except Like.DoesNotExist:
            # Create one like
            user = User.objects.get(pk=data["user"])
            newLike = Like(
                user = user,
                post_id = data["post_id"],
                likeUnlike = data["likeUnlike"],
            )
            newLike.save()

            likes = Post.objects.get(pk=data["post_id"])
            likes.num_likes += 1
            likes.save()
            likes.likes.add(newLike.id)
            
        return JsonResponse({"num_likes": likes.num_likes})
    else:
        likes = Like.objects.get(user=request.user.id, post_id=data["post_id"])
        likes.likeUnlike = False
        likes.save()

        unlike = Post.objects.get(pk=data["post_id"])
        if unlike.num_likes >-1:
            unlike.num_likes -= 1
            unlike.save()

        deletelike = Post.objects.get(pk=data["post_id"])
        like = Like.objects.get(user=request.user.id, post_id=data["post_id"])
        deletelike.likes.remove(like)

        return JsonResponse({"num_likes": deletelike.num_likes})

@login_required
def indexPage(request):
    posts = Post.objects.all()
    order_posts = posts.order_by("-timestamp").all()
    num_posts = Paginator(order_posts, 10)
    tenPost = num_posts.page(2).object_list

    # Return email contents
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in tenPost], safe=False)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    return JsonResponse({"data[pk]": "NO DATA"}, status=201)

@login_required()
def following(request):

    following = Follower.objects.filter(user=request.user.id, follow=True)

    if len(following) != 0:
        followers =[]
        for obj in following:
            followers.append(obj.userYouFollowId)
        
        posts = Post.objects.filter(user=followers[0])

        if len(following) == 2:
            posts = Post.objects.filter(user=followers[0]) | Post.objects.filter(user=followers[1])
        elif len(following) == 3:
            posts = Post.objects.filter(user=followers[0]) | Post.objects.filter(user=followers[1]) | Post.objects.filter(user=followers[2])
        
        # Return posts in reverse chronologial order
        order_posts = posts.order_by("-timestamp").all()
        num_posts = Paginator(order_posts, 10)
        tenPost = num_posts.page(1).object_list

        return render(request, "network/following.html",{
            "posts": tenPost,
            "num_posts": num_posts.count,
        })
    else:
        return render(request, "network/following.html",{
            "posts": following,
            "num_posts": 0,
        })

@login_required()
def profile(request, user_id):
    posts = Post.objects.filter(user=user_id)
    # Return posts in reverse chronologial order
    order_posts = posts.order_by("-timestamp").all()

    if request.method == "POST":
        form = PutForm(request.POST)
        if form.is_valid():
            try:
                userYouFollowId = Follower.objects.filter(user=request.user.id, userYouFollowId=user_id)
                follow = Follower.objects.get(user=request.user.id, userYouFollowId=user_id)
            except Follower.DoesNotExist:
                userYouFollowId = form.cleaned_data["follow"]
                newFollow= Follower( user = User.objects.get(pk=request.user.id),
                    userYouFollowId = user_id,
                    follow = userYouFollowId,)
                newFollow.save()

            if request.POST.get("Follow") == "Follow":
                follow = Follower.objects.get(user=request.user.id, userYouFollowId=user_id)
                follow.follow = True
                follow.save()
            elif request.POST.get("Follow") == "Unfollow":
                Unfollow = Follower.objects.get(user=request.user.id, userYouFollowId=user_id)
                Unfollow.follow = False
                Unfollow.save()

    try:
        followers = Follower.objects.filter(userYouFollowId=user_id, follow=True)
        num_followers = Paginator(followers, 2)
        follow = Follower.objects.get(user=request.user.id, userYouFollowId=user_id)
        userYouFollowId = Follower.objects.filter(user=user_id)
        num_userYouFollowId = Paginator(userYouFollowId, 2)
        
        return render(request,"network/profile.html",{
            "posts": order_posts,
            "num_followers": num_followers.count,
            "userYouFollowId": num_userYouFollowId.count,
            "form": PutForm,
            "follow": follow.follow,
            "EditPostForm": EditPostForm,
        })
    except Follower.DoesNotExist:
        followers = Follower.objects.filter(userYouFollowId=user_id, follow=True)
        num_followers = Paginator(followers, 2)
        userYouFollowId = Follower.objects.filter(user=user_id)
        num_userYouFollowId = Paginator(userYouFollowId, 2)
        return render(request,"network/profile.html",{
            "posts": order_posts,
            "num_followers": num_followers.count,
            "userYouFollowId": num_userYouFollowId.count,
            "form": PutForm,
            "follow": False,
            "EditPostForm": EditPostForm,
        })

@csrf_exempt
@login_required()
def new(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            newPost= Post( user = User.objects.get(pk=request.user.id),
                title = title,
                body = body,)
            newPost.save()
            # Attempt to get number of likes
            try:
                likes = Like.objects.get(pk=newPost.id)
                num_likes = Paginator(likes, 2)
                likes.num_likes.add(num_likes)
            except Like.DoesNotExist:
                # no existen likes
                return HttpResponseRedirect(reverse("index"))
                
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request,"network/new.html",{
                "form": NewPostForm
            } )

    return render(request,"network/new.html",{
            "form": NewPostForm
        })

def index(request):
    posts = Post.objects.all()
    order_posts = posts.order_by("-timestamp").all()
    num_posts = Paginator(order_posts, 10)
    tenPost = num_posts.page(1).object_list

    i=0
    user_likes = []
    for post in tenPost:
        flag =False
        for like in post.likes.all():
            try:
                exist = Like.objects.get(user=request.user.id, post_id=like.post_id)
                if len(post.likes.all()) >= 1 and flag == False:
                    i+=1
                    flag =True
                    user_likes.append(exist)
            except Like.DoesNotExist:
                # print(False)
                pass

    return render(request,"network/index.html",{
        "posts": tenPost,
        "num_posts": num_posts.count,
        "user_likes": user_likes,
    })

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
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")