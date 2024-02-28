from django.db import models
from course.models.category import Category
from account.models.users import User

class CHOICE_SET_STATUS(models.TextChoices):
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null= True, blank=True)
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank=True)
    status = models.CharField(max_length=20, choices=CHOICE_SET_STATUS.choices, default=CHOICE_SET_STATUS.PUBLIC)
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(null=True,blank=True, upload_to="upload/course/image")
    description = models.CharField(max_length=256, null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True)
    number_user_learned = models.IntegerField(default=0)
    delete_flag = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "course"
