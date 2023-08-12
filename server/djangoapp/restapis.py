import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth

from .models import CarDealer, DealerReview

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, CategoriesOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import os

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url,  **kwargs):
    print(kwargs)
    print("GET from {} {}".format(url, kwargs))

    api_key = kwargs.get('api_key', None)
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]

            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)

    return json_data


def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                 params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)

    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result

        # For each dealer object
        for dealer in dealers:
            print(dealer)

            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, id=dealerId)
    print(f'info: {url} {dealerId}')
    if json_result:
        reviews = json_result
        for review in reviews:
            review_doc = review
            review_obj = DealerReview(id=review_doc['id'], dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                      review=review_doc["review"], purchase_date=review_doc[
                                          "purchase_date"], car_make=review_doc["car_make"],
                                      car_model=review_doc["car_model"], car_year=review_doc["car_year"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results


def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealership_by_state_from_cf(url, st):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=st)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)


def analyze_review_sentiments(text):
    try:
        url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/77bcb2a9-952b-4629-a3e4-2e16ff31e508"

        api_key = os.getenv("IBM_NLU_KEY")

        authenticator = IAMAuthenticator(api_key)

        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-04-07', authenticator=authenticator)

        natural_language_understanding.set_service_url(url)

        response = natural_language_understanding.analyze(text=text, features=Features(
            sentiment=SentimentOptions(targets=[text]))).get_result()

        return response['sentiment']['document']['label']
    except Exception as e:
        print("Error processing text sentiment. {}".format(e))
