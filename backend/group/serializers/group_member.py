from rest_framework import serializers
from course.serializers.course import CourseBasicSerializer
from study.serializers.user_course import UserCourseDetailSerializer
from group.models.group_member import GroupMember
from account.serializers.UserSerializers import UserDetailSerializer

class GroupMember1Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = GroupMember
        fields = "__all__"


class GroupMemberSerializer(serializers.ModelSerializer):
    member = UserDetailSerializer()
    
    class Meta:
        model = GroupMember
        fields = "__all__"

class GroupMemberBasicSerializer(serializers.Serializer):
    course = CourseBasicSerializer()
    members = UserCourseDetailSerializer(many=True)



    