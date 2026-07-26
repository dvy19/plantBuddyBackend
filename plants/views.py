from django.shortcuts import render
from rest_framework.views import APIView
from .models import Plant
from .serializers import PlantSerializer
from rest_framework.permissions import AllowAny

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .services.gemini_service import plant_facts_for_a_day


class PlantApiView(APIView):

    permission_classes = [AllowAny]

    def get(self,request,plant_id=None):

        if plant_id:
            try:
                plant = Plant.objects.get(id=plant_id)

                serializer = PlantSerializer(plant)

                print("plant data:", serializer.data)  # Debugging statement
                
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
        
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
        return Response(
            {
                "message": "Places retrieved successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class PlantFactForDay(APIView):

    permission_classes = [AllowAny]

    def get(self,request):
        print("Inside API")

        
        fact = plant_facts_for_a_day()
        print(fact)

        return Response(fact)
            
