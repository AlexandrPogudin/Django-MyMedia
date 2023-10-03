from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("", views.sign_in, name="signin"),
    path("registration", views.sign_up, name = "signup"),
    path("forgotpassword", views.forgotpassword, name = "forgotpassword"),
    path("main/<str:page_id>/", views.mainpage, name = "mainpage"),
    path('upload/', views.upload_file, name='upload_file'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('changeinfo/', views.changeinfo, name='changeinfo'),
    path('deletefile/', views.deletefile, name='deletefile'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('google-oauth2-complete/', views.google_oauth2_callback, name='google_oauth2_callback'),
]