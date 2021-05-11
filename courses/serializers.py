from rest_framework import serializers
from authentication.serializers import UserSerializer


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    user_set = UserSerializer(read_only=True, many=True)
