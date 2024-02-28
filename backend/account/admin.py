from django.contrib import admin
from account.models.roles import Roles
from account.models.users import User
from account.models.users_roles import UserRole
from account.models.follower import Follower

# Register your models here.

admin.site.register(User)
admin.site.register(Roles)
admin.site.register(UserRole)
admin.site.register(Follower)

