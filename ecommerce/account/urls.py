from django.urls import path
from . import views


urlpatterns = [
    # store main page
    path('register', views.register, name='register'),


    ]
