
from django.urls import path

from core.ngo.views import NGOView


urlpatterns = [

    path("create/", NGOView.as_view(), name="ngo-create"),

    path("get/<int:ngo_id>/", NGOView.as_view(), name="ngo-get"),

    path("get/", NGOView.as_view(), name="ngo-get-all"),


]