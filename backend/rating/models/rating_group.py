from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models.users import User
from group.models.group import Group

class RatingGroup(models.Model):
    rating = models.SmallIntegerField( default=0,validators=[MaxValueValidator(5),MinValueValidator(1)])
    comment = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self) :
        return self.user.username

    class Meta:
        db_table = "rating_group" 