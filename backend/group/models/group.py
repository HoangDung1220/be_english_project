from django.db import models
from account.models.users import User

class CHOICE_SET_STATUS(models.TextChoices):
    PUBLIC = "public"
    PRIVATE = "private"

class Group(models.Model):

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="upload/group", null=True, blank=True)
    status = models.CharField(max_length=20, choices=CHOICE_SET_STATUS.choices, default=CHOICE_SET_STATUS.PUBLIC)
    active = models.BooleanField(default=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "group"