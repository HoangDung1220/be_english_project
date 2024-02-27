from rest_framework import serializers
from post.models.motation import Motation
from account.serializers.UserSerializers import UserDetailSerializer

class MotationSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer() 

    class Meta:
        model = Motation
        fields = ("id","user")

class MotationBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Motation
        fields = "__all__"