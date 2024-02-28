from django.contrib import admin
from study.models.user_course import UserCourse
from study.models.course_level import CourseLevel
from study.models.review_word import ReviewWord
# Register your models here.


admin.site.register(UserCourse)
admin.site.register(CourseLevel)
admin.site.register(ReviewWord)
