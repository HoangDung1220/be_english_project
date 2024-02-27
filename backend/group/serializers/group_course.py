from rest_framework import serializers
from group.models.group_course import GroupCourse
from course.serializers.course import CourseBasicSerializer
from account.serializers.UserSerializers import UserDetailSerializer

class GroupCourseBasicSerializer(serializers.ModelSerializer):
    course = CourseBasicSerializer()
    member_add = UserDetailSerializer()

    class Meta:
        model = GroupCourse
        fields = "__all__"

class GroupCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCourse
        fields = ("group","course","member_add")