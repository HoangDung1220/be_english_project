from django.db import models
from course.models.level import Level

class Conversation(models.Model):

    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=1000)
    audio = models.FileField(upload_to="upload/course/conversation")

    class Meta:
        db_table = "conversation"
