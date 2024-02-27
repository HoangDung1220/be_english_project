from django.db import models
from course.models.course import Course

class Level(models.Model):
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=True, blank=True)
    indexing = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "level"