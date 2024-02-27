from rest_framework import serializers
from study.models.user_course import UserCourse
from account.serializers.UserSerializers import UserDetailSerializer

class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ["user","course"]

class UserCourseDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = UserCourse
        fields = "__all__"