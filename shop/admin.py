from django.contrib import admin

from .models import SellCar, BuyCar

# Register your models here.

admin.site.register(SellCar)
admin.site.register(BuyCar)
