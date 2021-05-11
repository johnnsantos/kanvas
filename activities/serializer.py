from rest_framework import serializers


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    repo = serializers.CharField()
    grade = serializers.IntegerField(allow_null=True, required=False)
