from django.contrib import admin
from post.models.post import Post
from post.models.picture_post import PicturePost
from post.models.motation import Motation
from post.models.comment import Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(PicturePost)
admin.site.register(Motation)
admin.site.register(Comment)
