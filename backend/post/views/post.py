from rest_framework import generics,status
from rest_framework.response import Response
from post.serializers.post import PostDetailSerializer,PostBasicSerializer
from post.models.post import Post
from post.models.comment import Comment
from post.models.motation import Motation
from post.models.picture_post import PicturePost
from group.models.group_member import GroupMember

class PostView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            group_id = self.kwargs['group']            
            posts = Post.objects.filter(group__id = group_id).order_by("-created_at")
            datas = []
            for post in posts:
                num_comments = Comment.objects.filter(post__id = post.id).count()
                motations = Motation.objects.filter(post__id=post.id)
                pictures = PicturePost.objects.filter(post__id=post.id).order_by("id")

                data = {
                        "post" :post,
                        "number_motation" : len(motations),
                        "number_comment" : num_comments,
                        "motations" : motations,
                        "pictures" :pictures
                }
                datas.append(data)
            d = PostDetailSerializer(datas,many=True,context={"request": request}).data
            return Response(d, status=status.HTTP_201_CREATED)
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_204_NO_CONTENT))

class PostCreateView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            group = request.data.get("group",None)
            user = request.data.get("user",None)
            content = request.data.get("content",None)
            
            post = {
                "group" : group,
                "user" :user,
                "content" : content
            }
            serializer = PostBasicSerializer(data=post)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_204_NO_CONTENT))

class GetPostView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            post_id = self.kwargs['pk']            
            post = Post.objects.get(id=post_id)
            num_comments = Comment.objects.filter(post__id = post_id).count()
            motations = Motation.objects.filter(post__id=post_id)
            pictures = PicturePost.objects.filter(post__id=post_id).order_by("id")

            data = {
                        "post" :post,
                        "number_motation" : len(motations),
                        "number_comment" : num_comments,
                        "motations" : motations,
                        "pictures" :pictures
            }
                
            d = PostDetailSerializer(data,context={"request": request}).data
            return Response(d, status=status.HTTP_201_CREATED)
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_204_NO_CONTENT))
        
class DeletePostView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        try:
            post_id = self.kwargs['pk']            
            
            pics = PicturePost.objects.filter(post__id = post_id)
            for pic in pics:
                pic.delete()

            comments = Comment.objects.filter(post__id = post_id)
            for cmt in comments:
                cmt.delete()

            motations = Motation.objects.filter(post__id = post_id)
            for emoi in motations:
                emoi.delete()

            post = Post.objects.filter(id=post_id)
            if len(post)>0:
                post[0].delete()
                return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_204_NO_CONTENT))