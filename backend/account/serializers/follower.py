from account.models.follower import Follower
from rest_framework import serializers
from account.serializers.UserSerializers import UserDetailSerializer

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"

class GetFollowingSerializer(serializers.Serializer):
    follower = UserDetailSerializer(many=True)
    following = UserDetailSerializer(many=True)