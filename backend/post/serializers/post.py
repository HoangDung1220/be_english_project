from rest_framework import serializers
from post.models.post import Post
from account.serializers.UserSerializers import UserDetailSerializer
from post.serializers.picture_post import PicturePostSerializer
from post.serializers.motation import MotationSerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Post
        fields = "__all__"

class PostBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class PostDetailSerializer(serializers.Serializer):
    post = PostSerializer()
    number_motation = serializers.IntegerField()
    number_comment = serializers.IntegerField()
    motations = MotationSerializer(many=True)
    pictures = PicturePostSerializer(many=True)



    