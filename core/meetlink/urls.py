from django.urls import path

from . import views
from meetlink.domain.call import call_view

urlpatterns = [
    path("", views.index, name="index"),
    path("totem/", views.totem, name="totem"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("calls/", call_view.calls_index, name="calls_index"),
    path("calls/<int:id>", call_view.CallsEdit.as_view(), name="calls_edit"),
    path("api/calls", call_view.CallsApi.as_view(), name="calls_api_create"),
    # path("create_call/", views.create_call, name="create_call")
]
