from django.db import models
from account.models.users import User
from course.models.level import Level
from course.models.vocabulary import Vocabulary


class ReviewWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    id_word_last = models.ForeignKey(Vocabulary,on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        db_table = "review_word"