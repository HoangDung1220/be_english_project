from account.models.roles import Roles
from rest_framework import serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"