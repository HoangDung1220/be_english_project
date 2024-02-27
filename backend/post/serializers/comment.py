from rest_framework import serializers
from post.models.comment import Comment
from account.serializers.UserSerializers import UserDetailSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer() 
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H-%M")

    class Meta:
        model = Comment
        fields = "__all__"

class CommentBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class CommentShowSerializer(serializers.Serializer):
    comment = CommentSerializer()
    sub_comments = CommentSerializer(many=True)
    