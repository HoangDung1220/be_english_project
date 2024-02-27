from django.db import models
from account.models.users import User
from group.models.group import Group

class GroupMember(models.Model):
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    user_invite_join = models.IntegerField()
    created_at_join = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        db_table = "group_member"