from django.urls import path
from django.contrib.auth import views as login_views
from . import views as my_views


urlpatterns = [
    path("data/", my_views.data, name='data'),
]
