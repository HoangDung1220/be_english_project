from django.urls import path,include
from study.views.user_course import UserCourseView,LeaderBoardView
from study.views.course_level import CourseLevelView, CourseLevelAfterView,CourseLevelUser
from study.views.review_word import ReviewWordView,CourseLevelAfterReviewView
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'study', CourseLevelAfterView, basename='study-exam-complete')
router.register(r'self', CourseLevelUser, basename='detail-course')
router.register(r'study', CourseLevelAfterReviewView, basename='review-exam-complete')

urlpatterns = [
    path('study', UserCourseView.as_view()),
    path('study/level', CourseLevelView.as_view()), 
    path('review-word/', ReviewWordView.as_view()), 
    path('leader-board/<int:id>', LeaderBoardView.as_view()), 
    path('',include(router.urls)),
]
