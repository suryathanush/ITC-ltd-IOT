from django.urls import path, include
from . import views

urlpatterns = [
    path("server/", views.index, name="index"),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path("register_graph/", views.Register),
    path("register_card/", views.Register_card),
]


"""
auth/token/login/ ----for log in
auth/token/logout/ ---for log out
auth/users/    -------for sign up
"""
