from django.contrib import admin
from study.models.user_course import UserCourse
from study.models.course_level import CourseLevel
# Register your models here.


admin.site.register(UserCourse)
admin.site.register(CourseLevel)
