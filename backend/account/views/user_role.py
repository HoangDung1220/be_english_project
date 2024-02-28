from rest_framework import generics,status
from rest_framework.response import Response
from account.models.users_roles import UserRole
from account.serializers.user_role import UserRoleBasicSerialzer

class UserRoleView(generics.CreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleBasicSerialzer