from activities.models import Activity
from activities.serializer import ActivitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from activities.permissions import CreateActivityPermission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import ipdb


class ActivitiesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateActivityPermission]

    def get(self, request):
        if request.user.is_staff or request.user.is_superuser:
            data = Activity.objects.all()
            serializer = ActivitySerializer(data, many=True)
        else:
            data = Activity.objects.filter(user_id=request.user.id)
            serializer = ActivitySerializer(data, many=True)

        return Response(serializer.data)

    def put(self, request):
        activity_id = request.data["id"]
        grade = request.data["grade"]

        found_activity = get_object_or_404(Activity, id=activity_id)

        found_activity.update(grade=grade)

        serializer = ActivitySerializer(found_activity)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        if data["grade"]:
            data.pop("grade")

        user = User.objects.get(id=request.user.id)

        try:
            activity = Activity.objects.create(**data, user_id=user)
            serializer = ActivitySerializer(activity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"error": "activity already exists"}, status=status.HTTP_409_CONFLICT
            )
