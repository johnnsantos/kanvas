from courses.permissions import CreateCoursePermission
from courses.models import Course
from courses.serializers import CourseSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateCoursePermission]

    def get(self, request):
        courses = Course.objects.all()

        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.create(**serializer.data)

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateCourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateCoursePermission]

    def put(self, request):
        course_id = request.data["course_id"]
        user_ids = request.data["user_ids"]

        found_course = get_object_or_404(Course, id=course_id)

        found_users = User.objects.filter(pk__in=user_ids)

        found_course.user_set.clear()

        for user in found_users:
            found_course.user_set.add(user)

        serializer = CourseSerializer(found_course)
        return Response(serializer.data)
