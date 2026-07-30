from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer, RegisterSerializer , UserDetailSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserDetails

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access":  str(refresh.access_token),
    }




class LoginView(APIView):
    permission_classes = [AllowAny]  # no auth needed to login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            return Response(
                {
                    "message": "Login successful",
                    "role":    data["role"],
                    "tokens":  {
                        "access": data["access"],
                        "refresh": data["refresh"],
                    },
                },
                status=status.HTTP_200_OK,
            )

        # If validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(APIView):
    permission_classes = [AllowAny]  # no auth needed to register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user   = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response(
                {
                    "message": "Registration successful",
                    "role":    user.role,
                    "tokens":  tokens,
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            # This will show you exactly what failed
            print(serializer.errors)  # Check your terminal/console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailApiView(APIView):

    def post(self,request):

        serializer=UserDetailSerializer(data=request.data
        )

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "message":"Details created successfully",
                    "data":serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                "message":"Failed to create details",
                "errors":serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    

    def get(self,request,id=None):

        if id:
            try:
                user=UserDetails.objects.get(id=id)
                serializer=UserDetailSerializer(user)

                return Response(
                    {
                        "message":"Profile retrieved successfully",
                        "data":serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            except user.DoesNotExist:
                return Response(
                    {
                        "message":"User not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        
        reviews=UserDetails.objects.all()
        serializer=UserDetailSerializer(reviews,many=True)

        return Response(
            {
                "message":"User retrieved successfully",
                "data":serializer.data
            },
            status=status.HTTP_200_OK
        )

