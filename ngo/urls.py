
from django.urls import path

from .views import  MyNGOView, NGOView, CampaignView


urlpatterns = [

    path("create/", NGOView.as_view(), name="ngo-create"),

    path("get/<int:ngo_id>/", NGOView.as_view(), name="ngo-get"),

    path("get/", NGOView.as_view(), name="ngo-get-all"),

    path("campaigns/<int:campaign_id>/", CampaignView.as_view(), name="ngo-campaign-get"),

    path("campaigns/", CampaignView.as_view(), name="ngo-campaign-get-all"),

    path("profile/", MyNGOView.as_view(), name="ngo-profile"),

    


]