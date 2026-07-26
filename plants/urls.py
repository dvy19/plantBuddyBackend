
from django.urls import path
from .views import PlantApiView, PlantFactForDay

urlpatterns = [
    path(
        "singlePlants/<int:plant_id>/",
        PlantApiView.as_view(),
        name="get-single-plant"
    ),

     path(
            "allPlants/",
            PlantApiView.as_view(),
            name="get-all-plant"
    ),

    path(
        "getFactOfDay/",
        PlantFactForDay.as_view(),
        name="plant_fact_for_day"
    )



]