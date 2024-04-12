from django.db import models

# Create your models here.





class Medicine(models.Model):
    name = models.CharField(max_length=500)
    catagory = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)


# models.py

