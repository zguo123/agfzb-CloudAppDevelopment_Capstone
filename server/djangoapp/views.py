from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from random import *

from django.shortcuts import render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf
from .models import CarDealer, DealerReview, CarModel, CarMake


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
    context = {}

    if request.method == "GET":
        url = "https://faas-tor1-70ca848e.doserverless.co/api/v1/web/fn-f4a2ff9a-4c8e-43ca-81ab-c538031fe2fa/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        # Return a context that has the dealership list
        context = {'dealership_list': dealerships}

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    context = {}
    if request.method == "GET":
        dealer_url = "https://faas-tor1-70ca848e.doserverless.co/api/v1/web/fn-f4a2ff9a-4c8e-43ca-81ab-c538031fe2fa/dealership-package/get-dealership"
        # Get dealers from the dealershipUrl
        dealership = get_dealer_by_id_from_cf(dealer_url, id=id)

        url = "https://faas-tor1-70ca848e.doserverless.co/api/v1/web/fn-f4a2ff9a-4c8e-43ca-81ab-c538031fe2fa/dealership-package/get-reviews"
        reviews = get_dealer_reviews_from_cf(url, id=id)
        context["reviews"] = reviews
        context["dealer"] = dealership

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, id):
    if request.method == "GET":

        # get the CarMake
        dealer_url = "https://faas-tor1-70ca848e.doserverless.co/api/v1/web/fn-f4a2ff9a-4c8e-43ca-81ab-c538031fe2fa/dealership-package/get-dealership"
        # Get dealers from the dealershipUrl
        dealership = get_dealer_by_id_from_cf(dealer_url, id=id)

        context = {}

        cars = CarModel.objects.all()

        print(cars[0].car_make.name)

        context["cars"] = cars

        context["dealer"] = dealership

        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST" and request.user.is_authenticated:
        url = "https://faas-tor1-70ca848e.doserverless.co/api/v1/web/fn-f4a2ff9a-4c8e-43ca-81ab-c538031fe2fa/dealership-package/post-review"
        review = {}

        print(request.POST)

        # car
        car_id = request.POST["car"]
        car = CarModel.objects.get(pk=car_id)

        review['id'] = randint(1, 2000000)
        review['name'] = request.user.username
        review['dealership'] = id
        review['review'] = request.POST['content']
        review['purchase'] = request.POST.get('purchasecheck', False)
        review['purchase_date'] = request.POST['purchasedate']
        review['car_make'] = car.car_make.name
        review['car_model'] = car.name
        review['car_year'] = car.year.strftime("%Y")

        request_payload = {}
        request_payload['review'] = review

        response = post_request(url, request_payload)
        print(response)

        return redirect("djangoapp:dealer_details", id=id)
