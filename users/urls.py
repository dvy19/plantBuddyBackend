
from django.urls import path

from .views import DeviceTokenView, LoginView, RegisterView

urlpatterns = [

    path("register/", RegisterView.as_view()),
    path('login/', LoginView.as_view()),


]