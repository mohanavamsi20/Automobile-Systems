from django.urls import path

from .views import *

urlpatterns = [
    path('',models_home, name='models-home'),
    path('details/<int:id>/',detail,name='models-detail'),
    path('locate/',dealer_locate,name='dealer-locate'),
    path('custom/',custom,name='custom-order'),
    path('load-colors/', load_colors, name='load_colors'),
]