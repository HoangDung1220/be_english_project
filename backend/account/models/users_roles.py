from django.db import models
from account.models.users import User
from account.models.roles import Roles

class UserRole(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name="role")
    group_id = models.IntegerField(null=True, blank=True)

    def __str__(self) :
        return self.user.username + " : " + self.role.name
    
    class Meta:
        db_table = "user_role"