"""
Models
"""
from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    """
    CarMake Model
    """
    name = models.CharField(null=False, max_length=30, default='None')
    description = models.CharField(null=False, max_length=100, default='None')

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


class CarModel(models.Model):
    """
    CarModel Model
    """
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='None')
    dealer_id = models.IntegerField(null=False, default=0)
    car_type = models.CharField(
        null=False, max_length=10, choices=CAR_TYPE_CHOICES, default=SEDAN)
    year = models.DateField(null=False, default=now)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Dealer id: " + str(self.dealer_id) + "," + \
               "Car type: " + self.car_type + "," + \
               "Year: " + str(self.year)


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    # sentiment is going to be provided dynamically by the Watson NLU service
    sentiment = ""

    def __init__(self, id,  dealership, name, purchase, review, purchase_date, car_make, car_model, car_year):
        # Dealer id
        self.dealership = dealership
        # Reviewer name
        self.name = name
        # Reviewer purchase
        self.purchase = purchase
        # Reviewer review
        self.review = review
        # Reviewer purchase date
        self.purchase_date = purchase_date
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car year
        self.car_year = car_year

        self.id = id

    def __str__(self):
        return f'Review: {self.review} for {self.car_make} {self.car_model} {self.car_year} by {self.name} at {self.dealership} with sentiment of {self.sentiment}'
