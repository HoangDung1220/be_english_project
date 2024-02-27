from rest_framework import serializers
from course.models.level import Level

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"