from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from core.ngo.models import NGO
from core.ngo.serializer import NGOSerializer

# Create your views here.
class NGOView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = NGOSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "NGO profile created successfully",
                    "data": serializer.data
                },

                status=status.HTTP_200_OK

                )

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


    