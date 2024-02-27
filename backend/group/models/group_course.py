from django.db import models
from account.models.users import User
from group.models.group import Group
from course.models.course import Course


class GroupCourse(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    member_add = models.ForeignKey(User, on_delete=models.CASCADE)
    percentage = models.FloatField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   
    
    class Meta:
        db_table = "group_course"