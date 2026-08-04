from django.shortcuts import render
from rest_framework.views import APIView
from .models import Plant, FAQQuestion, PlantFAQ
from .serializers import PlantOfDayRequestSerializer, PlantSerializer, FaqSerializer, PlantFaqCacheSerializer, WaterLogSerializer, WaterLog
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from datetime import date, timedelta

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import traceback

from .pagination import PlantPagination

from .services.gemini_service import plant_facts_for_a_day , plant_faq_question, plant_of_the_day

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

        search = request.query_params.get("search", "").strip()

        plants = Plant.objects.all()

        # GET /api/plants/?search=rose

        if search:
            plants = plants.filter(name__icontains=search)

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


class PlantFAQAPIView(APIView):

    permission_classes=[AllowAny]

    def post(self, request):

        plant_id = request.data.get("plant_id")
        question_id = request.data.get("question_id")

        if not plant_id or not question_id:
            return Response(
                {"error": "plant_id and question_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            plant = Plant.objects.get(id=plant_id)
        except Plant.DoesNotExist:
            return Response(
                {"error": "Plant not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            question = FAQQuestion.objects.get(
                id=question_id,
                is_active=True
            )
        except FAQQuestion.DoesNotExist:
            return Response(
                {"error": "Question not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # --------------------
        # Check Cache
        # --------------------

        cache = PlantFAQ.objects.filter(
            plant=plant,
            question=question
        ).first()

        if cache:

            return Response(
                {
                    "cached": True,
                    "data": PlantFaqCacheSerializer(cache).data
                },
                status=status.HTTP_200_OK
            )

        # --------------------
        # Generate with Gemini
        # --------------------

        gemini_response = plant_faq_question(
            plant,
            question
        )

        cache = PlantFAQ.objects.create(
            plant=plant,
            question=question,
            answer=gemini_response["answer"]
        )

        return Response(
            {
                "cached": False,
                "data": PlantFaqCacheSerializer(cache).data
            },
            status=status.HTTP_201_CREATED
        )

class WaterLogApiView(APIView):

    def post( self, request):

        plant_id=request.data.get("plant")

        if not plant_id:
            return Response(
                {"error": "Plant ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            plant = Plant.objects.get(id=plant_id)
        except Plant.DoesNotExist:
            return Response(
                {"error": "Plant not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        today = date.today()

        watered=WaterLog.objects.filter(
            user=request.user,
            plant=plant,
            watered_on=today
        )

        if watered.exists():
            return Response(
                {"message": "Plant already watered today."},
                status=status.HTTP_200_OK
            )

        water_log = WaterLog.objects.create(
            user=request.user,
            plant=plant
        )

        serializer = WaterLogSerializer(water_log)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, plant_id):

        print(plant_id)

        try:
            plant = Plant.objects.get(id=plant_id)
            print(plant)
        except Plant.DoesNotExist:
            return Response(
                {"error": "Plant not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        logs = WaterLog.objects.filter(
            user=request.user,
            plant=plant
        ).order_by("watered_on")

        print(logs)

        watered_dates = [log.watered_on for log in logs]

        # ---------- Calculate Current Streak ----------
        watered_set = set(watered_dates)

        streak = 0
        current_day = date.today()

        while current_day in watered_set:
            streak += 1
            current_day -= timedelta(days=1)

        serializer = WaterLogSerializer(logs, many=True)

        return Response({
            "streak": streak,
            "watered_today": date.today() in watered_set,
            "watered_dates": watered_dates,
            "logs": serializer.data
        })


class PlantOfTheDayView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = PlantOfDayRequestSerializer(data=request.data)

        if serializer.is_valid():
            try:
                result = plant_of_the_day(serializer.validated_data)

                return Response(
                    {
                        "message": "Plant of the day generated successfully.",
                        "data": result
                    },
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {
                        "message": "Failed to generate plant recommendation.",
                        "error": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )