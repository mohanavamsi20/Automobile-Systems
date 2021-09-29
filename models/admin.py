from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Variant)
admin.site.register(Car)
admin.site.register(Deals)
admin.site.register(Color)
admin.site.register(Custom)
