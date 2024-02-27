from django.db import models
from account.models.users import User
from course.models.course import Course


class UserCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False, null=True, blank=True)
    total_score = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.course.title+" : "+ self.user.username

    class Meta:
        db_table = "user_course"

