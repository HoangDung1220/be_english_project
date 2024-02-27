from rest_framework import generics
from group.models.group_member import GroupMember
from group.serializers.group_member import GroupMemberSerializer,GroupMember1Serializer

class GroupMemberView(generics.CreateAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMember1Serializer