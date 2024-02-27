from rest_framework import generics,status
from rest_framework.response import Response
from post.models.motation import Motation
from post.serializers.motation import MotationBasicSerializer
from group.models.group_member import GroupMember

class MotationView(generics.CreateAPIView):
    queryset = Motation.objects.all()
    serializer_class = MotationBasicSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.data.get("user",None)
            post = request.data.get("post",None)
            group = request.data.get("group",None)
            group_member = GroupMember.objects.filter(group__id = group,member__id= user)
            if len(group_member)>0:
                motations = Motation.objects.filter(post__id = post, user__id = user)
                if len(motations)==0:
                    data = {
                        "post" : post,
                        "user" : user
                    }
                    serializer = MotationBasicSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    motations[0].delete()
                    return Response(dict(msg="You delete successfull", status=status.HTTP_200_OK)) 
            else:
               return Response(dict(msg="You can't react motation", status=status.HTTP_400_BAD_REQUEST)) 
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_204_NO_CONTENT))