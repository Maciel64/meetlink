from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("totem/", views.totem, name="totem"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("calls/", views.calls_index, name="calls_index"),
    path("calls/<int:id>", views.CallsEdit.as_view(), name="calls_edit"),
    # path("create_call/", views.create_call, name="create_call")
]