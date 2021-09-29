from django.urls import path
from .views import *

urlpatterns = [
    path('', render_index, name="index"),
    path('signup/', UserCreateView.as_view(), name="signup"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', logout, name="logout"),
    path('account/', profile, name="profile"),
    path('account/update/', update, name="account-update"),
    path('account/delete/', delete, name="account-delete"),
    path('load-cities/', load_cities, name='load_cities'),
    path('dealer/', dealerCreateView.as_view(), name='dealer'),
]