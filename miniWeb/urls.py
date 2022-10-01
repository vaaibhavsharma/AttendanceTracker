from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('register', views.register, name="register"),
    path('settings', views.settings, name="settings"),
    path('login', views.userlogin, name="login"),
    path('logout', views.logoutPage, name="logout"),
    path('refresh', views.refreshAtten, name="refresh"),
]
