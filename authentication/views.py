from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


class UserView(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=request.data["username"],
            password=request.data["password"],
            is_superuser=request.data["is_superuser"],
            is_staff=request.data["is_staff"],
        )

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

