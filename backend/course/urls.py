from django.urls import path,include
from course.views.course import CourseView,CourseDetailView, CourseInformationlView,CourseSuggestGroupView, CourseAdminView, CoursePublicView, TagPublicView, SearchCourseView
from course.views.level import LevelView
from course.views.vocabulary import VocabularyInLevel,VocabularyUserView, VocabularyInCourse
from course.views.vocabulary import VocabularyTestView, VocabularyInCoursePublic
from course.views.category import CategoryView, CategoryPublicView,CategoryDetailPublicView

from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'course', VocabularyUserView, basename='course-level')
router.register(r'course', CourseSuggestGroupView, basename='course-suggest')
router.register(r'course', SearchCourseView, basename='search-course')


urlpatterns = [
    path('course', CourseView.as_view()),
    path('course/admin', CourseAdminView.as_view()),
    path('course/category', CategoryPublicView.as_view()),
    path('course/<int:pk>', CourseDetailView.as_view()),
    path('course/detail/<int:pk>/<int:level>/<int:user>', CourseInformationlView.as_view()),
    path('course/level/', LevelView.as_view()),
    path('course/<int:id_course>/level/<int:id_level>/', VocabularyInLevel.as_view()),
    path('course/vocabulary/<int:id_course>/', VocabularyInCourse.as_view()),
    path('course/dictionary/<int:category>', CoursePublicView.as_view()),
    path('course/tag/<int:category>', TagPublicView.as_view()),
    path('vocabulary', VocabularyTestView.as_view()),
    path('vocabulary/category', CategoryView.as_view()),
    path('course/vocabulary/en/<int:id_course>/', VocabularyInCoursePublic.as_view()),
    path('course/category/<int:pk>', CategoryDetailPublicView.as_view()),
    path('',include(router.urls)),
]
