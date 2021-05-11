from courses.permissions import CreateCoursePermission
from courses.models import Course
from courses.serializers import CourseSerializer
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import CredentialSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateCoursePermission]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.create(**serializer.data)

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
