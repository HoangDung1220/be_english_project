from rest_framework import generics, status
from rest_framework.response import Response
from study.models.user_course import UserCourse
from course.models.course import Course
from study.serializers.user_course import UserCourseSerializer

class UserCourseView(generics.CreateAPIView):
    queryset = UserCourse.objects.filter(is_active=True)
    serializer_class = UserCourseSerializer

    def post(self, request, *args, **kwargs):
        id_user = request.data.get("user",None)
        id_course = request.data.get("course",None)
        if (id_user!=None and id_course!=None):
            item = self.queryset.filter(user__id=id_user).filter(course__id=id_course)
            if len(item)==0:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                item = self.queryset.filter(user__id=id_user).filter(course__id=id_course)
                course = Course.objects.get(id=id_course)
                course.number_user_learned = course.number_user_learned + 1
                course.save()
                return Response(dict(data=item[0].id, status=status.HTTP_201_CREATED, headers=headers))
            elif len(item):
                if item[0].is_complete:
                    return Response(dict(data=item[0].id,msg="User had learned before", status=status.HTTP_204_NO_CONTENT))
                else:
                    return Response(dict(data=item[0].id,msg="User was learning", status=status.HTTP_204_NO_CONTENT))