from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from account.models import User
from account.models.users_roles import UserRole

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username")

class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = User
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password"
    )

    class Meta:
        model = User
        fields = ["email", "password", "password2", "username"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."}
            )
        if password != password2:
            raise serializers.ValidationError({"password": "The two passwords differ."})
        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id","email", "password", "username", "tokens", "roles"]

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])

        return {"access": user.tokens()["access"], "refresh": user.tokens()["refresh"]}
    
    def get_roles(self, obj):
        print(obj)
        lst_user_role = UserRole.objects.filter(user__email=obj["email"])
        convert_role = ""
        for user_role in lst_user_role:
            convert_role = convert_role + str(user_role.role.id)
        return convert_role

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        return {"id":user.id,"email": user.email, "username": user.username, "tokens": user.tokens}


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")

# class AccountSerializer(serializers.Serializer):
#     account = UserSerializer()
#     roles = serializers.CharField()