
from django.urls import path

from .views import  LoginView, RegisterView , UserDetailApiView, VolunteerView

urlpatterns = [

    path("register/", RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('create-profile/', UserDetailApiView.as_view()),

    path('create-volunteer-profile/', VolunteerView.as_view()),


]