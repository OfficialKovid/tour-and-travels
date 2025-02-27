from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',signup, name = 'signup'),
    path('login/',login_page, name = 'login'),
    path('',login_page, name = 'login'),
    path('logout/',logout_user, name = 'logout'),
    path('account/',account, name = 'account'),
]