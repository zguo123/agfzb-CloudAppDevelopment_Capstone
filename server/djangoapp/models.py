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

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
