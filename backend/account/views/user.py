from account.models import User
from account.serializers.UserSerializers import UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets, generics
from rest_framework.decorators import action
from group.models.group_member import GroupMember

class UserView(viewsets.ViewSet):

    @action(methods=['GET'],detail=False)
    def all(self,request,*args, **kwargs):
        try:
            id_group = self.request.query_params.get("group",None)
            group_members = GroupMember.objects.filter(group__id = id_group)
            ids = [item.member.id for item in group_members]
            users = User.objects.exclude(id__in=ids)
            data = UserDetailSerializer(users, many=True).data
            return Response(data=data,status=status.HTTP_200_OK)
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_400_BAD_REQUEST)) 
        
class GetUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer