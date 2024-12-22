from django.urls import include, path
from meetlink.domain.call import call_view
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("calls", call_view.CallAPI, basename="calls")

urlpatterns = [
    path("", views.index, name="index"),
    path("totem/", views.totem, name="totem"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("calls/", call_view.calls_index, name="calls_index"),
    path("calls/<int:id>", call_view.CallsEdit.as_view(), name="calls_edit"),
    path("api/", include(router.urls)),
    path("create_call/", call_view.create_call, name="create_call"),
]
