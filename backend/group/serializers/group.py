from rest_framework import serializers
from group.models.group import Group
from account.serializers.UserSerializers import UserDetailSerializer
from group.serializers.group_course import GroupCourseBasicSerializer
from group.serializers.group_member import GroupMemberBasicSerializer, GroupMemberSerializer
from course.serializers.course import CourseBasicSerializer

class GroupAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id","name")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class GroupBasicSerializer(serializers.ModelSerializer):

    create_by = UserDetailSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Group
        fields = "__all__"


class GroupDetailSerialzer(serializers.Serializer):
    group = GroupBasicSerializer()
    courses = GroupCourseBasicSerializer(many=True)
    members = GroupMemberSerializer(many=True)
    members_course = GroupMemberBasicSerializer(many=True)
    public_course = CourseBasicSerializer(many=True)
    private_course = CourseBasicSerializer(many=True)

class GroupSpaceSerializer(serializers.Serializer):
    group = GroupSerializer()
    number_member = serializers.IntegerField()
    number_course = serializers.IntegerField()
    
class GroupAdminSerializer(serializers.Serializer):
    group = GroupBasicSerializer()
    number_member = serializers.IntegerField()
    number_course = serializers.IntegerField()
    rating = serializers.IntegerField()