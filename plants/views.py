from django.shortcuts import render
from rest_framework.views import APIView
from .models import Plant
from .serializers import PlantSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import traceback

from .pagination import PlantPagination

from .services.gemini_service import plant_facts_for_a_day

class PlantApiView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, plant_id=None):

        print("=" * 50)
        print("Request received")
        print("Plant ID:", plant_id)

        # Single Plant
        if plant_id:
            try:
                plant = Plant.objects.get(id=plant_id)

                print("Plant found:", plant)

                serializer = PlantSerializer(plant)

                print(serializer.data)

                return Response(
                    {
                        "message": "Plant retrieved successfully",
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            except Plant.DoesNotExist:
                return Response(
                    {
                        "message": "Plant not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        # All Plants (Paginated)
        plants = Plant.objects.all()

        paginator = PlantPagination()

        result_page = paginator.paginate_queryset(plants, request)

        serializer = PlantSerializer(result_page, many=True)

        return paginator.get_paginated_response(
            {
                "message": "Plants retrieved successfully",
                "data": serializer.data
            }
        )

        


class PlantFactForDay(APIView):

    permission_classes = [AllowAny]

    def get(self,request):
        print("Inside API")

        
        fact = plant_facts_for_a_day()
        print(fact)

        return Response(fact)



class PlantCategoryFilterAPIView(ListAPIView):
    serializer_class = PlantSerializer

    def get_queryset(self):
        queryset = Plant.objects.all()

        home_place = self.request.query_params.get("home_place")
        category = self.request.query_params.get("category")
        light = self.request.query_params.get("light")
        water = self.request.query_params.get("water")
        soil = self.request.query_params.get("soil")
        season = self.request.query_params.get("season")
        growth = self.request.query_params.get("growth")
        lifespan = self.request.query_params.get("lifespan")
        plant_type = self.request.query_params.get("plant_type")

        if home_place:
            queryset = queryset.filter(home_place_id=home_place)

        if category:
            queryset = queryset.filter(category_id=category)

        if light:
            queryset = queryset.filter(light_requirement_id=light)

        if water:
            queryset = queryset.filter(water_requirement_id=water)

        if soil:
            queryset = queryset.filter(soil_type_id=soil)

        if season:
            queryset = queryset.filter(season_id=season)

        if growth:
            queryset = queryset.filter(growth_rate_id=growth)

        if lifespan:
            queryset = queryset.filter(lifespan_id=lifespan)

        if plant_type:
            queryset = queryset.filter(plant_type_id=plant_type)

        return queryset
            
