from rest_framework import generics,status
from group.models.group_member import GroupMember
from group.serializers.group_member import GroupMemberSerializer,GroupMember1Serializer
from rest_framework.response import Response

class GroupMemberView(generics.CreateAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMember1Serializer

class GetGroupMemberView(generics.ListAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer

    def get(self, request, *args, **kwargs):
        id =self.kwargs["id"]
        members = GroupMember.objects.filter(group__id=id)
        serializer = GroupMemberSerializer(members,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class DeleteGroupMember(generics.DestroyAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer

    def delete(self, request, *args, **kwargs):
        group =self.kwargs["group"]
        member = self.kwargs["member"]
        members = GroupMember.objects.filter(group__id=group,member__id=member)
        if len(members)>0:
            members[0].delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)