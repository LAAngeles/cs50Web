from ast import Delete
from asyncio.windows_events import NULL
from queue import Empty
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# from .models import User
from .models import *
from django.contrib.auth.decorators import login_required


def accounts(request):
    return HttpResponseRedirect(reverse("login"))


def index(request):
    
    return render(request, "auctions/index.html",{
        "users": User.objects.all(),
        "Active_Listings": New_Listings.objects.all(),
        "Close_Listings": close_listing_action.objects.all()
    })


def Close_Listing(request,Listings_id):
    Close_Listings = close_listing_action.objects.get(Listings_id=Listings_id)
    return render(request, "auctions/close_listing.html",{
            "Close_Listings": Close_Listings
        })


def Active_Listings(request, Listings_id):

    try:
        Close_Listings = close_listing_action.objects.get(Listings_id=Listings_id)
        
        return render(request, "auctions/close_listing.html",{
            "Close_Listings": Close_Listings
        })
    except:
        Active_Listings = New_Listings.objects.get(pk=Listings_id)

    mayor = []
    aux = True
    for maximo in New_bid.objects.all():
        if maximo.Listings_id == Listings_id:
            mayor.append(maximo.bid) 
            current_bid = max(mayor)
        elif aux:
            current_bid = Active_Listings.starting_bid
            aux = False 
    error = False

    if request.method == "POST":
        if request.POST.get('coment') == '':
            bid = request.POST.get('bid')
            if request.user.is_authenticated:
                if ( Active_Listings.starting_bid < int(bid) and current_bid <= int(bid) ):
                    Active_bid = New_bid(starting_bid=Active_Listings,user=Active_Listings.user.username,userbid=User.objects.get(pk=request.user.id),Listings_id=Listings_id,bid=bid)
                    Active_bid.save()
                    mayor = []
                    for maximo in New_bid.objects.all():
                        if maximo.Listings_id == Listings_id:
                            mayor.append(maximo.bid) 
                    current_bid = max(mayor)
                else:
                    error =True
        else:
            coment = request.POST["coment"]
            Active_coment = New_Coments(user=User.objects.get(pk=request.user.id),coment=coment,usercoment=Listings_id)
            Active_coment.save()

        return render (request, "auctions/listing.html",{
            "Active": Active_Listings,
            "Active_id": Listings_id,
            "max_bid": current_bid,
            "New_Coments": New_Coments.objects.all(),
            "error": error
        })
    else:
        return render (request, "auctions/listing.html",{
            "Active": Active_Listings,
            "Active_id": Listings_id,
            "max_bid": current_bid,
            "New_Coments": New_Coments.objects.all(),
            "error": error
        })

@login_required()
def watchlist(request):

    if request.method == "POST":
        watchlist = request.POST.get("watchlist", "")
        Active_watchlist = New_Listings.objects.get(pk=watchlist)
        m_watchlist = add_watchlist(user = request.user, userwatchlist=Active_watchlist.id,title=Active_watchlist.title,starting_bid=Active_watchlist.starting_bid,URL_image=Active_watchlist.URL_image)
        m_watchlist.save()
        i=0
        for m_watchlist in add_watchlist.objects.all():
            if request.user.username == m_watchlist.user.username:
                i+=1
        Active_user = User.objects.get(pk=request.user.id)
        Active_user.len_watchlist=i
        Active_user.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render (request, "auctions/watchlist.html",{
            "m_watchlists": add_watchlist.objects.all(),
            "Actual_user": request.user.username
        })

@login_required()
def delete(request):
    
    if request.method == "POST":
        borrar = request.POST.get("delete", "")
        b = add_watchlist.objects.get(pk=borrar)
        b.delete()

        if request.user.is_authenticated:
            i=0
            for m_watchlist in add_watchlist.objects.all():
                if request.user.username == m_watchlist.user.username:
                    i+=1
            Active_user = User.objects.get(pk=request.user.id)
            Active_user.len_watchlist = i
            Active_user.save()
            return HttpResponseRedirect(reverse("watchlist"))
    else:
        return HttpResponseRedirect(reverse("watchlist"))

@login_required()
def close_action(request):

    if request.method == "POST":
        close = request.POST.get("close", "")

        Active_Listings = New_Listings.objects.get(pk=int(close))

        mayor = []
        for maximo in New_bid.objects.all():
            if maximo.Listings_id == int(close):
                mayor.append(maximo.bid) 
        max_bid = max(mayor, default=0)

        if max_bid != 0:
            Winner_bid = New_bid.objects.get(bid=int(max_bid))

            winner_Auction = close_listing_action(title=Active_Listings.title,description=Active_Listings.description,starting_bid=Active_Listings.starting_bid,category=Active_Listings.category,URL_image=Active_Listings.URL_image,user=Active_Listings.user,userbid=Winner_bid.userbid,Listings_id=Winner_bid.Listings_id,bid=Winner_bid.bid)
            winner_Auction.save()

            Active_Listings.delete()
            Winner_bid.delete()
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def categories(request):
    
    Active_Categoriess = New_Listings.objects.values_list('category', flat=True)
    Active_Categories = []
    for  Active_Categorie in Active_Categoriess:
        Active_Categories.append(Active_Categorie)
    Category = []
    for Active_Categorie in Active_Categories:
        if Active_Categorie in Category:
            pass
        else:
            Category.append(Active_Categorie)
    return render (request, "auctions/categories.html",{
        "Active_Categories": Category,
        "flag_categories": True
    })


def category_type(request, C_type):
    Active_categorys = New_Listings.objects.filter(category=C_type)
    return render (request, "auctions/categories.html",{
        "Active_Listings": Active_categorys,
        "flag_categories": False,
    })

@login_required()
def create_listing(request):

    if request.method == "POST":
        Title       = request.POST["Title"]
        Description = request.POST["Description"]
        bid         = request.POST["bid"]
        URL         = request.POST["URL"]
        Category    = request.POST["Category"]

        # Attempt to create new listing
        new = New_Listings(user=User.objects.get(pk=request.user.id),title=Title,description=Description,starting_bid=bid,URL_image=URL,category=Category)
        new.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render (request, "auctions/create_listing.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
