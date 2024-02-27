from django.db import models
from post.models.post import Post

class PicturePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True, upload_to="upload/post/image")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "picture_post"