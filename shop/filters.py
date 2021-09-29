 
from django.db.models import fields
import django_filters

from .models import *

class ShopCarFilter(django_filters.FilterSet):
    class Meta:
        model = SellCar
        fields = ['make', 'model', 'variant', 'state', 'city']
