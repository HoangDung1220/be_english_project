from course.models.level import Level
from course.models.course import Course
from django.db import models

class Vocabulary(models.Model):
    vocabulary = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    mean = models.CharField(max_length=100, null=True, blank=True)
    sample = models.CharField(max_length=100, null=True,blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)
    indexing = models.IntegerField(default=0)
    image = models.ImageField(upload_to="upload/course/vocabulary/image", null=True, blank=True)
    audio = models.FileField(upload_to="upload/course/vocabulary/audio",blank=True, null=True)

    def __str__(self):
        return self.vocabulary
    
    class Meta:
        db_table = "vocabulary"