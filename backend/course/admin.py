from django.contrib import admin
from course.models.category import Category
from course.models.conversation import Conversation
from course.models.vocabulary import Vocabulary
from course.models.level import Level
from course.models.course import Course

# Register your models here.
admin.site.register(Category)
admin.site.register(Conversation)
admin.site.register(Vocabulary)
admin.site.register(Level)
admin.site.register(Course)
