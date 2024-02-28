from account.models import User
from account.serializers.UserSerializers import UserDetailSerializer,AccountSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets, generics
from rest_framework.decorators import action
from group.models.group_member import GroupMember
from account.models.roles import Roles
from account.models.users_roles import UserRole

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

class GetMeView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        id = self.kwargs["pk"]
        user_roles = UserRole.objects.filter(user__id=id)
        ids_role = [item.role.id for item in user_roles]
        roles = Roles.objects.filter(id__in = ids_role)
        user = User.objects.filter(id=id)
        if len(user)>0:
            data={
                "account" :  user[0],
                "roles" : roles
            }
            serializer = AccountSerializer(data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


