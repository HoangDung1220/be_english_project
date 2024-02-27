from rest_framework import generics, viewsets
from rest_framework.decorators import action
from group.models.group_course import GroupCourse
from group.serializers.group_course import GroupCourseSerializer
from course.models.course import Course
from rest_framework.response import Response
from rest_framework import status
from account.models.users_roles import UserRole


class GroupCourseView(generics.CreateAPIView):
    queryset = GroupCourse.objects.all()
    serializer_class = GroupCourseSerializer

    def post(self, request, *args, **kwargs):
        # check exist course of you or course public
        try:
            id_user = request.data.get("member_add",None)
            id_group = request.data.get("group",None)
            id_course = request.data.get("course",None)

            course = Course.objects.get(id=id_course)
            if int(course.user_created.id) != int(id_user) and course.status != 'public':
                return Response(dict(msg="Course dosen't add to group", status=status.HTTP_400_BAD_REQUEST)) 

            course = GroupCourse.objects.filter(group__id = id_group).filter(course__id = id_course)
            if (len(course) > 0):
                return Response(dict(msg="Course was added to group. Please choice another course", status=status.HTTP_400_BAD_REQUEST)) 
            # save
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # transfer status private to protected
            course = Course.objects.get(id=id_course)
            if course.status == "private":
                course.status = "protected"
                course.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_400_BAD_REQUEST)) 
        
class GroupCourseDestroyView(viewsets.ViewSet):

    @action(methods=['DELETE'],detail=False)
    def remove(self,request,*args, **kwargs):
        try:
            id_user = self.request.query_params.get("user",None)
            id_course = self.request.query_params.get("course",None)
            id_group = self.request.query_params.get("group",None)
            is_permission_remove_1 = True
            is_permission_remove_2 = True
            # check course la public
            role = UserRole.objects.filter(user__id = id_user,group_id=id_group, role__name = 'admin_group')
            if (len(role)==0):
                is_permission_remove_1 = False
            roles = GroupCourse.objects.filter(group__id = id_group, course__id = id_course, member_add__id = id_user)
            if (len(roles)==0):
                is_permission_remove_2 = False


            if is_permission_remove_1 == True or is_permission_remove_2==True:
                course = Course.objects.get(id=id_course)
                group_course = GroupCourse.objects.get(group__id = id_group, course__id = id_course)
                if course.status == "protected":
                    group_course.delete()
                    course_protected = GroupCourse.objects.filter(course__id = course.id)
                    if (len(course_protected)==0):
                        course.status = "private"
                        course.save()
                else:
                    group_course.delete()
                return Response(dict(msg="You delete successful", status=status.HTTP_200_OK)) 
            else:
                return Response(dict(msg="You can't remove course", status=status.HTTP_400_BAD_REQUEST)) 
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_400_BAD_REQUEST)) 

        


    
