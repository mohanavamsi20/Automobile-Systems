from django.urls import path
from .views import *

urlpatterns = [
    path('', render_home, name="dashboard-home"),

]