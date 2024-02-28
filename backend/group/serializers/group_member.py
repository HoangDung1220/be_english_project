from rest_framework import serializers
from course.serializers.course import CourseBasicSerializer
from study.serializers.user_course import UserCourseDetailSerializer
from group.models.group_member import GroupMember
from account.serializers.UserSerializers import UserDetailSerializer
from account.models.users_roles import UserRole

class GroupMember1Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = GroupMember
        fields = "__all__"


class GroupMemberSerializer(serializers.ModelSerializer):
    member = UserDetailSerializer()
    
    class Meta:
        model = GroupMember
        fields = "__all__"

    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            role = UserRole.objects.filter(user__id=instance.member.id,role__id=3, group_id=instance.group.id)
            if len(role)>0:
                ret['role'] = "admin_group"
            else:
                ret['role'] = "member"
            
        except Exception:
            print("err")
        return ret

class GroupMemberBasicSerializer(serializers.Serializer):
    course = CourseBasicSerializer()
    members = UserCourseDetailSerializer(many=True)



    