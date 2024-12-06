from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("totem/", views.totem, name="totem"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
]