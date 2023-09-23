from django.urls import path

from . import views

urlpatterns = [
    path("", views.sign_in, name="signin"),
    path("registration", views.sign_up, name = "signup"),
    path("forgotpassword", views.forgotpassword, name = "forgotpassword")
]