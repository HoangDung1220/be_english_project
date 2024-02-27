from django.db import models
from course.models.level import Level
from course.models.vocabulary import Vocabulary
from study.models.user_course import UserCourse


class CourseLevel(models.Model):

    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    last_question_learned = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, null=True, blank=True)
    is_complete = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = "course_level"

