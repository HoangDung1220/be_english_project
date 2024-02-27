from django.contrib import admin
from account.models.roles import Roles
from account.models.users import User
from account.models.users_roles import UserRole

# Register your models here.

admin.site.register(User)
admin.site.register(Roles)
admin.site.register(UserRole)

