from rest_framework import generics, status
from rest_framework.response import Response

from post.models.comment import Comment
from post.serializers.comment import CommentShowSerializer,CommentBasicSerializer

class CommentView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['post']    
        comments = Comment.objects.filter(post__id = post_id,parent_comment=0).order_by("created_at")
        datas = []
        for comment in comments:
            sub_comments = Comment.objects.filter(post__id= post_id, parent_comment=comment.id)
            data = {
                "comment" : comment,
                "sub_comments" : sub_comments
            }
            datas.append(data)
        d = CommentShowSerializer(datas,many=True,context={"request": request}).data
        return Response(d, status=status.HTTP_201_CREATED) 
            
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentBasicSerializer