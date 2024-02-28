from rest_framework import serializers
from rating.models.rating_course import RatingCourse

class RatingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingCourse
        fields = "__all__"