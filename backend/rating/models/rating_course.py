from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models.users import User
from course.models.course import Course

class RatingCourse(models.Model):
    rating = models.SmallIntegerField( default=0,validators=[MaxValueValidator(5),MinValueValidator(1)])
    comment = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) :
        return self.user.username

    class Meta:
        db_table = "rating_course" 
