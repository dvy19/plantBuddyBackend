
from django.urls import path

from .views import NGOCampaignView, NGOView


urlpatterns = [

    path("create/", NGOView.as_view(), name="ngo-create"),

    path("get/<int:ngo_id>/", NGOView.as_view(), name="ngo-get"),

    path("get/", NGOView.as_view(), name="ngo-get-all"),

    path("campaigns/<int:campaign_id>/", NGOCampaignView.as_view(), name="ngo-campaign-get"),

    path("campaigns/", NGOCampaignView.as_view(), name="ngo-campaign-get-all"),

    


]