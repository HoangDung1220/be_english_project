from rest_framework import serializers
from post.models.picture_post import PicturePost

class PicturePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PicturePost
        fields = ("id","image")


class PicturePostBaiscSerializer(serializers.ModelSerializer):

    class Meta:
        model = PicturePost
        fields = "__all__"