from activities.models import Activity
from activities.serializer import ActivitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from activities.permissions import CreateActivityPermission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction


class ActivitiesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateActivityPermission]

    def get(self, request, user_id=""):
        if not request.user.is_superuser and not request.user.is_staff and user_id:
            return Response(
                {"error": "You dont have permission"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.user.is_superuser or request.user.is_staff:
            if user_id:
                found_user = get_object_or_404(User, id=user_id)
                activities = Activity.objects.filter(user_id=found_user)
                serializer = ActivitySerializer(activities, many=True)
                return Response(serializer.data)
            else:
                data = Activity.objects.all()
                serializer = ActivitySerializer(data, many=True)
                return Response(serializer.data)

        if not request.user.is_superuser and not request.user.is_staff:
            data = Activity.objects.filter(user_id=request.user.id)
            serializer = ActivitySerializer(data, many=True)
            return Response(serializer.data)

    def put(self, request):
        activity_id = request.data["id"]
        grade = request.data["grade"]

        get_object_or_404(Activity, id=activity_id)

        Activity.objects.filter(id=activity_id).update(grade=grade)

        updated_activity = Activity.objects.get(id=activity_id)

        serializer = ActivitySerializer(updated_activity)

        return Response(serializer.data)

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        if data["grade"]:
            data.pop("grade")

        user = get_object_or_404(User, id=request.user.id)

        try:
            with transaction.atomic():
                activity = Activity.objects.create(**data, user_id=user)
                serializer = ActivitySerializer(activity)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"error": "activity already exists"}, status=status.HTTP_409_CONFLICT
            )
