from django.db import models
from account.models.users import User

class Follower(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    user_follow = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "follwer"
