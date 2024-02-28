from django.urls import path,include
from rating.views.rating_course import RatingCourseView,GetRatingCourseView

urlpatterns = [
    path('course/rating', RatingCourseView.as_view()),
    path('course/rating/<int:course>/<int:user>', GetRatingCourseView.as_view()),

]