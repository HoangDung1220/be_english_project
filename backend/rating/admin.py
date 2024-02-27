from django.contrib import admin
from rating.models.rating_course import RatingCourse
from rating.models.rating_group import RatingGroup

# Register your models here.
admin.site.register(RatingCourse)
admin.site.register(RatingGroup)