from django.urls import path
from django.contrib.auth import views as login_views
from . import views as my_views


urlpatterns = [
    path("signin/", login_views.LoginView.as_view(template_name='users_system/signin.html'), name='signin'),
    path("signup/", my_views.sign_up, name='signup'),
    path("signout/", login_views.LogoutView.as_view(template_name='users_system/signout.html'), name='signout'),
]
