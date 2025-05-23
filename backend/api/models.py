from django.db import models
from django.contrib.auth.models import AbstractUser

class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    outlet = models.CharField(max_length=100)       # changed from outlet_type to outlet
    location = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)        # changed from brand_name to brand
    budget = models.PositiveIntegerField()
    size = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.phone}"

 
    

