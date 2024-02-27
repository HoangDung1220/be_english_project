from django.shortcuts import render
from account.models import User
from account.models.users_roles import UserRole
from account.models.roles import Roles
from account.serializers.UserSerializers import UserCreateSerializer, LoginSerializer, ChangePasswordSerializer, LogoutSerializer,UserDetailSerializer
from account.serializers.UserSerializers import UserSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.decorators import action
from suggest.suggest import Suggest
from group.models.group_member import GroupMember

# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        role_ins = Roles.objects.get(name="user")
        user_ins = User.objects.get(email=user_data['email'])
        UserRole.objects.create(user = user_ins, role= role_ins)
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class UserSuggestView(viewsets.ViewSet):

    @action(methods=['GET'],detail=False)
    def suggest(self,request,*args, **kwargs):
        try:
            id = self.request.query_params.get("user",None)
            id_group = self.request.query_params.get("group",None)
            group_members = GroupMember.objects.filter(group__id = id_group)
            ids_g = [item.member.id for item in group_members]
            ids = Suggest.getSuggestForUser(int(id))
            users = User.objects.filter(id__in = ids).exclude(id__in=ids_g)
            data = UserDetailSerializer(users, many=True).data
            return Response(data=data,status=status.HTTP_200_OK)
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_400_BAD_REQUEST)) 
        
class AccountAdmin(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def patch(self, request, *args, **kwargs):


class AccountDetailAdmin(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer