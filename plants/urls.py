
from django.urls import path
from .views import PlantApiView, PlantFactForDay, PlantCategoryFilterAPIView, PlantFAQAPIView, PlantOfTheDayView, WaterLogApiView

urlpatterns = [
    path(
        "singlePlants/<int:plant_id>/",
        PlantApiView.as_view(),
        name="get-single-plant"
    ),

    path("plant-of-the-day/", PlantOfTheDayView.as_view()),

     path(
            "allPlants/",
            PlantApiView.as_view(),
            name="get-all-plant"
    ),

    path(
        "getFactOfDay/",
        PlantFactForDay.as_view(),
        name="plant_fact_for_day"
    ),

    path(
        "category-filter/",
        PlantCategoryFilterAPIView.as_view()

    ),

    path(
        "plant-faq/",
        PlantFAQAPIView.as_view()
    ),

    path("water/", WaterLogApiView.as_view()),
    path("water/<int:plant_id>/", WaterLogApiView.as_view()),



]