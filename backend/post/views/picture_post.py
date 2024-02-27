from rest_framework import generics,status
from rest_framework.response import Response
from post.models.picture_post import PicturePost
from post.serializers.picture_post import PicturePostBaiscSerializer

class PicturePostView(generics.CreateAPIView):
    queryset = PicturePost.objects.all()
    serializer_class  = PicturePostBaiscSerializer