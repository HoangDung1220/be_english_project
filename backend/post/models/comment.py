from django.db import models
from post.models.post import Post
from account.models.users import User

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.IntegerField(default=0)
    content = models.CharField(max_length=1000,null=True,blank=True)
    image = models.ImageField(null=True,blank=True, upload_to="upload/post/comment/image")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment"