from django.urls import path,include
from study.views.user_course import UserCourseView
from study.views.course_level import CourseLevelView, CourseLevelAfterView,CourseLevelUser
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'study', CourseLevelAfterView, basename='study-exam-complete')
router.register(r'self', CourseLevelUser, basename='detail-course')

urlpatterns = [
    path('study', UserCourseView.as_view()),
    path('study/level', CourseLevelView.as_view()), 
    path('',include(router.urls)),
]
