from account.serializers.UserSerializers import UserSerializer
from account.serializers.role import RoleSerializer
from account.models.users_roles import UserRole
from rest_framework import serializers

class UserRoleSerialzer(serializers.ModelSerializer):
    user = UserSerializer()
    role = RoleSerializer()

    class Meta:
        model = UserRole
        fields = "__all__"