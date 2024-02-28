from django.urls import path,include
from course.views.course import CourseView,CourseDetailView, CourseInformationlView,CourseSuggestGroupView, CourseAdminView, CoursePublicView, TagPublicView, SearchCourseView
from course.views.course import CreateImageCouse,UpdateImageCouse,SearchCoursePersonalView,CoursePublicEachUser
from course.views.course import DeleteCourse,CoursePublicEachUserAdmin,GetCourseView,CourseEachUserAdmin,CourseHomeView
from course.views.level import LevelView,LevelShowView,LevelUpdateView,LevelVocabularyView
from course.views.vocabulary import VocabularyInLevel,VocabularyUserView, VocabularyInCourse,VocabularyView,VocabularyUserReviewView
from course.views.vocabulary import VocabularyTestView, VocabularyInCoursePublic,ManagementVocabulary
from course.views.category import CategoryView, CategoryPublicView,CategoryDetailPublicView

from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'course', VocabularyUserView, basename='course-level')
router.register(r'course', CourseSuggestGroupView, basename='course-suggest')
router.register(r'course', SearchCourseView, basename='search-course')
router.register(r'course', VocabularyUserReviewView, basename='review-course')


urlpatterns = [
    path('course', CourseView.as_view()),
    path('course/basic/<int:pk>', GetCourseView.as_view()),
    path('course/admin', CourseAdminView.as_view()),
    path('course/category', CategoryPublicView.as_view()),
    path('course/<int:pk>', CourseDetailView.as_view()),
    path('course/delete/<int:pk>', DeleteCourse.as_view()),
    path('course/detail/<int:pk>/<int:level>/<int:user>', CourseInformationlView.as_view()),
    path('course/level/', LevelView.as_view()),
    path('course/update-level/<int:pk>', LevelUpdateView.as_view()),
    path('course/level/<int:id>', LevelShowView.as_view()),
    path('course/<int:id_course>/level/<int:id_level>/', VocabularyInLevel.as_view()),
    path('course/vocabulary/<int:id_course>/', VocabularyInCourse.as_view()),
    path('course/dictionary/<int:category>', CoursePublicView.as_view()),
    path('course/home/<int:id>', CourseHomeView.as_view()),
    path('course/tag/<int:category>', TagPublicView.as_view()),
    path('course/search/<int:user>', SearchCoursePersonalView.as_view()),
    path('vocabulary', VocabularyTestView.as_view()),
    path('course/vocabulary/management/<int:pk>', ManagementVocabulary.as_view()),
    path('vocabulary/create', VocabularyView.as_view()),
    path('vocabulary/category', CategoryView.as_view()),
    path('course/vocabulary/en/<int:id_course>/', VocabularyInCoursePublic.as_view()),
    path('course/category/<int:pk>', CategoryDetailPublicView.as_view()),
    path('course/create', CreateImageCouse.as_view()),
    path('course/create/<int:pk>', UpdateImageCouse.as_view()),
    path('course/level/detail/<int:id>', LevelVocabularyView.as_view()),
    path('course/user/<int:id>', CoursePublicEachUser.as_view()),
    path('course/admin/<int:id>', CourseEachUserAdmin.as_view()),
    path('course/admin/user/<int:id>', CoursePublicEachUserAdmin.as_view()),
    path('',include(router.urls)),
]
