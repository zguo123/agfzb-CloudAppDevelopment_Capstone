from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
        return redirect('djangoapp:index')
    return render(request, 'djangoapp/index', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    if request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except Exception as e:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        context['message'] = "User already exists."
        return render(request, 'djangoapp/registration.html', context)
# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    if request.method == "GET":
        url = "https://georgezyguo-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        print(dealer_names)
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://georgezyguo-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context["reviews"] = reviews
        return HttpResponse(context['reviews'])


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):

    if request.method == "POST" and request.user.is_authenticated:
        url = "https://georgezyguo-5000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        review = dict()

        review['id'] = request.POST['id']
        review['name'] = request.user.username
        review['dealership'] = dealer_id
        review['review'] = request.POST['content']
        review['purchase'] = request.POST.get('purchasecheck', False)
        review['purchase_date'] = request.POST['purchasedate']
        review['car_make'] = request.POST['car_make']
        review['car_model'] = request.POST['car_model']
        review['car_year'] = request.POST['car_year']

        response = post_request(url, review)
        print(response)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
