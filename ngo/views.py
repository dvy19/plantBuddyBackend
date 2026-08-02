from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import NGO, Campaign
from .serializer import CampaignSerializer, NGOSerializer, CampaignSerializer

# Create your views here.
class NGOView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = NGOSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save(user=request.user)   # or serializer.save()
                return Response(serializer.data)
            except Exception as e:
                print(e)
                raise
        else:
            print(serializer.errors)
            

        return Response(serializer.errors, status=400)

    def get(self, request , ngo_id=None):

        if ngo_id:
            try:
                ngo = NGO.objects.get(id=ngo_id)

                serializer = NGOSerializer(ngo)

                return Response(
                    {
                        "message": "NGO retrieved successfully",
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            except NGO.DoesNotExist:
                return Response(
                    {
                        "message": "NGO not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        ngos = NGO.objects.all()

        serializer = NGOSerializer(ngos, many=True)

        return Response(
            {
                "message": "NGOs retrieved successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class MyNGOView(APIView):

    def get(self, request):
        try:
            ngo = request.user.ngo_profile
        except NGO.DoesNotExist:
            return Response(
                {"message": "NGO profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NGOSerializer(ngo)

        return Response(
            {
                "message": "NGO retrieved successfully",
                "data": serializer.data
            }
        )

class CampaignView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        try:
            ngo = request.user.ngo_profile
        except NGO.DoesNotExist:

            return Response(
                {"message": "NGO profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CampaignSerializer(data=request.data)

        print(serializer.is_valid())
        print(serializer.errors)

        if serializer.is_valid():
            serializer.save(ngo=ngo)

            return Response(
                {
                    "message": "Campaign created successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        print(serializer.errors)
        print(serializer.is_valid())
        print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, campaign_id=None):

        if campaign_id:
            try:
                campaign = Campaign.objects.get(id=campaign_id)

                serializer = CampaignSerializer(campaign)

                return Response(
                    {
                        "message": "Campaign retrieved successfully",
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            except Campaign.DoesNotExist:
                return Response(
                    {
                        "message": "Campaign not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        campaigns = Campaign.objects.all()

        serializer = CampaignSerializer(campaigns, many=True)

        return Response(
            {
                "message": "Campaigns retrieved successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )