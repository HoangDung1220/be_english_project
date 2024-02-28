from rest_framework import generics,status
from rest_framework.response import Response
from account.models.follower import Follower
from account.models.users import User
from account.serializers.follower import FollowerSerializer,GetFollowingSerializer
from account.serializers.UserSerializers import UserSerializer
from django.db.models import Q


class FollowerView(generics.CreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def post(self, request, *args, **kwargs):
        user = request.data.get("user",None)
        user_follow = request.data.get("user_follow",None)
        item = Follower.objects.filter(user__id = user, user_follow = user_follow)
        if len(item)==0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            user1 = User.objects.get(id=user)
            user1.number_follower = user1.number_follower +1
            user1.save()

            user2 = User.objects.get(id=user_follow)
            user2.number_folowing = user2.number_folowing +1
            user2.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetFollowerView(generics.ListAPIView):
    queryset = Follower.objects.all()
    serializer_class = GetFollowingSerializer

    def get(self, request, *args, **kwargs):
        user = self.kwargs["id"]
        following = Follower.objects.filter(user_follow=user)
        ids = [item.user.id for item in following]
        data1 = User.objects.filter(id__in=ids)

        follower= Follower.objects.filter(user__id=user)
        id1s = [item1.user_follow for item1 in follower]
        data2 = User.objects.filter(id__in=id1s)

        data={
            "following":data1,
            "follower":data2
        }
        serializer = GetFollowingSerializer(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetLeaderBoard(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        users = Follower.objects.filter(user_follow=id)
        ids = [item.user.id for item in users]
        datas = User.objects.filter(Q(id__in=ids)| Q(id=id) ).order_by("-total_mark_learned")
        serializer = UserSerializer(datas, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)
    



