from django.urls import path,include
from group.views.group import GroupView, GroupDetailView, GroupSpaceView, GroupAdminView, GroupDetailAdminView
from group.views.group_member import GroupMemberView
from group.views.group_course import GroupCourseView, GroupCourseDestroyView
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'group/course', GroupCourseDestroyView, basename='group-course-delete')

urlpatterns = [
    path('group', GroupView.as_view()),
    path('group/<int:user>', GroupDetailView.as_view()),
    path('group/space/<int:user>', GroupSpaceView.as_view()),
    path('group/member',GroupMemberView.as_view()),
    path('group/course',GroupCourseView.as_view()),
    path('admin/group',GroupAdminView.as_view()),
    path('admin/group/<int:group>',GroupDetailAdminView.as_view()),
    path('',include(router.urls)),
]