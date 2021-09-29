from django.contrib import admin

from .models import User, State, City, Dealer

# Register your models here.
admin.site.register(State)
admin.site.register(City)
admin.site.register(User)
admin.site.register(Dealer)