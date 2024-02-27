from django.contrib import admin
from group.models.group import Group
from group.models.group_course import GroupCourse
from group.models.group_member import GroupMember

# Register your models here.
admin.site.register(Group)
admin.site.register(GroupCourse)
admin.site.register(GroupMember)

