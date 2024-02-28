from django.urls import path,include
from post.views.post import PostView,PostCreateView,GetPostView,DeletePostView
from post.views.motation import MotationView
from post.views.picture_post import PicturePostView
from post.views.comment import CommentView,CommentCreateView
urlpatterns = [
    path('post/<int:group>', PostView.as_view()),
    path('post/delete/<int:pk>', DeletePostView.as_view()),
    path('post', PostCreateView.as_view()),
    path('post/detail/<int:pk>', GetPostView.as_view()),
    path('motation', MotationView.as_view()),
    path('post/picture', PicturePostView.as_view()),
    path('post/comment', CommentCreateView.as_view()),
    path('post/comment/<int:post>', CommentView.as_view()),
]
