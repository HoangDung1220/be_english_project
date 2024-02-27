from rest_framework import serializers
from study.models.course_level import CourseLevel

class CourseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLevel
        fields = ["user_course","level"]

class CourseLevelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLevel
        fields = "__all__"
